-- taxonomy_11b_rebuild_closure_dag.sql : time to rebuild the whole closure table from the edge table by recursion, on the
-- 50,000-node DAG of taxonomy_01 (stress mix, 99,871 edges, 1,004,185 closure rows). The closure is derived data: this is the
-- cost of throwing it away and building it again. Scratch database only (bench_taxonomy_*).
\set ON_ERROR_STOP on
\timing on
SET work_mem = '128MB';
DROP TABLE IF EXISTS closure_rebuilt;
CREATE TABLE closure_rebuilt (ancestor_id int, descendant_id int, depth smallint, PRIMARY KEY (ancestor_id, descendant_id));
WITH RECURSIVE r(a, d, depth) AS (
    SELECT id, id, 0 FROM concept
    UNION
    SELECT r.a, e.child_id, r.depth + 1 FROM r JOIN concept_edge e ON e.parent_id = r.d)
INSERT INTO closure_rebuilt SELECT a, d, min(depth) FROM r GROUP BY a, d;
SELECT count(*) AS rows_rebuilt,
       (SELECT count(*) FROM concept_closure) AS rows_in_table,
       (SELECT count(*) FROM (SELECT ancestor_id, descendant_id FROM concept_closure EXCEPT SELECT ancestor_id, descendant_id FROM closure_rebuilt) x) AS missing,
       (SELECT count(*) FROM (SELECT ancestor_id, descendant_id FROM closure_rebuilt EXCEPT SELECT ancestor_id, descendant_id FROM concept_closure) y) AS extra
FROM closure_rebuilt;
DROP TABLE closure_rebuilt;
