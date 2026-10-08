-- 03_variant_tables.sql : the two extra physical designs that are compared with the plain closure design.
--   ec_lt : V2b, the ltree design that copies every root-to-node path of the concept onto the membership row (ltree[] + GiST)
--   ec_pl : place path stored as ltree with a GiST index (instead of text + text_pattern_ops)
-- Scratch database only (bench_*).
\set ON_ERROR_STOP on
\timing on
SET maintenance_work_mem = '1GB';
SET work_mem = '256MB';
DROP TABLE IF EXISTS ec_lt, ec_pl;

CREATE TABLE ec_lt AS
SELECT ec.entry_id, ec.concept_id, ec.role, ec.place_path, ec.published, ec.sort_key, p.paths AS cpaths
FROM ec JOIN (SELECT concept_id, array_agg(path) AS paths FROM concept_path GROUP BY 1) p ON p.concept_id = ec.concept_id;
ALTER TABLE ec_lt ADD PRIMARY KEY (entry_id, concept_id);
CREATE INDEX ec_lt_paths_gist ON ec_lt USING gist (cpaths);                          -- default siglen (8 bytes)
CREATE INDEX ec_lt_place ON ec_lt (place_path text_pattern_ops) WHERE published;
VACUUM (ANALYZE) ec_lt;

CREATE TABLE ec_pl AS
SELECT entry_id, concept_id, role, place_path::ltree AS place_l, published, sort_key FROM ec;
ALTER TABLE ec_pl ADD PRIMARY KEY (entry_id, concept_id);
CREATE INDEX ec_pl_list ON ec_pl USING gist (concept_id, place_l) WHERE published;   -- btree_gist on concept_id
VACUUM (ANALYZE) ec_pl;

SELECT relname, pg_size_pretty(pg_total_relation_size(oid)) AS total, pg_size_pretty(pg_relation_size(oid)) AS heap
FROM pg_class WHERE relname IN ('ec','ec_lt','ec_pl') ORDER BY relname;
SELECT indexrelid::regclass AS index, pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_index WHERE indrelid IN ('ec'::regclass,'ec_lt'::regclass,'ec_pl'::regclass) ORDER BY 1::text;
SELECT round(avg(cardinality(cpaths)), 2) AS avg_paths_per_membership, max(cardinality(cpaths)) AS max_paths FROM ec_lt;
