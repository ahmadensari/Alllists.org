"""Latency by name script (Latin 'la', Roman Urdu 'ru', Urdu 'ur') for the index shapes chosen in note 07.

run_bench.py reports a per-script split only when a script has at least 10 queries in a cell, and Urdu rarely does. This script
samples the queries per script on purpose (n per cell, default 60) so every script has a number.

Usage: python bench_script.py --db bench_search --scale 1m|5m [--n 60]   (read only; refuses databases not starting with bench_)
Writes results/search_script_<scale>.jsonl. Query shapes are the ones in run_bench.py: tsv (prefix on the last word, stored prior, LIMIT 200),
like (substring, pg_trgm GIN), btree (prefix), dict (typo corrected through the word dictionary, then tsv).
Scopes: unscoped, country (pk), city (a pk city with at least 30 published entries, weighted by size).
"""
import argparse, json, random, re, sys, time
import numpy as np, psycopg

ap = argparse.ArgumentParser()
ap.add_argument("--db", required=True); ap.add_argument("--scale", choices=["1m", "5m"], required=True)
ap.add_argument("--n", type=int, default=60); ap.add_argument("--timeout-ms", type=int, default=4000)
ap.add_argument("--socket-dir", default="/var/lib/postgresql/bench_pg16"); ap.add_argument("--port", type=int, default=5544)
ap.add_argument("--seed", type=int, default=13)
a = ap.parse_args()
if not a.db.startswith("bench_"): sys.exit("refusing: database name must start with bench_")
E, V, W = f"entry_{a.scale}", f"variant_{a.scale}", f"words_{a.scale}"
rnd = random.Random(a.seed)
con = psycopg.connect(f"host={a.socket_dir} port={a.port} dbname={a.db} user=postgres", autocommit=True); cur = con.cursor()
cur.execute("set statement_timeout = 0"); cur.execute("set jit = off")
cur.execute("create extension if not exists pg_prewarm")
cur.execute("select c.oid::regclass::text from pg_class c where c.relkind in ('r','i') and c.relnamespace = 'public'::regnamespace and (c.relname like %s or c.relname like %s or c.relname like %s)",
            [f"{E}%", f"{V}%", f"{W}%"])
for (rel,) in cur.fetchall(): cur.execute("select pg_prewarm(%s)", [rel])
cur.execute(f"set statement_timeout = {a.timeout_ms}")
cur.execute(f"select count(*) from {E}"); N = cur.fetchone()[0]
cur.execute("select place_path, count(*) from %s where publish_state='published' group by 1" % E)
city = {}
for p, c in cur.fetchall():
    k = ".".join(p.split(".")[:3]); city[k] = city.get(k, 0) + c
cities = [(c, n) for c, n in city.items() if n >= 30 and c.startswith("pk.")]
def pick_city():
    tot = sum(n for _, n in cities); r = rnd.random() * tot
    for c, n in cities:
        r -= n
        if r <= 0: return c
    return cities[-1][0]

def scope(kind, path):
    if kind == "unscoped": return "", {}
    if kind == "country": return " and country_code = 'pk'", {}
    return " and country_code = 'pk' and (place_path = %(p)s or place_path like %(pl)s)", {"p": path, "pl": path + ".%"}

def sample(kind, path, script, k=40):
    frag, pr = scope(kind, path)
    if kind == "city":
        cur.execute(f"select name_fold from {E} where publish_state='published' and script=%(s)s {frag} order by random() limit {k}", dict(pr, s=script))
    else:
        cur.execute(f"select name_fold from {E} where id = any(%(ids)s) and publish_state='published' and script=%(s)s {frag} limit {k}",
                    dict(pr, s=script, ids=[rnd.randrange(1, N + 1) for _ in range(k * 6)]))
    return [r[0] for r in cur.fetchall()]

def typo(w, script):
    i = rnd.randrange(1, len(w) - 1); op = rnd.choice("sdt")
    if op == "s": return w[:i] + (rnd.choice("abcdefghilmnoprstu") if w.isascii() else rnd.choice("اسنرمتلکب")) + w[i + 1:]
    if op == "d": return w[:i] + w[i + 1:]
    return w[:i] + w[i + 1] + w[i] + w[i + 2:]

def tsq(words, prefix=True):
    esc = [re.sub(r"[^\w]", "", w) for w in words]; esc = [w for w in esc if w]
    return " & ".join(esc[:-1] + [esc[-1] + (":*" if prefix else "")]) if esc else ""

def run(method, q, frag, pr):
    t0 = time.perf_counter()
    if method == "like":
        cur.execute(f"select id from {E} where publish_state='published' {frag} and name_fold like '%%' || %(q)s || '%%' order by static_score desc limit 25", dict(pr, q=q["text"]))
    elif method == "btree":
        cur.execute(f"select id from {E} where publish_state='published' {frag} and name_fold like %(q)s || '%%' order by static_score desc limit 25", dict(pr, q=q["text"]))
    elif method == "tsv":
        cur.execute(f"""select id, name_fold from (select id, name_fold, static_score from {E} where publish_state='published' {frag}
                        and tsv @@ to_tsquery('simple', %(t)s) order by static_score desc limit 200) c
                        order by word_similarity(%(q)s, name_fold) * 0.6 + static_score / 1e6 * 0.4 desc limit 25""", dict(pr, t=tsq(q["words"]), q=q["text"]))
    elif method == "dict":
        alts = []
        for w in q["words"]:
            cur.execute(f"select word from {W} where word %% %(w)s order by similarity(word, %(w)s) desc, df desc limit 3", {"w": w})
            got = [r[0] for r in cur.fetchall()] or [w]
            alts.append("(" + " | ".join(re.sub(r"[^\w]", "", g) for g in got) + ")")
        cur.execute(f"""select id, name_fold from {E} where publish_state='published' {frag} and tsv @@ to_tsquery('simple', %(t)s)
                        order by static_score desc limit 25""", dict(pr, t=" & ".join(alts)))
    rows = cur.fetchall()
    return (time.perf_counter() - t0) * 1000, rows

CELLS = [("two", "tsv"), ("two", "like"), ("prefix", "btree"), ("prefix", "tsv"), ("typo", "dict")]
out = open(f"results/search_script_{a.scale}.jsonl", "w")
for kind in ("unscoped", "country", "city"):
    for script in ("la", "ru", "ur"):
        pool = []
        tries = 0
        while len(pool) < a.n + 3 and tries < a.n * 10:
            tries += 1
            path = pick_city() if kind == "city" else None
            names = sample(kind, path, script, 10)
            if not names: continue
            nm = rnd.choice(names); ws = nm.split()
            pool.append((nm, ws, path))
        for cls, method in CELLS:
            qs = []
            for nm, ws, path in pool:
                if cls == "two" and len(ws) >= 2: qs.append(dict(text=" ".join(ws[:2]), words=ws[:2], path=path))
                elif cls == "prefix" and len(ws[0]) >= 3:
                    L = min(rnd.choice([2, 3, 4]), len(ws[0]) - 1); qs.append(dict(text=ws[0][:L], words=[ws[0][:L]], path=path))
                elif cls == "typo":
                    c = [w for w in ws if len(w) >= (4 if script == "ur" else 5)]
                    if c: w = rnd.choice(c); t = typo(w, script); qs.append(dict(text=t, words=[t], orig=w, path=path))
            if len(qs) < 20: print("too few", kind, script, cls, len(qs)); continue
            lat, hits, rows_n, to = [], [], [], 0
            for i, q in enumerate(qs[:a.n + 3]):
                frag, pr = scope(kind, q["path"])
                try: ms, rows = run(method, q, frag, pr)
                except psycopg.errors.QueryCanceled: ms, rows = a.timeout_ms, []; to += 1
                if i < 3: continue
                lat.append(ms); rows_n.append(len(rows))
                if cls == "typo": hits.append(any(q["orig"] in r[1].split() for r in rows) if rows else False)
            arr = np.array(lat)
            rec = dict(scale=a.scale, scope=kind, script=script, cls=cls, method=method, n=len(lat), p50=round(float(np.percentile(arr, 50)), 2),
                       p95=round(float(np.percentile(arr, 95)), 2), max=round(float(arr.max()), 1), timeouts=to, mean_rows=round(float(np.mean(rows_n)), 1),
                       loadavg_1m=open("/proc/loadavg").read().split()[0])
            if hits: rec["typo_recall25"] = round(sum(hits) / len(hits), 3)
            out.write(json.dumps(rec, ensure_ascii=False) + "\n"); out.flush()
            print(f"{a.scale} {kind:9s}{script} {cls:6s}{method:6s} n={rec['n']:3d} p50={rec['p50']:8.2f} p95={rec['p95']:8.2f} rows={rec['mean_rows']:5.1f}"
                  + (f" recall={rec['typo_recall25']}" if hits else ""), flush=True)
