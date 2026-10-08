"""B04: 5,000,000 entry-like rows, three layouts, scratch database bench_part.

  flat   one table, PK(id), UNIQUE(uid), the same secondary indexes the Entry model has
  p40    PARTITION BY LIST (country_code): 40 country partitions + DEFAULT; PK(country_code, id), UNIQUE(country_code, uid)
  p250   same with 250 country partitions (every ISO country) + DEFAULT

Country weights are skewed (PK 25%, IN 20%, BD 10%, the rest long tail over 37 countries; the 210 extra countries in p250 hold
no rows, they test planner and catalog cost of many empty partitions).

Measures: load time; index build time; single-row INSERT rate (8 writers); list-page queries with and without the country;
planning time; whole-table VACUUM; ATTACH PARTITION with and without a prepared CHECK; DEFAULT partition trap; composite FK
across a partitioned parent; identity versus sequence default on a partitioned table; CREATE INDEX CONCURRENTLY on the parent.

Run: .venv/bin/python "research_notes/Scale research/benchmarks/b04_partition_5m.py" [rows]
"""

import multiprocessing as mp
import random
import re
import statistics
import sys
import time

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from common import Timer, connect, drop_db, make_db, pctl  # noqa: E402

import psycopg  # noqa: E402

DB = "bench_part"
TOP = [("PK", 25), ("IN", 20), ("BD", 10)]
TAIL = ["LK", "NP", "AE", "SA", "TR", "EG", "NG", "KE", "ZA", "GB", "DE", "FR", "US", "CA", "BR", "ID", "MY", "TH", "VN", "PH",
        "MX", "CO", "AR", "CL", "PE", "MA", "TN", "DZ", "GH", "TZ", "UG", "ET", "JO", "LB", "OM", "QA", "KW"]  # 37
COUNTRIES40 = [c for c, _ in TOP] + TAIL
ALL250 = COUNTRIES40 + [a + b for a in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" for b in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if a + b not in COUNTRIES40][:210]


def cols(partitioned):
    pk = "PRIMARY KEY (country_code, id)" if partitioned else "PRIMARY KEY (id)"
    return f"""(
  id bigint NOT NULL, uid char(26) NOT NULL, country_code varchar(2) NOT NULL, place_id bigint NOT NULL, place_path varchar(500) NOT NULL,
  primary_concept_id bigint NOT NULL, publish_state varchar(12) NOT NULL, claim_state varchar(10) NOT NULL DEFAULT 'unclaimed',
  name varchar(250) NOT NULL, name_fold varchar(250) NOT NULL, address_text varchar(400) NOT NULL DEFAULT '',
  description text NOT NULL DEFAULT '', website varchar(200) NOT NULL DEFAULT '', addons jsonb NOT NULL DEFAULT '{{}}',
  lat numeric(9,6), lon numeric(9,6), created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
  deleted_at timestamptz, {pk})"""


INDEXES = [
    ("uid", "(uid)", True),
    ("list_query", "(country_code, place_path, primary_concept_id, publish_state)", False),
    ("claim", "(country_code, claim_state)", False),
    ("name_fold", "(name_fold)", False),
    ("place", "(place_id)", False),
    ("concept", "(primary_concept_id)", False),
]


def weights(countries):
    w = {c: p for c, p in TOP}
    rest = (100 - sum(w.values())) / len(TAIL)
    return {c: w.get(c, rest if c in TAIL else 0) for c in countries}


def create_layout(c, name, countries):
    part = name != "flat"
    c.execute(f"CREATE TABLE {name} {cols(part)}" + (" PARTITION BY LIST (country_code)" if part else ""))
    c.execute(f"CREATE SEQUENCE {name}_seq CACHE 100")
    c.execute(f"ALTER TABLE {name} ALTER COLUMN id SET DEFAULT nextval('{name}_seq')")
    if part:
        for cc in countries:
            c.execute(f"CREATE TABLE {name}_{cc.lower()} PARTITION OF {name} FOR VALUES IN ('{cc}')")
        c.execute(f"CREATE TABLE {name}_default PARTITION OF {name} DEFAULT")


def load(c, name, n, countries):
    """INSERT ... SELECT in one statement per country (the flat table gets the same statements), PK index only."""
    w = weights(countries)
    base = 0
    with Timer() as t:
        for cc in countries:
            k = int(n * w[cc] / 100)
            if k == 0:
                continue
            c.execute(
                f"""INSERT INTO {name} (id, uid, country_code, place_id, place_path, primary_concept_id, publish_state, name, name_fold,
   address_text, description, website, addons, lat, lon, deleted_at)
SELECT nextval('{name}_seq'), 'E' || lpad(({base} + g)::text, 25, '0'), %(cc)s, 100 + g % 20,
       lower(%(cc)s) || '.p' || (1 + g % 4) || '.c' || (1 + (g / 4) % 5), 1100 + 1 + g % 20,
       CASE WHEN g % 10 < 7 THEN 'published' WHEN g % 10 < 9 THEN 'draft' ELSE 'review' END,
       'Entry ' || %(cc)s || ' ' || g, 'entry ' || lower(%(cc)s) || ' ' || md5(g::text),
       repeat('x', 40) || g, repeat('d', 100), 'https://example.org/' || g, '{{"k": 1}}'::jsonb,
       24 + (g % 1000) / 1000.0, 67 + (g % 1000) / 1000.0, CASE WHEN g % 100 = 0 THEN now() ELSE NULL END
  FROM generate_series(1, %(k)s) g""",
                {"cc": cc, "k": k},
            )
            base += k
    return t.s, base


def build_indexes(c, name):
    out = {}
    for iname, cols_, uniq in INDEXES:
        if name != "flat" and iname == "uid":
            cols_ = "(country_code, uid)"
        with Timer() as t:
            c.execute(f"CREATE {'UNIQUE ' if uniq else ''}INDEX {name}_{iname} ON {name} {cols_}")
        out[iname] = t.s
    return out


def insert_worker(name, countries, idx, duration, q, start_at):
    conn = connect(DB)
    rng = random.Random(100 + idx)
    w = weights(countries)
    cs = [c for c in countries if w[c] > 0]
    ws = [w[c] for c in cs]
    lat = []
    while time.time() < start_at:
        time.sleep(0.001)
    end = time.time() + duration
    i = 0
    while time.time() < end:
        cc = rng.choices(cs, ws)[0]
        t = time.perf_counter()
        conn.execute(
            f"INSERT INTO {name} (id, uid, country_code, place_id, place_path, primary_concept_id, publish_state, name, name_fold) "
            f"VALUES (nextval('{name}_seq'), %s, %s, 101, %s, 1101, 'draft', %s, %s)",
            (f"N{idx:02d}{i:022d}", cc, f"{cc.lower()}.p1.c1", f"New {i}", f"new {i}"),
        )
        lat.append(time.perf_counter() - t)
        i += 1
    q.put(lat)
    conn.close()


def run_inserts(name, countries, workers, duration):
    ctx = mp.get_context("spawn")
    q = ctx.Queue()
    start_at = time.time() + 2
    ps = [ctx.Process(target=insert_worker, args=(name, countries, i, duration, q, start_at)) for i in range(workers)]
    [p.start() for p in ps]
    lats = [q.get() for _ in ps]
    [p.join() for p in ps]
    flat = [x for l in lats for x in l]
    return len(flat) / duration, pctl(flat, 50) * 1000, pctl(flat, 99) * 1000


def explain_times(c, sql, params, reps=60):
    """Returns (median planning ms, median execution ms, plan text of the last run)."""
    pl, ex, txt = [], [], ""
    for _ in range(reps):
        rows = c.execute("EXPLAIN (ANALYZE, SUMMARY, TIMING OFF) " + sql, params).fetchall()
        txt = "\n".join(r[0] for r in rows)
        pl.append(float(re.search(r"Planning Time: ([\d.]+)", txt).group(1)))
        ex.append(float(re.search(r"Execution Time: ([\d.]+)", txt).group(1)))
    return statistics.median(pl), statistics.median(ex), txt


QUERIES = {
    "list page (country, city, concept, published, order by name, 25)": (
        "SELECT id, name FROM {t} WHERE country_code = %(cc)s AND place_path = %(pp)s AND primary_concept_id = %(cid)s AND publish_state = 'published' ORDER BY name_fold LIMIT 25"),
    "city and below (country, place_path prefix, concept in 5, published, limit 25)": (
        "SELECT id, name FROM {t} WHERE country_code = %(cc)s AND place_path LIKE %(pre)s AND primary_concept_id = ANY(%(cids)s) AND publish_state = 'published' ORDER BY name_fold LIMIT 25"),
    "country count (live)": "SELECT count(*) FROM {t} WHERE country_code = %(cc)s AND deleted_at IS NULL",
    "uid lookup WITHOUT country": "SELECT id FROM {t} WHERE uid = %(uid)s",
    "uid lookup WITH country": "SELECT id FROM {t} WHERE country_code = %(cc)s AND uid = %(uid)s",
    "global list (no country, concept, published, order by name, 25)": (
        "SELECT id, name FROM {t} WHERE primary_concept_id = %(cid)s AND publish_state = 'published' ORDER BY name_fold LIMIT 25"),
}


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5_000_000
    make_db(DB)
    c = connect(DB)
    layouts = {"flat": [], "p40": COUNTRIES40, "p250": ALL250}
    report = {}
    for name, countries in layouts.items():
        print(f"\n=== {name} ===", flush=True)
        create_layout(c, name, countries)
        t_load, rows = load(c, name, n, COUNTRIES40)
        print(f"load {rows:,} rows (PK only): {t_load:.1f}s = {rows / t_load:,.0f} rows/s", flush=True)
        idx = build_indexes(c, name)
        print("index builds (s):", {k: round(v, 1) for k, v in idx.items()}, "total", round(sum(idx.values()), 1), flush=True)
        with Timer() as t:
            c.execute(f"ANALYZE {name}")
        size = c.execute(f"SELECT pg_size_pretty(pg_total_relation_size('{name}')), pg_size_pretty(sum(pg_indexes_size(c.oid)))  FROM pg_class c WHERE relkind IN ('r','p') AND relname = '{name}'").fetchone()
        print(f"analyze {t.s:.1f}s; total size incl. indexes {size[0]}", flush=True)
        report[name] = {"load": t_load, "idx": sum(idx.values())}

    print("\n=== single-row INSERT rate, 8 writers, 8 s each (writers pick countries by the same weights) ===")
    for name, countries in layouts.items():
        countries = COUNTRIES40
        rate, p50, p99 = run_inserts(name, countries, 8, 8)
        print(f"{name:5s} {rate:,.0f} inserts/s  p50={p50:.2f}ms p99={p99:.2f}ms", flush=True)
    for name, countries in layouts.items():
        rate, p50, p99 = run_inserts(name, COUNTRIES40, 1, 6)
        print(f"{name:5s} 1 writer: {rate:,.0f} inserts/s  p50={p50:.2f}ms p99={p99:.2f}ms", flush=True)

    print("\n=== queries (median of 60 EXPLAIN ANALYZE runs, warm cache) ===")
    uid_pk = c.execute("SELECT uid FROM flat WHERE country_code='PK' AND id > 100000 LIMIT 1").fetchone()[0]
    uid_tr = c.execute("SELECT uid FROM flat WHERE country_code='TR' LIMIT 1").fetchone()[0]
    for qn, sql in QUERIES.items():
        for cc, uid in (("PK", uid_pk), ("TR", uid_tr)):
            if "WITH country" in qn and cc == "TR":
                continue
            line = f"{qn} [{cc}]: "
            for name in layouts:
                params = {"cc": cc, "pp": f"{cc.lower()}.p1.c2", "cid": 1105, "pre": f"{cc.lower()}.p1.%", "cids": [1101, 1102, 1103, 1104, 1105], "uid": uid}
                pl, ex, txt = explain_times(c, sql.format(t=name), params)
                line += f"{name}: plan {pl:.2f} + exec {ex:.2f} ms | "
            print(line, flush=True)
            if cc == "PK" and qn.startswith("global"):
                pl, ex, txt = explain_times(c, sql.format(t="p40"), params, 3)
                print("   p40 global-list plan top:", txt.splitlines()[0:3])

    print("\n=== maintenance ===")
    for name in layouts:
        c.execute(f"UPDATE {name} SET updated_at = now() WHERE id % 50 = 0")
        with Timer() as t:
            c.execute(f"VACUUM (ANALYZE) {name}")
        print(f"{name}: UPDATE 2% then VACUUM (ANALYZE) whole table {t.s:.1f}s", flush=True)
    with Timer() as t:
        c.execute("VACUUM (ANALYZE) p40_pk")
    print(f"p40_pk alone (25% of rows): VACUUM {t.s:.1f}s")
    with Timer() as t:
        c.execute("VACUUM (ANALYZE) p40_ke")
    print(f"p40_ke alone (~1.5% of rows): VACUUM {t.s:.2f}s")

    print("\n=== ATTACH / DEFAULT partition behaviour (p40) ===")
    # new country 'ZZ' prepared offline as a standalone table with the same indexes and a CHECK
    c.execute("CREATE TABLE p40_zz (LIKE p40 INCLUDING DEFAULTS INCLUDING GENERATED)")
    c.execute("INSERT INTO p40_zz (id, uid, country_code, place_id, place_path, primary_concept_id, publish_state, name, name_fold) "
              "SELECT nextval('p40_seq'), 'Z' || lpad(g::text, 25, '0'), 'ZZ', 1, 'zz.p1.c1', 1101, 'draft', 'z' || g, 'z' || g FROM generate_series(1, 200000) g")
    c.execute("ALTER TABLE p40_zz ADD PRIMARY KEY (country_code, id)")
    c.execute("CREATE UNIQUE INDEX p40_zz_uid ON p40_zz (country_code, uid)")
    for iname, cols_, uniq in INDEXES[1:]:
        c.execute(f"CREATE INDEX p40_zz_{iname} ON p40_zz {cols_}")
    with Timer() as t:
        c.execute("ALTER TABLE p40 ATTACH PARTITION p40_zz FOR VALUES IN ('ZZ')")
    print(f"ATTACH 200,000-row partition with NO check constraint (full scan, default partition also checked): {t.s * 1000:.0f} ms")
    c.execute("ALTER TABLE p40 DETACH PARTITION p40_zz")
    c.execute("ALTER TABLE p40_zz ADD CONSTRAINT zz_ck CHECK (country_code = 'ZZ') NOT VALID")
    c.execute("ALTER TABLE p40_zz VALIDATE CONSTRAINT zz_ck")
    with Timer() as t:
        c.execute("ALTER TABLE p40 ATTACH PARTITION p40_zz FOR VALUES IN ('ZZ')")
    print(f"ATTACH same partition with CHECK validated first: {t.s * 1000:.0f} ms (default partition has {c.execute('SELECT count(*) FROM p40_default').fetchone()[0]:,} rows)")
    with Timer() as t:
        c.execute("ALTER TABLE p40 DETACH PARTITION p40_zz CONCURRENTLY")
    print(f"DETACH PARTITION CONCURRENTLY: {t.s * 1000:.0f} ms")
    # the default partition trap: rows for a new country already sit in the DEFAULT partition
    c.execute("INSERT INTO p40 (id, uid, country_code, place_id, place_path, primary_concept_id, publish_state, name, name_fold) "
              "SELECT nextval('p40_seq'), 'Q' || lpad(g::text, 25, '0'), 'QQ', 1, 'qq.p1.c1', 1101, 'draft', 'q' || g, 'q' || g FROM generate_series(1, 300000) g")
    print(f"default partition rows now {c.execute('SELECT count(*) FROM p40_default').fetchone()[0]:,} (country QQ has no partition)")
    try:
        with Timer() as t:
            c.execute("CREATE TABLE p40_qq PARTITION OF p40 FOR VALUES IN ('QQ')")
        print("unexpected: created")
    except psycopg.Error as e:
        print(f"CREATE PARTITION for QQ while rows sit in DEFAULT fails after {t.s * 1000:.0f} ms: {type(e).__name__}: {str(e).splitlines()[0]}")
    # the safe way: detach default, move rows, attach
    with Timer() as t:
        with c.transaction():
            c.execute("CREATE TABLE p40_qq (LIKE p40 INCLUDING ALL)")
            c.execute("WITH m AS (DELETE FROM p40_default WHERE country_code = 'QQ' RETURNING *) INSERT INTO p40_qq SELECT * FROM m")
            c.execute("ALTER TABLE p40_qq ADD CONSTRAINT qq_ck CHECK (country_code = 'QQ')")
            c.execute("ALTER TABLE p40 ATTACH PARTITION p40_qq FOR VALUES IN ('QQ')")
    print(f"move 300,000 rows out of DEFAULT into a new partition in one transaction: {t.s:.1f}s (holds ACCESS EXCLUSIVE on the default partition meanwhile)")

    print("\n=== foreign keys against a partitioned parent ===")
    c.execute("CREATE TABLE child_bad (id bigserial PRIMARY KEY, entry_id bigint NOT NULL, country_code varchar(2) NOT NULL)")
    try:
        c.execute("ALTER TABLE child_bad ADD FOREIGN KEY (entry_id) REFERENCES p40 (id)")
        print("single-column FK to p40(id): OK (unexpected)")
    except psycopg.Error as e:
        print("single-column FK to p40(id):", str(e).splitlines()[0])
    c.execute("CREATE TABLE child_ok (id bigserial, entry_id bigint NOT NULL, country_code varchar(2) NOT NULL, note text, PRIMARY KEY (country_code, id)) PARTITION BY LIST (country_code)")
    c.execute("CREATE TABLE child_ok_pk PARTITION OF child_ok FOR VALUES IN ('PK')")
    c.execute("CREATE TABLE child_ok_def PARTITION OF child_ok DEFAULT")
    with Timer() as t:
        c.execute("ALTER TABLE child_ok ADD FOREIGN KEY (country_code, entry_id) REFERENCES p40 (country_code, id) ON DELETE CASCADE")
    print(f"composite FK (country_code, entry_id) -> p40(country_code, id): OK in {t.s * 1000:.0f} ms (empty child)")
    pid = c.execute("SELECT id FROM p40 WHERE country_code='PK' LIMIT 1").fetchone()[0]
    c.execute("INSERT INTO child_ok (entry_id, country_code, note) VALUES (%s, 'PK', 'hello')", (pid,))
    try:
        c.execute("INSERT INTO child_ok (entry_id, country_code, note) VALUES (%s, 'PK', 'orphan')", (-5,))
        print("orphan insert accepted (unexpected)")
    except psycopg.errors.ForeignKeyViolation:
        print("orphan insert rejected by the database: ForeignKeyViolation")
    # lock cost of the DB-level cascade when deleting a parent row
    c.execute("DELETE FROM p40 WHERE country_code='PK' AND id=%s", (pid,))
    print("cascade delete removed child rows:", c.execute("SELECT count(*) FROM child_ok WHERE entry_id=%s", (pid,)).fetchone()[0] == 0)

    print("\n=== identity column versus sequence default on a partitioned table ===")
    try:
        c.execute("CREATE TABLE ident (id bigint GENERATED BY DEFAULT AS IDENTITY, country_code varchar(2), PRIMARY KEY (country_code, id)) PARTITION BY LIST (country_code)")
        c.execute("CREATE TABLE ident_pk PARTITION OF ident FOR VALUES IN ('PK')")
        c.execute("INSERT INTO ident (country_code) VALUES ('PK') RETURNING id")
        print("identity column on partitioned parent: works in PostgreSQL 16, INSERT .. RETURNING id ok")
    except psycopg.Error as e:
        print("identity on partitioned parent:", str(e).splitlines()[0])

    print("\n=== CREATE INDEX CONCURRENTLY on the partitioned parent (what Django AddIndex(concurrent) emits) ===")
    try:
        c.execute("CREATE INDEX CONCURRENTLY p40_new_idx ON p40 (created_at)")
        print("unexpected success")
    except psycopg.Error as e:
        print("CONCURRENTLY on partitioned parent:", str(e).splitlines()[0])
    with Timer() as t:
        c.execute("CREATE INDEX p40_new_idx ON ONLY p40 (created_at)")
        parts = [r[0] for r in c.execute("SELECT c.relname FROM pg_inherits i JOIN pg_class c ON c.oid = i.inhrelid WHERE i.inhparent = 'p40'::regclass").fetchall()]
        for p in parts:
            c.execute(f"CREATE INDEX CONCURRENTLY {p}_created ON {p} (created_at)")
            c.execute(f"ALTER INDEX p40_new_idx ATTACH PARTITION {p}_created")
    valid = c.execute("SELECT indisvalid FROM pg_index WHERE indexrelid = 'p40_new_idx'::regclass").fetchone()[0]
    print(f"workaround (ONLY parent + CONCURRENTLY per partition + ATTACH) over {len(parts)} partitions: {t.s:.1f}s; parent index valid = {valid}")
    c.close()
    drop_db(DB)


if __name__ == "__main__":
    main()
