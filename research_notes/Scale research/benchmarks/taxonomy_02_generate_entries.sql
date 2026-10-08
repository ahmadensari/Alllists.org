-- 02_generate_entries.sql : synthetic entries and memberships (entry_concept) on top of 01_generate_concepts.sql.
-- Scratch database only (name starts with bench_). Default 2,000,000 entries, about 3 memberships each.
\set ON_ERROR_STOP on
\timing on
\if :{?n_entries}
\else
\set n_entries 2000000
\endif
SELECT setseed(0.43);
SET maintenance_work_mem = '1GB';
SET work_mem = '256MB';

DROP TABLE IF EXISTS ec, ec_raw, entry_prim, entry_src, entry CASCADE;
DROP FUNCTION IF EXISTS pick_node(int, double precision);

-- node at relative position pos (0..1) inside a level; neighbours in a level share a sector
CREATE FUNCTION pick_node(lvl int, pos double precision) RETURNS int LANGUAGE sql IMMUTABLE AS $$
  SELECT (ARRAY[1,2,32,592,3992,12392])[lvl + 1]
       + GREATEST(0, LEAST((ARRAY[1,30,560,3400,8400,37609])[lvl + 1] - 1,
                           floor(pos * (ARRAY[1,30,560,3400,8400,37609])[lvl + 1])::int));
$$;

-- raw draws: place (220 countries, 17 regions, 12 cities, 3 areas, skewed), level, rank, state
CREATE TABLE entry_src AS
SELECT g AS id,
       floor(220 * power(random(), 2.5))::int AS c,
       floor(17 * power(random(), 1.8))::int AS a,
       floor(12 * power(random(), 1.8))::int AS t,
       floor(3 * power(random(), 1.5))::int AS r,
       random() AS u_area, random() AS u_lvl, random() AS u_rank, random() AS u_pub,
       power(random(), 2.5) AS pos
FROM generate_series(1, :n_entries) g;

CREATE TABLE entry_prim AS
SELECT s.id,
       CASE WHEN s.u_lvl < 0.05 THEN 3 WHEN s.u_lvl < 0.40 THEN 4 ELSE 5 END AS lvl,
       s.pos
FROM entry_src s;
ALTER TABLE entry_prim ADD COLUMN cid int;
UPDATE entry_prim SET cid = pick_node(lvl, pos);

CREATE TABLE entry AS
SELECT s.id,
       chr(97 + s.c / 26) || chr(97 + s.c % 26) AS country_code,
       chr(97 + s.c / 26) || chr(97 + s.c % 26)
         || '.region_' || lpad(s.a::text, 2, '0')
         || '.city_' || lpad(s.t::text, 3, '0')
         || CASE WHEN s.u_area < 0.30 THEN '.area_' || lpad(s.r::text, 2, '0') ELSE '' END AS place_path,
       CASE WHEN s.u_pub < 0.85 THEN 1 ELSE 0 END::smallint AS publish_state,      -- 1 = published
       CASE WHEN s.u_rank < 0.03 THEN 0 WHEN s.u_rank < 0.10 THEN 1 WHEN s.u_rank < 0.40 THEN 2 ELSE 3 END::smallint AS rank, -- 0 surveyor, 1 owner, 2 ai, 3 none
       (floor(random() * 1000))::int AS fresh,
       md5(s.id::text) AS name,
       repeat(md5((s.id * 7)::text), 6) AS filler                                    -- about 190 bytes of other columns
FROM entry_src s;
ALTER TABLE entry ADD COLUMN sort_key int;
UPDATE entry SET sort_key = rank * 1000 + fresh;
ALTER TABLE entry ADD PRIMARY KEY (id);
DROP TABLE entry_src;

-- memberships: 1 primary + 0..4 secondary (mean 2); secondary 70% near the primary (same sector), 30% anywhere
CREATE TABLE ec_raw AS
SELECT p.id AS entry_id, p.cid AS concept_id, 1::smallint AS role FROM entry_prim p
UNION ALL
SELECT p.id, pick_node(CASE WHEN x.u1 < 0.6 THEN 5 ELSE 4 END,
                       CASE WHEN x.u2 < 0.7 THEN p.pos + (x.u3 - 0.5) * 0.02 ELSE power(x.u3, 2.5) END), 2::smallint
FROM (SELECT id, pos, (ARRAY[0,0,1,1,2,2,3,3,4,4])[1 + floor(random() * 10)::int] AS s FROM entry_prim) p
CROSS JOIN LATERAL generate_series(1, p.s) g
CROSS JOIN LATERAL (SELECT random() + (g - g) AS u1, random() AS u2, random() AS u3) x;

CREATE TABLE ec (
    entry_id bigint NOT NULL,
    concept_id int NOT NULL,
    role smallint NOT NULL,
    place_path text NOT NULL,
    published boolean NOT NULL,
    sort_key int NOT NULL
);
INSERT INTO ec
SELECT DISTINCT ON (r.entry_id, r.concept_id) r.entry_id, r.concept_id, r.role, e.place_path, e.publish_state = 1, e.sort_key
FROM ec_raw r JOIN entry e ON e.id = r.entry_id
ORDER BY r.entry_id, r.concept_id, r.role;
DROP TABLE ec_raw, entry_prim;

ALTER TABLE ec ADD PRIMARY KEY (entry_id, concept_id);                                         -- I1 membership uniqueness, entry -> concepts
CREATE UNIQUE INDEX ec_primary_uq ON ec (entry_id) WHERE role = 1;                             -- I4 exactly one primary
CREATE INDEX ec_list ON ec (concept_id, place_path text_pattern_ops) INCLUDE (entry_id, sort_key) WHERE published;  -- I3 list page
CREATE INDEX entry_place ON entry (place_path text_pattern_ops);                               -- like the repo's place_path_prefix
VACUUM (ANALYZE) entry;
VACUUM (ANALYZE) ec;

\echo '--- entry statistics ---'
SELECT count(*) AS entries, count(*) FILTER (WHERE publish_state = 1) AS published FROM entry;
SELECT count(*) AS memberships, round(count(*)::numeric / (SELECT count(*) FROM entry), 2) AS per_entry,
       count(*) FILTER (WHERE role = 1) AS primaries FROM ec;
SELECT count(DISTINCT place_path) AS distinct_home_places, count(DISTINCT split_part(place_path, '.', 1)) AS countries FROM entry;
SELECT relname, pg_size_pretty(pg_total_relation_size(oid)) AS total, pg_size_pretty(pg_relation_size(oid)) AS heap
FROM pg_class WHERE relname IN ('entry', 'ec') ORDER BY relname;
SELECT indexrelid::regclass AS index, pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_index WHERE indrelid IN ('ec'::regclass, 'entry'::regclass) ORDER BY 1::text;
