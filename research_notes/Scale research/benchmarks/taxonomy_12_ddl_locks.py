#!/usr/bin/env python3
"""How long the DDL steps of the migration plan block writers, measured on a 2,000,000-row copy of entry with one
client updating random rows the whole time (pgbench, per-transaction log). Each step is run the way Django would run
it (plain ALTER, plain CREATE INDEX) and the way the plan runs it (NOT VALID then VALIDATE, CREATE INDEX CONCURRENTLY).

  sudo -u postgres env PYTHONPATH=/var/tmp/benchlibs python3 taxonomy_12_ddl_locks.py DBNAME OUTDIR
"""
import glob
import json
import os
import re
import subprocess
import sys
import time

import psycopg

DB, OUT = sys.argv[1], sys.argv[2]
assert re.fullmatch(r"bench_taxonomy_[a-z0-9_]+", DB)
os.chdir(OUT)
conn = psycopg.connect(dbname=DB, user="postgres", autocommit=True)
conn.execute("DROP TABLE IF EXISTS entry_mig, brand_mig CASCADE")
conn.execute("CREATE TABLE entry_mig AS TABLE entry")
conn.execute("ALTER TABLE entry_mig ADD PRIMARY KEY (id)")
conn.execute("CREATE INDEX ON entry_mig (place_path text_pattern_ops)")
conn.execute("CREATE TABLE brand_mig (id bigserial PRIMARY KEY, name text)")
conn.execute("VACUUM (ANALYZE) entry_mig")
N = conn.execute("SELECT count(*) FROM entry_mig").fetchone()[0]

open("/var/tmp/benchout/ddl_writer.sql", "w").write("\\set id random(1, 2000000)\nUPDATE entry_mig SET fresh = fresh + 1 WHERE id = :id;\n")

STEPS = [
    (
        "AddField, nullable foreign key (Django: ADD COLUMN ... REFERENCES in one statement)",
        "ALTER TABLE entry_mig ADD COLUMN moved_to_id bigint NULL CONSTRAINT fk_moved REFERENCES entry_mig (id) DEFERRABLE INITIALLY DEFERRED",
        "ALTER TABLE entry_mig ADD COLUMN brand_id bigint NULL;"
        "ALTER TABLE entry_mig ADD CONSTRAINT fk_brand_nv FOREIGN KEY (brand_id) REFERENCES brand_mig (id) DEFERRABLE INITIALLY DEFERRED NOT VALID;"
        "ALTER TABLE entry_mig VALIDATE CONSTRAINT fk_brand_nv",
    ),
    (
        "AddField, small integer with default 0, NOT NULL and CHECK (Django)",
        "ALTER TABLE entry_mig ADD COLUMN closure_score smallint DEFAULT 0 NOT NULL CHECK (closure_score >= 0);"
        "ALTER TABLE entry_mig ALTER COLUMN closure_score DROP DEFAULT",
        "same",
    ),
    (
        "Index on the new foreign key column (Django: plain CREATE INDEX)",
        "CREATE INDEX entry_mig_moved_plain ON entry_mig (moved_to_id)",
        "CREATE INDEX CONCURRENTLY entry_mig_brand_cc ON entry_mig (brand_id)",
    ),
    (
        "Check constraint on a populated column",
        "ALTER TABLE entry_mig ADD CONSTRAINT chk_plain CHECK (rank <= 3)",
        "ALTER TABLE entry_mig ADD CONSTRAINT chk_nv CHECK (rank <= 3) NOT VALID; ALTER TABLE entry_mig VALIDATE CONSTRAINT chk_nv",
    ),
]


def run_step(sql):
    for f in glob.glob("pgbench_log.*"):
        os.remove(f)
    p = subprocess.Popen(
        ["pgbench", "-n", "-h", "/var/run/postgresql", "-U", "postgres", "-d", DB, "-f", "/var/tmp/benchout/ddl_writer.sql", "-c", "1", "-T", "40", "-l"],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
    )
    time.sleep(4)
    t = time.perf_counter()
    for stmt in [s for s in sql.split(";") if s.strip()]:
        conn.execute(stmt)
    dur = time.perf_counter() - t
    # let the writer run a few more seconds, then stop it early
    time.sleep(3)
    p.terminate()
    p.wait()
    lat = []
    for f in glob.glob("pgbench_log.*"):
        for line in open(f):
            parts = line.split()
            if len(parts) >= 3:
                lat.append(int(parts[2]) / 1000.0)
    lat.sort()
    return {"ddl_seconds": round(dur, 3), "writer_txns": len(lat), "writer_max_ms": round(max(lat), 1) if lat else None, "writer_p99_ms": round(lat[int(0.99 * len(lat))], 2) if lat else None, "writer_over_500ms": sum(1 for x in lat if x > 500)}


results = []
for label, plain, safe in STEPS:
    r1 = run_step(plain)
    r2 = None if safe == "same" else run_step(safe)
    results.append({"step": label, "plain": r1, "plan": r2})
    print(results[-1], flush=True)
json.dump({"rows": N, "steps": results}, open(f"{OUT}/ddl_locks.json", "w"), indent=1)
conn.execute("DROP TABLE IF EXISTS entry_mig, brand_mig CASCADE")
