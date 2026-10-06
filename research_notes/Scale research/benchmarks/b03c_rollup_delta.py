"""B03c: roll-ups without loading entries in Python. Needs b03a data in bench_django (1,000,000 entries).

Builds, next to the real Django tables (nothing in them is changed except the mutation workload on entries):
  rc            roll-up cells with integer counters (fillfactor 70)        -> replaces analytics_rollupcell.by_level JSON
  ers           "entry roll-up state": what each entry contributed last time -> makes the delta exact and idempotent
  rc_dirty      queue of changed entries (the outbox table in the real design)
  concept_anc   ancestor array per concept (stands in for a stored Concept.path)

Measures: exact recount as SQL (one stage vs two stage) for all 1M entries; delta batches of 1 / 100 / 1,000 / 10,000 changed
entries; 4 parallel consumers; equality of delta result and exact recount after a mixed workload; a clock jump handled by the
expiry sweeper; HOT update ratio.

Run: .venv/bin/python "research_notes/Scale research/benchmarks/b03c_rollup_delta.py"
"""

import random
import statistics
import sys
import threading
import time
from datetime import datetime, timedelta, timezone

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from common import Timer, connect, pctl  # noqa: E402

import psycopg  # noqa: E402

DB = "bench_django"
MAX_ID = 0

DDL = """
DROP TABLE IF EXISTS rc, ers, rc_dirty, concept_anc, rc_exact CASCADE;
CREATE OR REPLACE FUNCTION place_paths(p text) RETURNS text[] LANGUAGE sql IMMUTABLE PARALLEL SAFE AS $$
  SELECT ARRAY['']::text[] || ARRAY(SELECT array_to_string((string_to_array(p, '.'))[1:i], '.')
                                      FROM generate_series(1, cardinality(string_to_array(p, '.'))) i)
$$;
CREATE TABLE concept_anc (concept_id bigint PRIMARY KEY, anc bigint[] NOT NULL);
INSERT INTO concept_anc
WITH RECURSIVE t(id, anc) AS (
  SELECT id, ARRAY[id] FROM taxonomy_concept
  UNION ALL SELECT t.id, t.anc || c.parent_id FROM t JOIN taxonomy_concept c ON c.id = t.anc[cardinality(t.anc)] WHERE c.parent_id IS NOT NULL)
SELECT DISTINCT ON (id) id, anc FROM t ORDER BY id, cardinality(anc) DESC;
CREATE TABLE rc (
  country_code varchar(2) NOT NULL, place_path varchar(500) NOT NULL, concept_id bigint NOT NULL,
  total int NOT NULL DEFAULT 0, published int NOT NULL DEFAULT 0,
  lv_surveyor int NOT NULL DEFAULT 0, lv_owner int NOT NULL DEFAULT 0, lv_ai int NOT NULL DEFAULT 0, lv_none int NOT NULL DEFAULT 0,
  verified_12m int NOT NULL DEFAULT 0, with_contact int NOT NULL DEFAULT 0, updated_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (country_code, place_path, concept_id)) WITH (fillfactor = 70);
CREATE TABLE ers (
  entry_id bigint PRIMARY KEY, country_code varchar(2) NOT NULL, place_path varchar(500) NOT NULL, concept_id bigint NOT NULL,
  counted boolean NOT NULL, published boolean NOT NULL, lv smallint NOT NULL, v12 boolean NOT NULL, contact boolean NOT NULL) WITH (fillfactor = 80);
CREATE TABLE rc_dirty (entry_id bigint PRIMARY KEY);
"""

NEWST = """
SELECT e.id AS entry_id, e.country_code, e.place_path, e.primary_concept_id AS concept_id,
       (e.deleted_at IS NULL AND e.merged_into_id IS NULL) AS counted,
       (e.publish_state = 'published') AS published,
       COALESCE((SELECT min(CASE v.level WHEN 'surveyor' THEN 1 WHEN 'owner' THEN 2 WHEN 'ai' THEN 3 END)
                   FROM entries_verificationcurrent v
                  WHERE v.entry_id = e.id AND v.state = 'verified' AND v.expires_at > %(now)s), 0)::smallint AS lv,
       COALESCE(e.last_verified_at > %(now)s - interval '365 days', false) AS v12,
       EXISTS (SELECT 1 FROM entries_contact c WHERE c.entry_id = e.id) AS contact
  FROM entries_entry e
"""

CONTRIB = """
  sign * (counted)::int AS total,
  sign * (counted AND published)::int AS published,
  sign * (counted AND published AND lv = 1)::int AS lv_surveyor,
  sign * (counted AND published AND lv = 2)::int AS lv_owner,
  sign * (counted AND published AND lv = 3)::int AS lv_ai,
  sign * (counted AND published AND lv = 0)::int AS lv_none,
  sign * (counted AND published AND v12)::int AS verified_12m,
  sign * (counted AND published AND contact)::int AS with_contact
"""

SUMS = """sum(total)::int AS total, sum(published)::int AS published, sum(lv_surveyor)::int AS lv_surveyor, sum(lv_owner)::int AS lv_owner,
  sum(lv_ai)::int AS lv_ai, sum(lv_none)::int AS lv_none, sum(verified_12m)::int AS verified_12m, sum(with_contact)::int AS with_contact"""

APPLY = f"""
WITH b AS (
  DELETE FROM rc_dirty WHERE entry_id IN (SELECT entry_id FROM rc_dirty ORDER BY entry_id LIMIT %(n)s FOR UPDATE SKIP LOCKED)
  RETURNING entry_id),
new AS ({NEWST} WHERE e.id IN (SELECT entry_id FROM b)),
signed AS (
  SELECT country_code, place_path, concept_id, {CONTRIB.replace('sign', '1')} FROM new
  UNION ALL
  SELECT country_code, place_path, concept_id, {CONTRIB.replace('sign', '(-1)')} FROM ers WHERE entry_id IN (SELECT entry_id FROM b)),
cells AS (
  SELECT s.country_code, pp AS place_path, c AS concept_id, {SUMS}
    FROM signed s JOIN concept_anc a ON a.concept_id = s.concept_id
   CROSS JOIN LATERAL unnest(place_paths(s.place_path)) pp CROSS JOIN LATERAL unnest(a.anc) c
   GROUP BY 1, 2, 3
  HAVING sum(abs(total)) + sum(abs(published)) + sum(abs(lv_surveyor)) + sum(abs(lv_owner)) + sum(abs(lv_ai)) + sum(abs(lv_none))
         + sum(abs(verified_12m)) + sum(abs(with_contact)) > 0),
up AS (
  INSERT INTO rc (country_code, place_path, concept_id, total, published, lv_surveyor, lv_owner, lv_ai, lv_none, verified_12m, with_contact, updated_at)
  SELECT country_code, place_path, concept_id, total, published, lv_surveyor, lv_owner, lv_ai, lv_none, verified_12m, with_contact, %(now)s
    FROM cells ORDER BY country_code, place_path, concept_id
  ON CONFLICT (country_code, place_path, concept_id) DO UPDATE SET
    total = rc.total + EXCLUDED.total, published = rc.published + EXCLUDED.published,
    lv_surveyor = rc.lv_surveyor + EXCLUDED.lv_surveyor, lv_owner = rc.lv_owner + EXCLUDED.lv_owner, lv_ai = rc.lv_ai + EXCLUDED.lv_ai,
    lv_none = rc.lv_none + EXCLUDED.lv_none, verified_12m = rc.verified_12m + EXCLUDED.verified_12m,
    with_contact = rc.with_contact + EXCLUDED.with_contact, updated_at = EXCLUDED.updated_at
  RETURNING 1),
st AS (
  INSERT INTO ers SELECT entry_id, country_code, place_path, concept_id, counted, published, lv, v12, contact FROM new
  ON CONFLICT (entry_id) DO UPDATE SET country_code = EXCLUDED.country_code, place_path = EXCLUDED.place_path,
    concept_id = EXCLUDED.concept_id, counted = EXCLUDED.counted, published = EXCLUDED.published, lv = EXCLUDED.lv,
    v12 = EXCLUDED.v12, contact = EXCLUDED.contact
  RETURNING 1),
gone AS (DELETE FROM ers WHERE entry_id IN (SELECT entry_id FROM b) AND entry_id NOT IN (SELECT entry_id FROM new) RETURNING 1)
SELECT (SELECT count(*) FROM b), (SELECT count(*) FROM up), (SELECT count(*) FROM st), (SELECT count(*) FROM gone)
"""

LEAF_SQL = f"""
WITH st AS ({NEWST} WHERE e.deleted_at IS NULL AND e.merged_into_id IS NULL),
leaf AS (
  SELECT country_code, place_path, concept_id, count(*)::int AS total, (count(*) FILTER (WHERE published))::int AS published,
         (count(*) FILTER (WHERE published AND lv = 1))::int AS lv_surveyor, (count(*) FILTER (WHERE published AND lv = 2))::int AS lv_owner,
         (count(*) FILTER (WHERE published AND lv = 3))::int AS lv_ai, (count(*) FILTER (WHERE published AND lv = 0))::int AS lv_none,
         (count(*) FILTER (WHERE published AND v12))::int AS verified_12m, (count(*) FILTER (WHERE published AND contact))::int AS with_contact
    FROM st GROUP BY 1, 2, 3)
INSERT INTO rc_exact (country_code, place_path, concept_id, total, published, lv_surveyor, lv_owner, lv_ai, lv_none, verified_12m, with_contact)
SELECT l.country_code, pp, c, {SUMS.replace('sum(total)', 'sum(l.total)').replace('sum(published)', 'sum(l.published)').replace('sum(lv_surveyor)', 'sum(l.lv_surveyor)').replace('sum(lv_owner)', 'sum(l.lv_owner)').replace('sum(lv_ai)', 'sum(l.lv_ai)').replace('sum(lv_none)', 'sum(l.lv_none)').replace('sum(verified_12m)', 'sum(l.verified_12m)').replace('sum(with_contact)', 'sum(l.with_contact)')}
  FROM leaf l JOIN concept_anc a ON a.concept_id = l.concept_id
 CROSS JOIN LATERAL unnest(place_paths(l.place_path)) pp CROSS JOIN LATERAL unnest(a.anc) c
 GROUP BY 1, 2, 3
"""

ONE_STAGE_SQL = f"""
WITH st AS ({NEWST} WHERE e.deleted_at IS NULL AND e.merged_into_id IS NULL),
signed AS (SELECT country_code, place_path, concept_id, {CONTRIB.replace('sign', '1')} FROM st)
INSERT INTO rc_exact (country_code, place_path, concept_id, total, published, lv_surveyor, lv_owner, lv_ai, lv_none, verified_12m, with_contact)
SELECT s.country_code, pp, c, {SUMS}
  FROM signed s JOIN concept_anc a ON a.concept_id = s.concept_id
 CROSS JOIN LATERAL unnest(place_paths(s.place_path)) pp CROSS JOIN LATERAL unnest(a.anc) c
 GROUP BY 1, 2, 3
"""

DIFF = """
SELECT count(*) FROM (
  (SELECT country_code, place_path, concept_id, total, published, lv_surveyor, lv_owner, lv_ai, lv_none, verified_12m, with_contact FROM rc WHERE total <> 0 OR published <> 0
   EXCEPT SELECT country_code, place_path, concept_id, total, published, lv_surveyor, lv_owner, lv_ai, lv_none, verified_12m, with_contact FROM rc_exact)
  UNION ALL
  (SELECT country_code, place_path, concept_id, total, published, lv_surveyor, lv_owner, lv_ai, lv_none, verified_12m, with_contact FROM rc_exact
   EXCEPT SELECT country_code, place_path, concept_id, total, published, lv_surveyor, lv_owner, lv_ai, lv_none, verified_12m, with_contact FROM rc WHERE total <> 0 OR published <> 0)
) d
"""


def exact(c, now, sql=LEAF_SQL):
    c.execute("DROP TABLE IF EXISTS rc_exact")
    c.execute("CREATE UNLOGGED TABLE rc_exact (LIKE rc INCLUDING DEFAULTS)")
    c.execute("ALTER TABLE rc_exact DROP COLUMN updated_at")
    with Timer() as t:
        c.execute(sql, {"now": now})
    return t.s


def mutate(c, rng, n, now):
    """Mixed workload on n entries; every change also queues the entry (the app or a trigger does this in the same tx)."""
    global MAX_ID
    if not MAX_ID:
        MAX_ID = c.execute("SELECT max(id) FROM entries_entry").fetchone()[0]
    ids = rng.sample(range(1, MAX_ID + 1), n)
    parts = [ids[i::6] for i in range(6)]
    with c.transaction():
        c.execute("UPDATE entries_entry SET publish_state = 'published' WHERE id = ANY(%s)", (parts[0],))
        c.execute("INSERT INTO entries_verificationcurrent (field_group, level, state, verified_at, expires_at, method, actor_display, entry_id) "
                  "SELECT 'basics', 'surveyor', 'verified', %s, %s, 'visit', '', x FROM unnest(%s::bigint[]) x ON CONFLICT (entry_id, field_group, level) DO UPDATE SET expires_at = EXCLUDED.expires_at, state = 'verified'",
                  (now, now + timedelta(days=200), parts[1]))
        c.execute("INSERT INTO entries_contact (country_code, kind, value_enc, value_hash, label, preferred_hours, relay_only, optin_state, entry_id) "
                  "SELECT 'XX', 'phone', 'enc', md5(x::text || 'm'), '', '', true, 'none', x FROM unnest(%s::bigint[]) x", (parts[2],))
        c.execute("UPDATE entries_entry SET deleted_at = %s WHERE id = ANY(%s)", (now, parts[3]))
        c.execute("UPDATE entries_entry SET place_path = replace(place_path, '.c1', '.c2'), place_id = place_id + 1 WHERE id = ANY(%s) AND place_path LIKE '%%.c1'", (parts[4],))
        c.execute("UPDATE entries_entry SET primary_concept_id = 1101 + (primary_concept_id - 1100) %% 20 WHERE id = ANY(%s)", (parts[5],))
        c.execute("INSERT INTO rc_dirty SELECT x FROM unnest(%s::bigint[]) x ON CONFLICT DO NOTHING", (ids,))
    return len(ids)


def drain(c, batch, now):
    total = 0
    lat = []
    while True:
        t = time.perf_counter()
        n = c.execute(APPLY, {"n": batch, "now": now}).fetchone()[0]
        if not n:
            break
        lat.append(time.perf_counter() - t)
        total += n
    return total, lat


def main():
    rng = random.Random(11)
    c = connect(DB)
    now = datetime.now(timezone.utc)
    n_entries = c.execute("SELECT count(*) FROM entries_entry").fetchone()[0]
    print(f"entries in table: {n_entries:,}")
    c.execute(DDL)

    # 1. initial population = the first exact recount, both ways
    t_leaf = exact(c, now, LEAF_SQL)
    cells = c.execute("SELECT count(*) FROM rc_exact").fetchone()[0]
    print(f"exact recount, two-stage SQL (leaf GROUP BY then expand ancestors): {t_leaf:.1f}s for {n_entries:,} entries -> {cells:,} cells")
    t_one = exact(c, now, ONE_STAGE_SQL)
    print(f"exact recount, one-stage SQL (every entry x 4 place paths x 3 concepts): {t_one:.1f}s -> {c.execute('SELECT count(*) FROM rc_exact').fetchone()[0]:,} cells")
    exact(c, now, LEAF_SQL)
    with Timer() as t:
        c.execute("INSERT INTO rc SELECT country_code, place_path, concept_id, total, published, lv_surveyor, lv_owner, lv_ai, lv_none, verified_12m, with_contact, %s FROM rc_exact", (now,))
        c.execute("INSERT INTO ers SELECT entry_id, country_code, place_path, concept_id, counted, published, lv, v12, contact FROM (" + NEWST + ") x", {"now": now})
    print(f"initial fill of rc and ers: {t.s:.1f}s")
    c.execute("ANALYZE rc")
    c.execute("ANALYZE ers")
    print("diff rc vs exact after initial fill:", c.execute(DIFF).fetchone()[0])
    root = c.execute("SELECT total, published, lv_surveyor, lv_owner, lv_ai, lv_none, verified_12m, with_contact FROM rc WHERE country_code='PK' AND place_path='' AND concept_id=1000").fetchone()
    print("PK / world path / root concept cell:", root)

    # 2. delta batches
    print("== delta apply, one consumer ==")
    for batch_changes in (1, 100, 1000, 10000):
        reps = 200 if batch_changes == 1 else (20 if batch_changes == 100 else (5 if batch_changes == 1000 else 2))
        lats = []
        for _ in range(reps):
            mutate(c, rng, batch_changes, now)
            t = time.perf_counter()
            drain(c, batch_changes, now)
            lats.append(time.perf_counter() - t)
        per_entry = statistics.median(lats) / batch_changes
        print(f"batch of {batch_changes:>6,} changed entries: median {statistics.median(lats) * 1000:9.1f} ms/batch  "
              f"p95 {pctl(lats, 95) * 1000:9.1f} ms  = {per_entry * 1000:.3f} ms per entry  ({1 / per_entry:,.0f} entries/s)", flush=True)
    exact(c, now, LEAF_SQL)
    print("diff rc vs exact after single-consumer workload (must be 0):", c.execute(DIFF).fetchone()[0])

    # 3. four consumers in parallel, hot cells shared
    print("== 4 parallel consumers (SKIP LOCKED), 20,000 changed entries ==")
    mutate(c, rng, 10000, now)
    mutate(c, rng, 10000, now)
    total_dirty = c.execute("SELECT count(*) FROM rc_dirty").fetchone()[0]
    res, errs = [], []

    def consumer():
        cc = connect(DB)
        try:
            n, _ = drain(cc, 1000, now)
            res.append(n)
        except psycopg.Error as e:
            errs.append(type(e).__name__)
        finally:
            cc.close()

    t0 = time.perf_counter()
    ths = [threading.Thread(target=consumer) for _ in range(4)]
    [t.start() for t in ths]
    [t.join() for t in ths]
    wall = time.perf_counter() - t0
    print(f"queued={total_dirty:,} processed={sum(res):,} in {wall:.2f}s ({sum(res) / wall:,.0f} entries/s) errors={errs}")
    exact(c, now, LEAF_SQL)
    print("diff after parallel consumers (must be 0):", c.execute(DIFF).fetchone()[0])

    # 4. clock jump: expiry sweeper
    print("== clock moves 40 days: sweeper finds entries whose answer changes ==")
    now2 = now + timedelta(days=40)
    for with_index in (False, True):
        if with_index:
            with Timer() as ti:
                c.execute("CREATE INDEX IF NOT EXISTS vc_expires_idx ON entries_verificationcurrent (expires_at) WHERE state = 'verified'")
                c.execute("CREATE INDEX IF NOT EXISTS entry_last_verified_idx ON entries_entry (last_verified_at) WHERE last_verified_at IS NOT NULL")
            print(f"  built the two sweeper indexes in {ti.s:.1f}s")
        with Timer() as t:
            c.execute("INSERT INTO rc_dirty SELECT entry_id FROM entries_verificationcurrent WHERE state = 'verified' AND expires_at > %s AND expires_at <= %s ON CONFLICT DO NOTHING", (now, now2))
            c.execute("INSERT INTO rc_dirty SELECT id FROM entries_entry WHERE last_verified_at > %s - interval '365 days' AND last_verified_at <= %s - interval '365 days' ON CONFLICT DO NOTHING", (now, now2))
        q = c.execute("SELECT count(*) FROM rc_dirty").fetchone()[0]
        print(f"  sweeper query {'with' if with_index else 'without'} indexes: {t.s * 1000:.0f} ms, {q:,} entries queued")
        if not with_index:
            c.execute("TRUNCATE rc_dirty")
    n, lat = drain(c, 5000, now2)
    print(f"  applied {n:,} sweeper entries in {sum(lat):.1f}s")
    exact(c, now2, LEAF_SQL)
    print("diff rc vs exact at now+40d (must be 0):", c.execute(DIFF).fetchone()[0])

    # 5. bloat / HOT
    r = c.execute("SELECT n_tup_upd, n_tup_hot_upd, n_dead_tup, pg_size_pretty(pg_relation_size('rc')) FROM pg_stat_user_tables WHERE relname='rc'").fetchone()
    print(f"rc: updates={r[0]:,} hot={r[1]:,} ({100 * r[1] / max(r[0], 1):.0f}%) dead={r[2]:,} size={r[3]}")
    c.execute("DROP TABLE IF EXISTS rc_exact")


if __name__ == "__main__":
    main()
