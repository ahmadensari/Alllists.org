-- 04_pairs.sql : the list pages used by the query benchmark. Each pair is (node X, place Y) that really has entries
-- (decision E28: lists exist only where entries exist). Sampling follows the entries, so popular cells are picked
-- more often than a uniform draw over (node, place) would. 10 pairs for each (node level 1..5) x (place level 0..4).
-- Scratch database only (bench_*).
\set ON_ERROR_STOP on
SELECT setseed(0.44);
DROP TABLE IF EXISTS bench_pairs;
CREATE TABLE bench_pairs (
    id serial PRIMARY KEY,
    concept_level int NOT NULL,
    place_level int NOT NULL,          -- 0 world, 1 country, 2 region, 3 city, 4 area
    concept_id int NOT NULL,
    place_path text NOT NULL,
    n_members int,                     -- distinct published entries, by the closure query
    n_desc int,                        -- descendant nodes of X, self included
    UNIQUE (concept_id, place_path)
);
DO $$
DECLARE L int; P int; i int; tries int; e record; anc int; pref text; labels int;
BEGIN
  FOR L IN 1..5 LOOP
    FOR P IN 0..4 LOOP
      i := 0; tries := 0;
      WHILE i < 10 AND tries < 5000 LOOP
        tries := tries + 1;
        SELECT en.id, en.place_path, ec.concept_id AS prim INTO e
        FROM entry en JOIN ec ON ec.entry_id = en.id AND ec.role = 1
        WHERE en.id = 1 + floor(random() * 2000000)::int AND en.publish_state = 1;
        CONTINUE WHEN e.id IS NULL;
        labels := array_length(string_to_array(e.place_path, '.'), 1);
        CONTINUE WHEN labels < P;
        SELECT cl.ancestor_id INTO anc FROM concept_closure cl JOIN concept c ON c.id = cl.ancestor_id
        WHERE cl.descendant_id = e.prim AND c.level = L ORDER BY random() LIMIT 1;
        CONTINUE WHEN anc IS NULL;
        pref := CASE WHEN P = 0 THEN '' ELSE array_to_string((string_to_array(e.place_path, '.'))[1:P], '.') END;
        INSERT INTO bench_pairs (concept_level, place_level, concept_id, place_path) VALUES (L, P, anc, pref)
        ON CONFLICT DO NOTHING;
        IF FOUND THEN i := i + 1; END IF;
      END LOOP;
    END LOOP;
  END LOOP;
END $$;

UPDATE bench_pairs bp SET
  n_desc = (SELECT count(*) FROM concept_closure WHERE ancestor_id = bp.concept_id),
  n_members = (SELECT count(DISTINCT ec.entry_id)
               FROM concept_closure cl JOIN ec ON ec.concept_id = cl.descendant_id AND ec.published
               WHERE cl.ancestor_id = bp.concept_id
                 AND (bp.place_path = '' OR ec.place_path = bp.place_path OR ec.place_path LIKE bp.place_path || '.%'));
ANALYZE bench_pairs;
SELECT concept_level, place_level, count(*) AS pairs, min(n_members) AS min_members, percentile_disc(0.5) WITHIN GROUP (ORDER BY n_members) AS median_members, max(n_members) AS max_members
FROM bench_pairs GROUP BY 1,2 ORDER BY 1,2;
SELECT CASE WHEN n_members < 100 THEN 'a: <100' WHEN n_members < 1000 THEN 'b: 100-999' WHEN n_members < 10000 THEN 'c: 1k-9.9k'
            WHEN n_members < 100000 THEN 'd: 10k-99k' ELSE 'e: >=100k' END AS bucket, count(*) AS pairs, round(avg(n_desc)) AS avg_descendant_nodes
FROM bench_pairs GROUP BY 1 ORDER BY 1;
