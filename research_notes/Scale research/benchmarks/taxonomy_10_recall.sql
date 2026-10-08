-- taxonomy_10_recall.sql : what a list page loses when the graph or the memberships are simplified.
-- For the 250 benchmark pairs (node X at place Y), count distinct published entries under three rules:
--   full      closure over every parent, every membership (the design)
--   primary_tree  descendants through PRIMARY edges only (what a single-path ltree or Concept.parent gives), every membership
--   current   primary edges only AND the primary membership only (what the repository does today: Entry.primary_concept
--             in the descendants of the node, which ignores secondary parents and secondary products)
-- Scratch database only (bench_*).
\set ON_ERROR_STOP on
\timing off
DROP TABLE IF EXISTS bench_recall;
CREATE TABLE bench_recall AS
WITH RECURSIVE pd(anc, d) AS (
    SELECT DISTINCT concept_id, concept_id FROM bench_pairs
    UNION ALL
    SELECT pd.anc, e.child_id FROM pd JOIN concept_edge e ON e.parent_id = pd.d AND e.is_primary
)
SELECT bp.id AS pair_id, bp.concept_level, bp.place_level, bp.n_members AS full_members,
       (SELECT count(DISTINCT ec.entry_id) FROM pd JOIN ec ON ec.concept_id = pd.d AND ec.published
         WHERE pd.anc = bp.concept_id AND (bp.place_path = '' OR ec.place_path = bp.place_path OR ec.place_path LIKE bp.place_path || '.%')) AS primary_tree_members,
       (SELECT count(DISTINCT ec.entry_id) FROM pd JOIN ec ON ec.concept_id = pd.d AND ec.published AND ec.role = 1
         WHERE pd.anc = bp.concept_id AND (bp.place_path = '' OR ec.place_path = bp.place_path OR ec.place_path LIKE bp.place_path || '.%')) AS current_members
FROM bench_pairs bp;

SELECT concept_level,
       count(*) AS pairs,
       round(100.0 * sum(primary_tree_members) / sum(full_members), 1) AS pct_seen_by_primary_tree,
       round(100.0 * sum(current_members) / sum(full_members), 1) AS pct_seen_by_current_code
FROM bench_recall GROUP BY ROLLUP (concept_level) ORDER BY concept_level NULLS LAST;
SELECT round(100.0 * avg(CASE WHEN full_members > 0 THEN current_members::numeric / full_members END), 1) AS mean_pct_per_page_seen_by_current_code,
       count(*) FILTER (WHERE current_members < full_members) AS pages_where_current_code_misses_entries,
       count(*) AS pages
FROM bench_recall;
