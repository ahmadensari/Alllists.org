"""Experiment: one multicolumn GIN index that holds place ancestors, list-type ancestors and the text, so that
'list = saved filter' (place subtree AND list type subtree AND text) is ONE index scan at any depth.

Usage: python anc_gin.py --db bench_search --scale 1m|5m   (refuses databases not starting with bench_)
Adds place_anc text[] and concept_anc int[] to entry_<scale>, builds
   gin (place_anc, concept_anc, tsv)       -> tsv text match
   gin (place_anc, concept_anc, name_fold gin_trgm_ops) -> contains and word-similarity text match
and compares with the btree-range plans of run_bench.py for the same kind of queries (city, area, city+list type).
"""
import argparse, json, random, sys, time
import numpy as np, psycopg
ap = argparse.ArgumentParser()
ap.add_argument("--db", required=True); ap.add_argument("--scale", choices=["1m", "5m"], required=True)
ap.add_argument("--socket-dir", default="/var/lib/postgresql/bench_pg16"); ap.add_argument("--port", type=int, default=5544)
ap.add_argument("--n", type=int, default=100); ap.add_argument("--build", action="store_true")
a = ap.parse_args()
if not a.db.startswith("bench_"): sys.exit("refusing: database name must start with bench_")
E, W = f"entry_{a.scale}", f"words_{a.scale}"
con = psycopg.connect(f"host={a.socket_dir} port={a.port} dbname={a.db} user=postgres", autocommit=True); cur = con.cursor()
cur.execute("set maintenance_work_mem='2GB'; set statement_timeout=20000; set pg_trgm.word_similarity_threshold=0.4; set jit=off")
out = {"scale": a.scale}
if a.build:
    t = time.time()
    cur.execute(f"alter table {E} add column if not exists place_anc text[], add column if not exists concept_anc int[]")
    cur.execute(f"""update {E} e set place_anc = array[ split_part(place_path,'.',1), split_part(place_path,'.',1)||'.'||split_part(place_path,'.',2),
                    split_part(place_path,'.',1)||'.'||split_part(place_path,'.',2)||'.'||split_part(place_path,'.',3), place_path ]""")
    cur.execute(f"""create temp table cmap as select descendant_id, array_agg(ancestor_id) anc from concept_closure group by 1""")
    cur.execute(f"update {E} e set concept_anc = m.anc from cmap m where m.descendant_id = e.concept_id")
    out["columns_seconds"] = round(time.time() - t, 1)
    for name, sql in (("gin_anc_tsv", f"create index {E}_anc_tsv on {E} using gin (place_anc, concept_anc, tsv) where publish_state = 'published'"),
                      ("gin_anc_trgm", f"create index {E}_anc_trgm on {E} using gin (place_anc, concept_anc, name_fold gin_trgm_ops) where publish_state = 'published'")):
        t = time.time(); cur.execute(sql)
        cur.execute(f"select pg_relation_size('{E}_{name.split('_',1)[1]}')"); out[name] = {"seconds": round(time.time() - t, 1), "bytes": cur.fetchone()[0]}
        print(name, out[name], flush=True)
    cur.execute(f"vacuum analyze {E}")
# ---- queries
rnd = random.Random(5)
cur.execute(f"select place_path, count(*) from {E} where publish_state='published' group by 1"); leaf = cur.fetchall()
cities = {}
for p, c in leaf: k = ".".join(p.split(".")[:3]); cities[k] = cities.get(k, 0) + c
cities = [(k, v) for k, v in cities.items() if v >= 30]; areas = [(p, c) for p, c in leaf if c >= 20 and p.count(".") == 3]
cur.execute(f"select word, df from {W}"); df = dict(cur.fetchall())
N = sum(c for _, c in leaf)
cur.execute("select id from concept where parent_id is null"); roots = [r[0] for r in cur.fetchall()]
def pick(items): return rnd.choices([i for i, _ in items], [w for _, w in items])[0]
def cls_word(ws, cls):
    top = {w for w, _ in sorted(df.items(), key=lambda t: -t[1])[:25]}
    for w in ws:
        d = df.get(w, 0)
        if cls == "common" and w in top: return w
        if cls == "mid" and w not in top and N * 0.0002 <= d <= N * 0.005 and len(w) >= 3: return w
    return None
def make(kind, cls):
    for _ in range(200):
        path = pick(cities) if kind.startswith("city") else pick(areas)
        prm = {"p": path}
        if kind == "city_concept":
            root = rnd.choice(roots); cond += " and concept_anc @> array[%(r)s]"; prm["r"] = root
        cur.execute(f"select name_fold from {E} where publish_state='published' and place_anc @> array[%(p)s] {'and concept_anc @> array[%(r)s]' if 'r' in prm else ''} order by random() limit 30", prm)
        rows = [r[0] for r in cur.fetchall()]
        if not rows: continue
        ws = rnd.choice(rows).split()
        q = cls_word(ws, cls) if cls in ("common", "mid") else (" ".join(ws[:2]) if len(ws) >= 2 else None)
        if q: return q, prm
    return None
cells = []
for kind in ("city", "area", "city_concept"):
    for cls in ("common", "mid", "two"):
        qs = [x for x in (make(kind, cls) for _ in range(a.n)) if x]
        cells.append((kind, cls, qs))
def run(method, q, prm):
    sc = " and place_anc @> array[%(p)s]" + (" and concept_anc @> array[%(r)s]" if "r" in prm else "")
    words = q.split()
    tsq = " & ".join(words[:-1] + [words[-1] + ":*"])
    if method == "anc_tsv":
        sql = f"select name_fold from (select name_fold, static_score from {E} where publish_state='published' {sc} and tsv @@ to_tsquery('simple', %(t)s) order by static_score desc limit 200) c order by word_similarity(%(q)s, name_fold)*0.6 + static_score/1e6*0.4 desc limit 25"
        p = dict(prm, t=tsq, q=q)
    elif method == "anc_like":
        sql = f"select name_fold from {E} where publish_state='published' {sc} and name_fold like '%%'||%(q)s||'%%' order by static_score desc limit 25"; p = dict(prm, q=q)
    elif method == "anc_wsim":
        sql = f"select name_fold from {E} where publish_state='published' {sc} and %(q)s <%% name_fold order by word_similarity(%(q)s, name_fold) desc, static_score desc limit 25"; p = dict(prm, q=q)
    cur.execute(sql, p); return cur.fetchall()
res = []
for kind, cls, qs in cells:
    for method in ("anc_tsv", "anc_like", "anc_wsim") if cls == "common" else ("anc_tsv", "anc_like"):
        lat = []
        for i, (q, prm) in enumerate(qs):
            t0 = time.perf_counter()
            try: run(method, q, prm)
            except psycopg.errors.QueryCanceled: lat.append(20000.0); continue
            ms = (time.perf_counter() - t0) * 1000
            if i >= 3: lat.append(ms)
        arr = np.array(lat); r = dict(scale=a.scale, scope=kind, cls=cls, method=method, n=len(lat), p50=round(float(np.percentile(arr, 50)), 2), p95=round(float(np.percentile(arr, 95)), 2), max=round(float(arr.max()), 1))
        res.append(r); print(r, flush=True)
out["cells"] = res
json.dump(out, open(f"results/anc_gin_{a.scale}.json", "w"), indent=1)
