-- taxonomy_13_design_table_size.sql : bytes per row and load time of the DESIGNED membership table, with the real column set,
-- the real data types (bigint concept id and entry id, as Django makes them) and the real indexes. The older benchmark tables
-- (taxonomy_02) had 6 columns and an int concept id; this file measures the table the note proposes.
--   V1  as the migrations create it: surrogate id key, plus the two foreign-key indexes Django adds by default
--   V2  V1 without the two foreign-key indexes (db_index=False on both foreign keys)
--   V3  composite primary key (entry_id, concept_id) and no id column (Django 5.2 CompositePrimaryKey)
-- Run in the design scratch database (bench_alllists_design_*) after `migrate`. 1,000,000 entries x 3 memberships = 3,000,000 rows.
\set ON_ERROR_STOP on
\timing on
SET maintenance_work_mem = '512MB';
SELECT setseed(0.45);
DROP TABLE IF EXISTS ec_stage, ec_v1, ec_v2, ec_v3;

CREATE TABLE ec_stage AS
SELECT e AS entry_id,
       (12392 + ((e * 31 + k * 1009) % 37609))::bigint AS concept_id,
       CASE WHEN k = 0 THEN 1 ELSE 2 END::smallint AS role,
       'zz' AS country_code,
       'zz.region_' || lpad(((e * 7) % 17)::text, 2, '0') || '.city_' || lpad(((e * 13) % 12)::text, 3, '0')
         || CASE WHEN e % 10 < 3 THEN '.area_' || lpad((e % 3)::text, 2, '0') ELSE '' END AS place_path,
       (random() < 0.85) AS listable,
       (CASE WHEN random() < 0.03 THEN 0 WHEN random() < 0.10 THEN 1 WHEN random() < 0.40 THEN 2 ELSE 3 END)::smallint AS best_level,
       (e % 1000)::int AS sk,
       k
FROM generate_series(1, 1000000) e, generate_series(0, 2) k;
SELECT count(*) AS stage_rows, avg(length(place_path))::numeric(5,1) AS avg_place_path_chars FROM ec_stage;

CREATE TABLE ec_v1 (LIKE entries_entryconcept INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES);
CREATE TABLE ec_v2 (LIKE entries_entryconcept INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES);
-- the two foreign-key indexes Django adds: non-unique, one column, no WHERE (the partial review-queue index has a WHERE)
DO $$
DECLARE r record;
BEGIN
  FOR r IN SELECT indexrelid::regclass::text AS n FROM pg_index
           WHERE indrelid = 'ec_v2'::regclass AND NOT indisunique AND indnatts = 1 AND indpred IS NULL
  LOOP
    EXECUTE 'DROP INDEX ' || r.n;
  END LOOP;
END $$;
CREATE TABLE ec_v3 (LIKE entries_entryconcept INCLUDING DEFAULTS INCLUDING CONSTRAINTS);
ALTER TABLE ec_v3 DROP COLUMN id;
ALTER TABLE ec_v3 ADD PRIMARY KEY (entry_id, concept_id);
CREATE UNIQUE INDEX ec_v3_primary ON ec_v3 (entry_id) WHERE role = 1;
CREATE INDEX ec_v3_list ON ec_v3 (concept_id, place_path text_pattern_ops) INCLUDE (entry_id, sort_key) WHERE listable;
CREATE INDEX ec_v3_place_list ON ec_v3 (place_path text_pattern_ops, concept_id) INCLUDE (entry_id, sort_key) WHERE listable;
CREATE INDEX ec_v3_review ON ec_v3 (state) WHERE state = 1;

-- the rows: the same 3,000,000 for every variant; the indexes exist while loading (the worst case for load time)
\echo '--- load V1'
INSERT INTO ec_v1 (entry_id, concept_id, role, state, source, broad, rank, added_at, country_code, place_path, listable, best_level, sort_key)
SELECT entry_id, concept_id, role, 2, 2, false, 0, now(), country_code, place_path, listable, best_level,
       (CASE WHEN role = 1 THEN 0 ELSE 1 END) * 100000000 + best_level * 1000000 + sk FROM ec_stage ORDER BY entry_id, k;
\echo '--- load V2'
INSERT INTO ec_v2 (entry_id, concept_id, role, state, source, broad, rank, added_at, country_code, place_path, listable, best_level, sort_key)
SELECT entry_id, concept_id, role, 2, 2, false, 0, now(), country_code, place_path, listable, best_level,
       (CASE WHEN role = 1 THEN 0 ELSE 1 END) * 100000000 + best_level * 1000000 + sk FROM ec_stage ORDER BY entry_id, k;
\echo '--- load V3'
INSERT INTO ec_v3 (entry_id, concept_id, role, state, source, broad, rank, added_at, country_code, place_path, listable, best_level, sort_key)
SELECT entry_id, concept_id, role, 2, 2, false, 0, now(), country_code, place_path, listable, best_level,
       (CASE WHEN role = 1 THEN 0 ELSE 1 END) * 100000000 + best_level * 1000000 + sk FROM ec_stage ORDER BY entry_id, k;
VACUUM (ANALYZE) ec_v1; VACUUM (ANALYZE) ec_v2; VACUUM (ANALYZE) ec_v3;

\echo '--- sizes'
SELECT t AS variant, rows, pg_size_pretty(heap) AS heap, pg_size_pretty(idx) AS indexes, pg_size_pretty(total) AS total,
       round(heap::numeric / rows, 1) AS heap_bytes_per_row, round(idx::numeric / rows, 1) AS index_bytes_per_row, round(total::numeric / rows, 1) AS total_bytes_per_row
FROM (SELECT t, (SELECT reltuples::bigint FROM pg_class WHERE relname = t) AS rows,
             pg_relation_size(t::regclass) AS heap, pg_indexes_size(t::regclass) AS idx, pg_total_relation_size(t::regclass) AS total
      FROM (VALUES ('ec_v1'), ('ec_v2'), ('ec_v3')) v(t)) s ORDER BY t;
SELECT c.relname AS index, pg_size_pretty(pg_relation_size(c.oid)) AS size, round(pg_relation_size(c.oid)::numeric / 3000000, 1) AS bytes_per_row
FROM pg_index i JOIN pg_class c ON c.oid = i.indexrelid WHERE i.indrelid IN ('ec_v1'::regclass, 'ec_v2'::regclass, 'ec_v3'::regclass) ORDER BY c.relname;
DROP TABLE ec_stage, ec_v1, ec_v2, ec_v3;
