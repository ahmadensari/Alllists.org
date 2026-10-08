"""B10: what pg_partman 5.0.1 can and cannot do for AllLists, in scratch database bench_partman.

pg_partman is taken from the Ubuntu package (postgresql-16-partman 5.0.1) extracted with `dpkg -x`; its extension files are copied
into the PostgreSQL 16 extension directory for the test and REMOVED again at the end (PARTMAN_DIR = extraction directory).

Tests
  1  create_parent on a LIST-partitioned table (what we would want for countries)         -> expect refusal
  2  create_parent on a RANGE (monthly) table for an append-only log (audit / events)     -> works; premake, maintenance
  3  retention: drop or detach the oldest month versus DELETE of the same rows            -> time and bloat
  4  move 2,000,000 existing rows from an unpartitioned table in 50,000-row batches
Run: PARTMAN_DIR=<dir> .venv/bin/python b10_partman.py
"""

import glob
import os
import shutil
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from common import Timer, connect, drop_db, make_db  # noqa: E402

import psycopg  # noqa: E402

DB = "bench_partman"
SRC = os.environ["PARTMAN_DIR"]
EXT = "/usr/share/postgresql/16/extension"
LIB = "/usr/lib/postgresql/16/lib"


def install():
    files = []
    for f in glob.glob(f"{SRC}/usr/share/postgresql/16/extension/pg_partman*"):
        dst = f"{EXT}/{os.path.basename(f)}"
        if not os.path.exists(dst):
            shutil.copy(f, dst)
            files.append(dst)
    for f in glob.glob(f"{SRC}/usr/lib/postgresql/16/lib/pg_partman*.so"):
        dst = f"{LIB}/{os.path.basename(f)}"
        if not os.path.exists(dst):
            shutil.copy(f, dst)
            files.append(dst)
    return files


def main():
    files = install()
    print(f"temporarily installed {len(files)} extension files")
    try:
        make_db(DB)
        c = connect(DB)
        c.execute("CREATE SCHEMA partman")
        c.execute("CREATE EXTENSION pg_partman SCHEMA partman")
        print("extension version:", c.execute("SELECT extversion FROM pg_extension WHERE extname='pg_partman'").fetchone()[0])

        print("== 1. LIST partitioned table (country) ==")
        c.execute("CREATE TABLE entry_l (id bigint, country_code varchar(2) NOT NULL, name text, PRIMARY KEY (country_code, id)) PARTITION BY LIST (country_code)")
        try:
            c.execute("SELECT partman.create_parent('public.entry_l', 'country_code', '1 month')")
            print("create_parent on LIST table: accepted?!")
        except psycopg.Error as e:
            print("create_parent on a LIST-partitioned table:", str(e).strip().splitlines()[0])
        try:
            c.execute("SELECT partman.create_parent('public.entry_l', 'country_code', 'native')")
        except psycopg.Error as e:
            print("with interval 'native':", str(e).strip().splitlines()[0])

        print("== 2. monthly RANGE table for an append-only log ==")
        c.execute("""CREATE TABLE audit_p (id bigint GENERATED ALWAYS AS IDENTITY, ts timestamptz NOT NULL, country_code varchar(2) NOT NULL, action varchar(80) NOT NULL,
                     row_hash char(64) NOT NULL, payload jsonb NOT NULL DEFAULT '{}', PRIMARY KEY (ts, id)) PARTITION BY RANGE (ts)""")
        c.execute("CREATE TABLE audit_p_template (LIKE audit_p)")
        c.execute("CREATE INDEX audit_p_tpl_obj ON audit_p_template (country_code, action)")  # per-partition index via the template
        c.execute("SELECT partman.create_parent(p_parent_table => 'public.audit_p', p_control => 'ts', p_interval => '1 month', p_premake => 3, p_start_partition => (date_trunc('month', now()) - interval '5 months')::text, p_template_table => 'public.audit_p_template')")
        n = c.execute("SELECT count(*) FROM pg_inherits WHERE inhparent = 'public.audit_p'::regclass").fetchone()[0]
        print(f"create_parent: {n} partitions made (5 months back + current + premake 3 + default)")
        c.execute("INSERT INTO audit_p (ts, country_code, action, row_hash) SELECT now() - (g % 150 || ' days')::interval, 'PK', 'bench', md5(g::text) FROM generate_series(1, 2000000) g")
        sizes = c.execute("SELECT inhrelid::regclass::text, pg_size_pretty(pg_total_relation_size(inhrelid)) FROM pg_inherits WHERE inhparent = 'public.audit_p'::regclass ORDER BY 1 LIMIT 4").fetchall()
        print("2,000,000 rows inserted; first partitions:", sizes)
        print("indexes created on a partition by the template:", [r[0] for r in c.execute("SELECT indexname FROM pg_indexes WHERE tablename LIKE 'audit_p_p%' ORDER BY 1 LIMIT 3").fetchall()])
        c.execute("UPDATE partman.part_config SET premake = 3, retention = '3 months', retention_keep_table = false WHERE parent_table = 'public.audit_p'")
        with Timer() as t:
            c.execute("CALL partman.run_maintenance_proc()")
        n2 = c.execute("SELECT count(*) FROM pg_inherits WHERE inhparent = 'public.audit_p'::regclass").fetchone()[0]
        print(f"run_maintenance_proc (retention 3 months, drop): {t.s:.2f}s, partitions {n} -> {n2}; rows left {c.execute('SELECT count(*) FROM audit_p').fetchone()[0]:,}")

        print("== 3. retention by drop versus DELETE (same row count) ==")
        c.execute("CREATE TABLE audit_flat (LIKE audit_p INCLUDING ALL)")
        c.execute("INSERT INTO audit_flat SELECT * FROM audit_p")
        oldest = c.execute("SELECT min(ts) FROM audit_flat").fetchone()[0]
        cutoff = c.execute("SELECT date_trunc('month', min(ts)) + interval '1 month' FROM audit_flat").fetchone()[0]
        k = c.execute("SELECT count(*) FROM audit_flat WHERE ts < %s", (cutoff,)).fetchone()[0]
        with Timer() as t:
            c.execute("DELETE FROM audit_flat WHERE ts < %s", (cutoff,))
        dead = c.execute("SELECT n_dead_tup FROM pg_stat_user_tables WHERE relname = 'audit_flat'").fetchone()[0]
        print(f"DELETE {k:,} oldest rows from the flat table: {t.s:.2f}s, dead tuples left for vacuum: {dead:,}")
        first = c.execute("SELECT inhrelid::regclass::text FROM pg_inherits WHERE inhparent = 'public.audit_p'::regclass ORDER BY 1 LIMIT 1").fetchone()[0]
        kk = c.execute(f"SELECT count(*) FROM {first}").fetchone()[0]
        with Timer() as t:
            c.execute(f"ALTER TABLE audit_p DETACH PARTITION {first}")
            c.execute(f"DROP TABLE {first}")
        print(f"DETACH + DROP one partition of {kk:,} rows: {t.s * 1000:.0f} ms, no dead tuples")

        print("== 4. move existing rows into a partman-managed table ==")
        c.execute("DROP TABLE IF EXISTS audit_old CASCADE")
        c.execute("CREATE TABLE audit_old (id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY, ts timestamptz NOT NULL, country_code varchar(2) NOT NULL, action varchar(80) NOT NULL, row_hash char(64) NOT NULL, payload jsonb NOT NULL DEFAULT '{}')")
        c.execute("INSERT INTO audit_old (ts, country_code, action, row_hash) SELECT now() - (g % 300 || ' days')::interval, 'PK', 'bench', md5(g::text) FROM generate_series(1, 2000000) g")
        c.execute("ALTER TABLE audit_old DROP CONSTRAINT audit_old_pkey")
        c.execute("ALTER TABLE audit_old ADD PRIMARY KEY (ts, id)")
        c.execute("CREATE TABLE audit_n (LIKE audit_old INCLUDING DEFAULTS INCLUDING GENERATED, PRIMARY KEY (ts, id)) PARTITION BY RANGE (ts)")
        c.execute("SELECT partman.create_parent(p_parent_table => 'public.audit_n', p_control => 'ts', p_interval => '1 month', p_premake => 2, p_start_partition => (date_trunc('month', now()) - interval '10 months')::text)")
        with Timer() as t:
            moved = 0
            while True:
                r = c.execute("WITH m AS (DELETE FROM audit_old WHERE ctid IN (SELECT ctid FROM audit_old ORDER BY ts LIMIT 50000) RETURNING *) INSERT INTO audit_n (ts, country_code, action, row_hash, payload) SELECT ts, country_code, action, row_hash, payload FROM m").rowcount
                if not r:
                    break
                moved += r
        print(f"moved {moved:,} rows in 50,000-row batches (DELETE..RETURNING into the partitioned table): {t.s:.1f}s ({moved / t.s:,.0f} rows/s)")
        c.close()
    finally:
        for f in files:
            os.remove(f)
        print(f"removed {len(files)} temporary extension files")
        drop_db(DB)


if __name__ == "__main__":
    main()
