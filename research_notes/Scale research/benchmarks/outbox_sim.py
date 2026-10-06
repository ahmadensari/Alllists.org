"""Proof of the index-sync design: transactional outbox + idempotent versioned upserts into a simulated engine.

Usage: python outbox_sim.py --db bench_outbox   (creates tables, runs 5 tests, writes results/outbox_sim.json)
Refuses databases whose name does not start with bench_. Creates the database on the private bench cluster if missing.
Tests
  T1 write overhead of the outbox trigger (single-row transactions, one client)
  T2 consumer throughput with 1 and 4 workers claiming batches with FOR UPDATE SKIP LOCKED
  T3 convergence under duplicate, shuffled, reordered delivery and worker crashes (must equal the source of truth)
  T4 outbox age (lag) under a sustained write rate with 2 consumers
  T5 cost of cleaning done rows
"""
import argparse, json, random, statistics, sys, threading, time
import numpy as np, psycopg

ap = argparse.ArgumentParser()
ap.add_argument("--db", required=True)
ap.add_argument("--socket-dir", default="/var/lib/postgresql/bench_pg16"); ap.add_argument("--port", type=int, default=5544)
a = ap.parse_args()
if not a.db.startswith("bench_"): sys.exit("refusing: database name must start with bench_")
dsn = lambda db: f"host={a.socket_dir} port={a.port} dbname={db} user=postgres"
with psycopg.connect(dsn("postgres"), autocommit=True) as c:
    if not c.execute("select 1 from pg_database where datname=%s", [a.db]).fetchone():
        c.execute(f'create database "{a.db}"')
R = {}
def conn(): return psycopg.connect(dsn(a.db), autocommit=True)

DDL = """
drop table if exists src, outbox, idx cascade;
create table src(id bigint primary key, name text, version bigint not null default 1);
create table outbox(id bigserial primary key, entry_id bigint not null, version bigint not null, op char(1) not null,
                    created_at timestamptz not null default clock_timestamp(), done_at timestamptz);
create index outbox_pending on outbox(id) where done_at is null;
create table idx(id bigint primary key, version bigint not null, name text, deleted boolean not null default false);
create or replace function src_outbox() returns trigger language plpgsql as $$
begin
  if tg_op = 'DELETE' then insert into outbox(entry_id, version, op) values (old.id, old.version + 1, 'D'); return old;
  else insert into outbox(entry_id, version, op) values (new.id, new.version, case tg_op when 'INSERT' then 'I' else 'U' end); return new; end if;
end $$;
"""
c = conn(); c.execute(DDL)
c.execute("create trigger src_ob after insert or update or delete on src for each row execute function src_outbox()")
N = 200_000
c.execute("insert into src select g, 'entry ' || g, 1 from generate_series(1, %s) g", [N])

# ---- T1 write overhead ----
def bump(n, with_trigger):
    c.execute("alter table src %s trigger src_ob" % ("enable" if with_trigger else "disable"))
    ids = [random.randrange(1, N + 1) for _ in range(n)]
    t = time.perf_counter()
    for i in ids: c.execute("update src set version = version + 1, name = name where id = %s", [i])
    return n / (time.perf_counter() - t)
random.seed(1)
tps_no = bump(20000, False); tps_tr = bump(20000, True); tps_no2 = bump(20000, False); tps_tr2 = bump(20000, True)
R["T1"] = {"updates_per_s_no_trigger": round((tps_no + tps_no2) / 2), "updates_per_s_with_outbox_trigger": round((tps_tr + tps_tr2) / 2),
           "overhead_pct": round(100 * (1 - (tps_tr + tps_tr2) / (tps_no + tps_no2)), 1)}
print("T1", R["T1"], flush=True)

# ---- consumer ----
CLAIM = """with c as (select id from outbox where done_at is null order by id limit %(n)s for update skip locked)
           update outbox o set done_at = clock_timestamp() from c where o.id = c.id returning o.entry_id, o.version, o.op, o.created_at, o.done_at"""
APPLY = """insert into idx(id, version, name, deleted)
           select s.entry_id, s.version, null, s.op = 'D' from unnest(%(ids)s::bigint[], %(vers)s::bigint[], %(ops)s::text[]) as s(entry_id, version, op)
           on conflict (id) do update set version = excluded.version, deleted = excluded.deleted where idx.version < excluded.version"""
def drain_once(cn, n=1000, crash=False):
    with cn.transaction():
        rows = cn.execute(CLAIM, {"n": n}).fetchall()
        if not rows: return 0, []
        latest = {}
        for eid, ver, op, cr, dn in rows:       # coalesce: keep the highest version per entry in the batch
            if eid not in latest or ver > latest[eid][0]: latest[eid] = (ver, op)
        ids = list(latest); cn.execute(APPLY, {"ids": ids, "vers": [latest[i][0] for i in ids], "ops": [latest[i][1] for i in ids]})
        if crash: raise RuntimeError("simulated crash after apply, before commit")
        return len(rows), [(dn - cr).total_seconds() for _, _, _, cr, dn in rows]

# ---- T2 throughput ----
for tag, workers in (("1_worker", 1), ("4_workers", 4)):
    c.execute("truncate outbox; truncate idx")
    c.execute("insert into outbox(entry_id, version, op) select (random() * %s)::bigint + 1, g, 'U' from generate_series(1, 400000) g", [N])
    done = [0] * workers
    def work(k):
        cn = conn()
        while True:
            n, _ = drain_once(cn)
            if n == 0: break
            done[k] += n
        cn.close()
    t = time.perf_counter(); th = [threading.Thread(target=work, args=(k,)) for k in range(workers)]
    [x.start() for x in th]; [x.join() for x in th]; dt = time.perf_counter() - t
    R.setdefault("T2", {})[tag] = {"rows": sum(done), "seconds": round(dt, 2), "rows_per_s": round(sum(done) / dt)}
print("T2", R["T2"], flush=True)

# ---- T3 convergence ----
c.execute("truncate outbox; truncate idx; truncate src")
M = 20000; rng = random.Random(5)
c.execute("alter table src disable trigger src_ob")
c.execute("insert into src select g, 'e' || g, 1 from generate_series(1, %s) g", [M])
events = []   # (entry, version, op); the source of truth is the max version per entry
truth = {g: (1, "I") for g in range(1, M + 1)}
events += [(g, 1, "I") for g in range(1, M + 1)]
for _ in range(150000):
    g = rng.randrange(1, M + 1); v = truth[g][0] + 1; op = "D" if rng.random() < 0.02 else "U"
    truth[g] = (v, op); events.append((g, v, op))
dups = rng.sample(events, int(len(events) * 0.2)); events += dups      # 20% duplicate deliveries
rng.shuffle(events)                                                      # arbitrary order
c.execute("insert into outbox(entry_id, version, op) select * from unnest(%s::bigint[], %s::bigint[], %s::text[])",
          [[e[0] for e in events], [e[1] for e in events], [e[2] for e in events]])
crashes = 0; cn = conn()
while True:
    try:
        n, _ = drain_once(cn, 777, crash=rng.random() < 0.15)
    except RuntimeError:
        crashes += 1; continue
    if n == 0: break
# a delete followed by an older update delivered later must not resurrect: version guard handles it
mism = 0
rows = {r[0]: (r[1], r[2]) for r in c.execute("select id, version, deleted from idx").fetchall()}
for g, (v, op) in truth.items():
    exp = (v, op == "D")
    if rows.get(g) != exp: mism += 1
R["T3"] = {"entries": M, "events_delivered": len(events), "duplicate_events": len(dups), "worker_crashes_injected": crashes,
           "mismatches_vs_source_of_truth": mism}
print("T3", R["T3"], flush=True)
assert mism == 0

# ---- T4 lag under sustained writes ----
c.execute("truncate outbox; truncate idx; alter table src enable trigger src_ob")
stop = threading.Event(); ages = []; lock = threading.Lock(); written = [0]
def writer(rate=2000):
    cn = conn(); t0 = time.perf_counter(); i = 0
    while not stop.is_set():
        cn.execute("update src set version = version + 1 where id = %s", [rng.randrange(1, M + 1)]); i += 1; written[0] = i
        ahead = i / rate - (time.perf_counter() - t0)
        if ahead > 0: time.sleep(ahead)
def reader():
    cn = conn()
    while not stop.is_set():
        n, ag = drain_once(cn, 500)
        if n == 0: time.sleep(0.05)
        else:
            with lock: ages.extend(ag)
th = [threading.Thread(target=writer)] + [threading.Thread(target=reader) for _ in range(2)]
[x.start() for x in th]; time.sleep(20); stop.set(); [x.join() for x in th]
ages_ms = np.array(ages) * 1000
R["T4"] = {"target_writes_per_s": 2000, "achieved_writes_per_s": round(written[0] / 20), "events_consumed": len(ages),
           "age_ms_p50": round(float(np.percentile(ages_ms, 50)), 1), "age_ms_p95": round(float(np.percentile(ages_ms, 95)), 1),
           "age_ms_max": round(float(ages_ms.max()), 1)}
print("T4", R["T4"], flush=True)

# ---- T5 cleanup ----
c.execute("truncate outbox"); c.execute("insert into outbox(entry_id, version, op, done_at) select g % 1000 + 1, g, 'U', now() from generate_series(1, 1000000) g")
t = time.perf_counter(); c.execute("delete from outbox where done_at < now() + interval '1 minute'"); d = time.perf_counter() - t
t = time.perf_counter(); c.execute("vacuum outbox"); v = time.perf_counter() - t
R["T5"] = {"delete_1m_done_rows_s": round(d, 1), "vacuum_s": round(v, 1),
           "note": "in production partition outbox by day and drop old partitions instead of deleting"}
print("T5", R["T5"])
json.dump(R, open("results/outbox_sim.json", "w"), indent=1)
