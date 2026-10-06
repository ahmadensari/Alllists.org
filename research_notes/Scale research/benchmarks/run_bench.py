"""Latency benchmark for Postgres search over the synthetic entries (single client, warm cache).

Usage: python run_bench.py --db bench_search --scale 1m|5m [--n 150] [--only scope,class,method filters]
Writes results/search_<scale>.jsonl, one line per (scope, query class, method) cell.
Refuses any database not starting with bench_. Read-only on the data (SELECT and EXPLAIN only).

Query classes   common  one very frequent word (top 25 words by document frequency)
                mid     one word with document frequency 0.02% to 0.5% of rows
                rare    one word with 30 or fewer documents
                two     the first two words of a real name
                typo    a mid or two-word query with one edit (substitution, deletion, transposition) in a word of 5+ letters
                prefix  the first 2, 3 or 4 letters of the first word of a real name (autocomplete)
Scopes          unscoped, country (pk), city, area, city_concept (list page: city + a list type with its descendants)
                city_nocc / area_nocc: same as city / area but WITHOUT the country_code predicate (the repository's SQL shape)
Methods         repo     the repository's current ModelBackend.entries() SQL shape (similarity() function, OR, variant subselect)
                like     name_fold LIKE '%q%' (pg_trgm GIN)
                wsim     q <% name_fold (pg_trgm word similarity, threshold 0.4, GIN)
                tsv      to_tsquery('simple', 'a & b:*') on a stored tsvector (GIN), ordered by stored prior, LIMIT 200 then reranked
                tsvrank  same match, ordered by ts_rank (textbook)
                btree    name_fold LIKE 'q%' (btree text_pattern_ops), ordered by stored prior
                dict     typo correction through a word dictionary (trigram on words) then tsv
"""
import argparse, json, random, re, statistics, sys, time
import numpy as np
import psycopg

ap = argparse.ArgumentParser()
ap.add_argument("--db", required=True)
ap.add_argument("--scale", choices=["1m", "5m"], required=True)
ap.add_argument("--n", type=int, default=150)
ap.add_argument("--only", default="", help="comma list of substrings; a cell runs if scope:cls:method contains any")
ap.add_argument("--socket-dir", default="/var/lib/postgresql/bench_pg16")
ap.add_argument("--port", type=int, default=5544)
ap.add_argument("--timeout-ms", type=int, default=4000)
ap.add_argument("--seed", type=int, default=7)
ap.add_argument("--out", default="")
a = ap.parse_args()
if not a.db.startswith("bench_"):
    sys.exit("refusing: database name must start with bench_")
E, V, W = f"entry_{a.scale}", f"variant_{a.scale}", f"words_{a.scale}"
rnd = random.Random(a.seed)
con = psycopg.connect(f"host={a.socket_dir} port={a.port} dbname={a.db} user=postgres", autocommit=True)
cur = con.cursor()
cur.execute(f"set statement_timeout = {a.timeout_ms}")
cur.execute("set pg_trgm.similarity_threshold = 0.25; set pg_trgm.word_similarity_threshold = 0.4; set jit = off")
cur.execute(f"select count(*) from {E}"); N = cur.fetchone()[0]

# ---------- word statistics ----------
cur.execute(f"select word, df from {W}")
df = dict(cur.fetchall())
top = sorted(df.items(), key=lambda t: -t[1])
COMMON = {w for w, _ in top[:25]}
MIDLO, MIDHI = max(40, N * 0.0002), N * 0.005
def wclass(w):
    d = df.get(w, 0)
    if w in COMMON: return "common"
    if MIDLO <= d <= MIDHI: return "mid"
    if d <= 30: return "rare"
    return "other"

# ---------- scopes ----------
cur.execute(f"""select place_path, count(*) from {E} where publish_state='published' group by 1""")
leaf_counts = cur.fetchall()
city_counts = {}
for p, c in leaf_counts:
    city = ".".join(p.split(".")[:3]); city_counts[city] = city_counts.get(city, 0) + c
cities = [(c, n) for c, n in city_counts.items() if n >= 30]
areas = [(p, c) for p, c in leaf_counts if c >= 20 and p.count(".") == 3]
def wchoice(items):
    tot = sum(w for _, w in items); r = rnd.random() * tot
    for it, w in items:
        r -= w
        if r <= 0: return it
    return items[-1][0]
cur.execute("select ancestor_id, array_agg(descendant_id) from concept_closure group by 1")
closure = dict(cur.fetchall())
cur.execute("select id from concept where parent_id is null"); roots = [r[0] for r in cur.fetchall()]

def scope_sql(kind, path, cc, cids):
    """returns (sql fragment, params) for the scope; fragment starts with ' and '"""
    pr = {}
    if kind == "unscoped": return "", pr
    if kind == "country": return " and country_code = %(cc)s", {"cc": cc}
    if kind in ("city", "area"):
        return " and country_code = %(cc)s and (place_path = %(p)s or place_path like %(pl)s)", {"cc": cc, "p": path, "pl": path + ".%"}
    if kind in ("city_nocc", "area_nocc"):
        return " and (place_path = %(p)s or place_path like %(pl)s)", {"p": path, "pl": path + ".%"}
    if kind == "city_concept":
        return " and country_code = %(cc)s and (place_path = %(p)s or place_path like %(pl)s) and concept_id = any(%(cids)s)", \
               {"cc": cc, "p": path, "pl": path + ".%", "cids": cids}
    raise ValueError(kind)

def pick_scope(kind):
    if kind == "unscoped": return None, None, None
    if kind == "country": return "pk", "pk", None
    if kind in ("city", "city_nocc", "city_concept"):
        path = wchoice(cities)
    else:
        path = wchoice(areas)
    cids = None
    if kind == "city_concept":
        # a root list type that exists in this city, weighted by size
        cur.execute(f"""select c.id, count(*) from {E} e join concept_closure cc on cc.descendant_id = e.concept_id
                        join concept c on c.id = cc.ancestor_id and c.parent_id is null
                        where e.country_code = %s and e.place_path like %s and e.publish_state='published' group by 1 having count(*) >= 20""",
                    [path.split(".")[0], path + "%"])
        opts = cur.fetchall()
        if not opts: return pick_scope(kind)
        root = wchoice(opts); cids = closure[root]
    return path, path.split(".")[0], cids

def sample_names(kind, path, cc, cids, k=60):
    frag, pr = scope_sql(kind, path, cc, cids)
    cur.execute(f"select id, name_fold, script from {E} where publish_state='published' {frag} order by random() limit {k}", pr)
    return cur.fetchall()

def typo(word):
    i = rnd.randrange(1, len(word) - 1); op = rnd.choice("sdt")
    if op == "s":
        c = rnd.choice("abcdefghilmnoprstu") if word.isascii() else rnd.choice("اسنرمتلکب")
        return word[:i] + c + word[i + 1:]
    if op == "d": return word[:i] + word[i + 1:]
    return word[:i] + word[i + 1] + word[i] + word[i + 2:]

def make_query(cls, rows):
    """rows: sampled (id, name_fold, script); returns dict or None"""
    rnd.shuffle(rows)
    for eid, name, script in rows:
        ws = name.split()
        if cls in ("common", "mid", "rare"):
            for w in ws:
                if wclass(w) == cls and len(w) >= 3: return dict(text=w, words=[w], eid=eid, script=script, cls=cls)
        elif cls == "two" and len(ws) >= 2:
            return dict(text=" ".join(ws[:2]), words=ws[:2], eid=eid, script=script, cls=cls)
        elif cls == "typo":
            cands = [w for w in ws if len(w) >= 5 and wclass(w) in ("mid", "rare", "other")]
            if cands:
                w = rnd.choice(cands); t = typo(w)
                return dict(text=t, words=[t], orig=w, eid=eid, script=script, cls=cls)
        elif cls == "prefix":
            w = ws[0]
            if len(w) >= 3:
                L = rnd.choice([2, 3, 4]); L = min(L, len(w) - 1)
                return dict(text=w[:L], words=[w[:L]], eid=eid, script=script, cls=cls)
    return None

def tsq(words, prefix_last=True):
    esc = [re.sub(r"[^\w]", "", w) for w in words]
    esc = [w for w in esc if w]
    if not esc: return ""
    return " & ".join(esc[:-1] + [esc[-1] + (":*" if prefix_last else "")])

CAND = 200
def sql_for(method, q, frag):
    """returns list of (sql, params) steps; result of the LAST step is what is timed as rows"""
    qt = q["text"]
    if method == "repo":
        # replicates catalog/search_backend.py ModelBackend.entries(): SIMILARITY() function, OR, variant subselect, contains
        return [(f"""select id, name_fold, similarity(name_fold, %(q)s) as sim from {E} where publish_state = 'published' {frag}
            and (similarity(name_fold, %(q)s) >= 0.25 or id in (select entry_id from {V} where similarity(text_fold, %(q)s) >= 0.25)
                 or name_fold like '%%' || %(q)s || '%%') order by sim desc, name_fold limit 25""", {"q": qt})]
    if method == "like":
        return [(f"""select id, name_fold from {E} where publish_state = 'published' {frag} and name_fold like '%%' || %(q)s || '%%'
                     order by static_score desc limit 25""", {"q": qt})]
    if method == "wsim":
        return [(f"""select id, name_fold, word_similarity(%(q)s, name_fold) ws from {E} where publish_state = 'published' {frag}
                     and %(q)s <%% name_fold order by ws desc, static_score desc limit 25""", {"q": qt})]
    if method == "tsv":
        return [(f"""select id, name_fold from (select id, name_fold, static_score from {E} where publish_state = 'published' {frag}
                     and tsv @@ to_tsquery('simple', %(t)s) order by static_score desc limit {CAND}) c
                     order by word_similarity(%(q)s, name_fold) * 0.6 + static_score / 1e6 * 0.4 desc limit 25""",
                 {"t": tsq(q["words"]), "q": qt})]
    if method == "tsvrank":
        return [(f"""select id, name_fold from {E} where publish_state = 'published' {frag} and tsv @@ to_tsquery('simple', %(t)s)
                     order by ts_rank(tsv, to_tsquery('simple', %(t)s)) desc limit 25""", {"t": tsq(q["words"])})]
    if method == "btree":
        return [(f"""select id, name_fold from {E} where publish_state = 'published' {frag} and name_fold like %(q)s || '%%'
                     order by static_score desc limit 25""", {"q": qt})]
    if method == "dict":
        return [("DICT", {"words": q["words"]}), (f"""select id, name_fold from {E} where publish_state = 'published' {frag}
                     and tsv @@ to_tsquery('simple', %(t)s) order by static_score desc limit 25""", {})]
    raise ValueError(method)

def run_query(method, q, frag, pr):
    """execute steps, return (ms, rows list)"""
    steps = sql_for(method, q, frag)
    t0 = time.perf_counter(); rows = []
    for sql, p in steps:
        if sql == "DICT":
            alts = []
            for w in p["words"]:
                cur.execute(f"select word from {W} where word %% %(w)s order by similarity(word, %(w)s) desc, df desc limit 3", {"w": w})
                got = [r[0] for r in cur.fetchall()] or [w]
                alts.append("(" + " | ".join(re.sub(r"[^\w]", "", g) for g in got) + ")")
            steps[1][1]["t"] = " & ".join(alts)
            continue
        p = dict(p); p.update(pr)
        cur.execute(sql, p); rows = cur.fetchall()
    return (time.perf_counter() - t0) * 1000, rows

def explain_one(method, q, frag, pr):
    steps = sql_for(method, q, frag)
    sql, p = steps[-1]
    if sql == "DICT": return ""
    p = dict(p); p.update(pr)
    if method == "dict": p["t"] = tsq(q["words"], prefix_last=False)
    try:
        cur.execute("explain (costs off) " + sql, p)
        return "\n".join(r[0] for r in cur.fetchall())
    except Exception as ex:
        return f"explain failed: {ex}"

# ---------- cells ----------
SCOPES = ["unscoped", "country", "city", "area", "city_concept", "city_nocc", "area_nocc"]
CELLS = []
for sc in SCOPES:
    nocc = sc.endswith("_nocc")
    for cls in ["common", "mid", "rare", "two"]:
        ms = ["repo", "like", "tsv"] if not nocc else ["repo", "tsv"]
        if sc in ("unscoped", "country"): ms.append("tsvrank")
        if sc in ("unscoped", "country", "city") and cls == "common": ms.append("wsim")
        for m in ms: CELLS.append((sc, cls, m))
    for m in ["repo", "wsim", "dict"]: CELLS.append((sc, "typo", m))
    for m in ["btree", "like", "tsv"]: CELLS.append((sc, "prefix", m))
only = [x for x in a.only.split(",") if x]
if only:
    CELLS = [c for c in CELLS if any(o in ":".join(c) for o in only)]

# warm the cache with a sweep of the indexes (cold start is a separate, unmeasured case)
cur.execute(f"select count(*) from {E} where tsv @@ to_tsquery('simple','hotel')")
out_path = a.out or f"results/search_{a.scale}.jsonl"
outf = open(out_path, "a")
pool_cache = {}
for (sc, cls, method) in CELLS:
    # build the query set for this (scope, class); reuse across methods so methods see identical queries
    key = (sc.replace("_nocc", ""), cls)
    if key not in pool_cache:
        qs = []
        tries = 0
        while len(qs) < a.n and tries < a.n * 8:
            tries += 1
            kind = key[0]
            path, cc, cids = pick_scope(kind)
            rows = sample_names(kind, path, cc, cids, 40)
            q = make_query(cls, rows)
            if q: q.update(path=path, cc=cc, cids=cids); qs.append(q)
        pool_cache[key] = qs
    qs = pool_cache[key]
    if not qs:
        continue
    lat, rowsn, scr, hits, timeouts = [], [], [], [], 0
    plan = ""
    t_cell = time.time()
    for i, q in enumerate(qs):
        frag, pr = scope_sql(sc, q["path"], q["cc"], q["cids"])
        if sc.endswith("_nocc"): pass
        if i == 0: plan = explain_one(method, q, frag, pr)
        try:
            ms, rows = run_query(method, q, frag, pr)
        except psycopg.errors.QueryCanceled:
            ms, rows = a.timeout_ms, []; timeouts += 1
        if i < 3: continue          # warm-up queries are not counted
        lat.append(ms); rowsn.append(len(rows)); scr.append(q["script"])
        if cls == "typo":
            hits.append(any(q["orig"] in r[1].split() for r in rows))
        if time.time() - t_cell > 120 and len(lat) >= 30: break  # slow cell: stop after 2 minutes with at least 30 samples
    arr = np.array(lat)
    rec = dict(scale=a.scale, rows=N, scope=sc, cls=cls, method=method, n=len(lat), p50=round(float(np.percentile(arr, 50)), 2),
               p95=round(float(np.percentile(arr, 95)), 2), p99=round(float(np.percentile(arr, 99)), 2), max=round(float(arr.max()), 1),
               mean=round(float(arr.mean()), 2), timeouts=timeouts, mean_rows=round(statistics.mean(rowsn), 1),
               zero_rows=round(sum(1 for r in rowsn if r == 0) / len(rowsn), 3))
    if hits: rec["typo_recall25"] = round(sum(hits) / len(hits), 3)
    by = {}
    for s in ("la", "ru", "ur"):
        v = [l for l, x in zip(lat, scr) if x == s]
        if len(v) >= 10: by[s] = [round(float(np.percentile(v, 50)), 2), round(float(np.percentile(v, 95)), 2), len(v)]
    rec["by_script_p50_p95_n"] = by
    rec["plan"] = plan
    outf.write(json.dumps(rec, ensure_ascii=False) + "\n"); outf.flush()
    print(f"{a.scale} {sc:13s}{cls:7s}{method:8s} n={rec['n']:3d} p50={rec['p50']:8.2f} p95={rec['p95']:8.2f} max={rec['max']:8.1f} rows={rec['mean_rows']:5.1f} to={timeouts}"
          + (f" recall={rec['typo_recall25']}" if hits else ""), flush=True)
