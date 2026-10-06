-- taxonomy_11_backfill_graph.sql : time of the E2 data step (edges, closure by recursion, slugs) on a legacy-shaped tree of
-- 50,000 nodes (primary parent only), the same SQL as taxonomy/migrations/0005_backfill_graph.py. Scratch database only.
\set ON_ERROR_STOP on
\timing on
CREATE TEMP TABLE t_concept AS
SELECT c.id, e.parent_id, NULL::int AS level, c.slug, 'list_type'::text AS kind, now() AS created_at
FROM concept c LEFT JOIN concept_edge e ON e.child_id = c.id AND e.is_primary;
CREATE UNIQUE INDEX ON t_concept (id);
CREATE INDEX ON t_concept (parent_id);
CREATE TEMP TABLE t_edge (parent_id int, child_id int, is_primary bool, reason text, created_at timestamptz, PRIMARY KEY (parent_id, child_id));
CREATE TEMP TABLE t_closure (ancestor_id int, descendant_id int, depth smallint, PRIMARY KEY (ancestor_id, descendant_id));
CREATE TEMP TABLE t_slug (slug text PRIMARY KEY, concept_id int, is_current bool, reason text, created_at timestamptz);
\echo '--- edges'
INSERT INTO t_edge SELECT parent_id, id, true, 'primary', created_at FROM t_concept WHERE parent_id IS NOT NULL ON CONFLICT DO NOTHING;
\echo '--- levels'
WITH RECURSIVE t(id, d) AS (SELECT id, 0 FROM t_concept WHERE parent_id IS NULL UNION ALL SELECT c.id, t.d + 1 FROM t_concept c JOIN t ON c.parent_id = t.id)
UPDATE t_concept c SET level = t.d FROM t WHERE c.id = t.id AND c.level IS NULL AND t.d <= 7;
\echo '--- closure by recursion'
WITH RECURSIVE r(a, d, depth) AS (
    SELECT id, id, 0 FROM t_concept
    UNION ALL SELECT r.a, e.child_id, r.depth + 1 FROM r JOIN t_edge e ON e.parent_id = r.d)
INSERT INTO t_closure (ancestor_id, descendant_id, depth) SELECT a, d, min(depth) FROM r GROUP BY a, d ON CONFLICT DO NOTHING;
\echo '--- slugs'
INSERT INTO t_slug SELECT slug, id, true, 'created', created_at FROM t_concept WHERE kind = 'list_type' ON CONFLICT (slug) DO NOTHING;
SELECT (SELECT count(*) FROM t_edge) AS edges, (SELECT count(*) FROM t_closure) AS closure_rows, (SELECT count(*) FROM t_slug) AS slugs;
