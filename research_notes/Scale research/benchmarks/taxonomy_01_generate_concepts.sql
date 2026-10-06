-- 01_generate_concepts.sql : synthetic taxonomy (50,000 nodes, a DAG with 2 parents on average).
-- Run only against a scratch database whose name starts with bench_. See run_all.sh.
-- Level sizes follow 01_manufacturing_depth_taxonomy.md section 3.1: 30 sectors, 560 industries, 3,400 families,
-- 8,400 products and 37,609 variants (plus one root) = 50,000 nodes.
\set ON_ERROR_STOP on
\timing on
-- Secondary-parent mix: psql variable sec_array (default: 2 parents on average). Examples:
--   stress   0,0,0,1,1,1,1,1,2,3   (mean 1.0 secondary parents per node, 2.0 parents in all)  [default]
--   moderate 0,0,0,0,0,0,0,0,0,1   (about 1.1 parents)
--   seedlike 0 x49 then 1          (about 1.02 parents: the seed has 21 secondary links in 1,170 nodes)
\if :{?sec_array}
\else
\set sec_array '0,0,0,1,1,1,1,1,2,3'
\endif
CREATE EXTENSION IF NOT EXISTS ltree;
CREATE EXTENSION IF NOT EXISTS btree_gist;
SELECT setseed(0.42);
SET maintenance_work_mem = '512MB';
SET work_mem = '128MB';

DROP TABLE IF EXISTS lv, concept_edge, concept_closure, concept_path, concept CASCADE;

CREATE TABLE lv (level int PRIMARY KEY, n int NOT NULL, first_id int NOT NULL);
INSERT INTO lv VALUES (0,1,1),(1,30,2),(2,560,32),(3,3400,592),(4,8400,3992),(5,37609,12392);

CREATE TABLE concept (
    id int PRIMARY KEY,
    level smallint NOT NULL,
    idx int NOT NULL,
    slug text NOT NULL,
    status text NOT NULL DEFAULT 'active'
);
INSERT INTO concept (id, level, idx, slug)
SELECT lv.first_id + g, lv.level, g, 'node-' || (lv.first_id + g)
FROM lv, LATERAL generate_series(0, lv.n - 1) g;

-- Edges. Every parent sits exactly one level above the child (rule M2: same level as the primary parent).
CREATE TABLE concept_edge (
    parent_id int NOT NULL,
    child_id int NOT NULL,
    is_primary boolean NOT NULL,
    PRIMARY KEY (parent_id, child_id)
);
CREATE INDEX concept_edge_child ON concept_edge (child_id);

-- primary parent: contiguous blocks, so neighbours in a level share a sector
INSERT INTO concept_edge
SELECT p.first_id + (c.idx::bigint * p.n / cl.n)::int, c.id, true
FROM concept c
JOIN lv cl ON cl.level = c.level
JOIN lv p ON p.level = c.level - 1
WHERE c.level >= 1;

-- secondary parents: 0..3 per node, mean 1.0 (so 2 parents on average), 60% near the primary, 40% anywhere in the level.
-- Materialised in a temp table first: random() inside a join was evaluated more than once per row in a one-statement form.
CREATE TEMP TABLE sec_pick AS
SELECT base.id, base.level, sec.pidx
FROM (
    SELECT c.id, c.level,
           (c.idx::bigint * p.n / cl.n)::int AS pidx0,
           p.n AS pn,
           GREATEST(2, p.n / 100) AS w,
           (ARRAY[:sec_array])[1 + floor(random() * cardinality(ARRAY[:sec_array]))::int] AS s
    FROM concept c
    JOIN lv cl ON cl.level = c.level
    JOIN lv p ON p.level = c.level - 1
    WHERE c.level >= 2
) base
CROSS JOIN LATERAL generate_series(1, base.s) g
CROSS JOIN LATERAL (
    SELECT GREATEST(0, LEAST(base.pn - 1 + (g - g),   -- (g - g) forces one evaluation per generated row, not per node
               CASE WHEN random() < 0.6
                    THEN base.pidx0 + floor(random() * (2 * base.w + 1))::int - base.w
                    ELSE floor(random() * base.pn)::int END)) AS pidx
) sec
WHERE sec.pidx <> base.pidx0;
INSERT INTO concept_edge
SELECT p.first_id + sp.pidx, sp.id, false
FROM sec_pick sp JOIN lv p ON p.level = sp.level - 1
ON CONFLICT DO NOTHING;

-- closure table: (ancestor, descendant, depth), self rows included
CREATE TABLE concept_closure (
    ancestor_id int NOT NULL,
    descendant_id int NOT NULL,
    depth smallint NOT NULL,
    PRIMARY KEY (ancestor_id, descendant_id)
);
INSERT INTO concept_closure SELECT id, id, 0 FROM concept;
CREATE INDEX concept_closure_desc ON concept_closure (descendant_id, ancestor_id);
DO $$
DECLARE k int;
BEGIN
  FOR k IN 1..5 LOOP
    INSERT INTO concept_closure
    SELECT DISTINCT cl.ancestor_id, e.child_id, cl.depth + 1
    FROM concept_edge e
    JOIN concept ch ON ch.id = e.child_id AND ch.level = k
    JOIN concept_closure cl ON cl.descendant_id = e.parent_id
    ON CONFLICT DO NOTHING;
  END LOOP;
END $$;

-- ltree: one row per root-to-node path (a DAG needs one path per route). Label = 'n' || concept id.
CREATE TABLE concept_path (
    concept_id int NOT NULL,
    path ltree NOT NULL
);
INSERT INTO concept_path SELECT id, ('n' || id)::ltree FROM concept WHERE level = 0;
CREATE INDEX concept_path_concept ON concept_path (concept_id);
DO $$
DECLARE k int;
BEGIN
  FOR k IN 1..5 LOOP
    INSERT INTO concept_path
    SELECT e.child_id, cp.path || ('n' || e.child_id)::ltree
    FROM concept_edge e
    JOIN concept ch ON ch.id = e.child_id AND ch.level = k
    JOIN concept_path cp ON cp.concept_id = e.parent_id;
  END LOOP;
END $$;
CREATE INDEX concept_path_gist ON concept_path USING gist (path);
CREATE INDEX concept_path_btree ON concept_path (path);

ANALYZE;

\echo '--- taxonomy statistics ---'
SELECT count(*) AS nodes FROM concept;
SELECT count(*) AS edges, round(count(*)::numeric / (SELECT count(*) - 1 FROM concept), 2) AS parents_per_node FROM concept_edge;
SELECT count(*) AS closure_rows, round(count(*)::numeric / (SELECT count(*) FROM concept), 2) AS closure_rows_per_node FROM concept_closure;
SELECT count(*) AS ltree_paths, round(count(*)::numeric / (SELECT count(*) FROM concept), 2) AS paths_per_node, max(nlevel(path)) AS max_depth FROM concept_path;
SELECT c.level, count(*) AS nodes, round(avg(np.n), 1) AS avg_paths, max(np.n) AS max_paths,
       round(avg(nc.n), 1) AS avg_ancestors, max(nc.n) AS max_ancestors
FROM concept c
JOIN (SELECT concept_id, count(*) n FROM concept_path GROUP BY 1) np ON np.concept_id = c.id
JOIN (SELECT descendant_id, count(*) n FROM concept_closure GROUP BY 1) nc ON nc.descendant_id = c.id
GROUP BY c.level ORDER BY c.level;
SELECT c.level, count(*) AS nodes, round(avg(d.n), 1) AS avg_descendants, max(d.n) AS max_descendants
FROM concept c JOIN (SELECT ancestor_id, count(*) n FROM concept_closure GROUP BY 1) d ON d.ancestor_id = c.id
WHERE c.level <= 4 GROUP BY c.level ORDER BY c.level;
SELECT relname, pg_size_pretty(pg_total_relation_size(oid)) AS total FROM pg_class
WHERE relname IN ('concept','concept_edge','concept_closure','concept_path') ORDER BY relname;
SELECT indexrelid::regclass AS index, pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_index WHERE indrelid IN ('concept_closure'::regclass,'concept_path'::regclass,'concept_edge'::regclass) ORDER BY 1::text;
