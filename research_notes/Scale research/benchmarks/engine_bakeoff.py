"""Small real bake-off: the same documents and queries against Meilisearch, Typesense, OpenSearch and Postgres (1M docs).

Usage:
  python engine_bakeoff.py --make-queries                        # sample queries once from bench_search.entry_1m
  python engine_bakeoff.py --engine postgres|meilisearch|typesense|opensearch [--docs 1000000]
Engines are started by run_engines.sh (binaries extracted from the vendors' public container images; see note 07).
Read-only on Postgres. Refuses databases not starting with bench_. Everything listens on 127.0.0.1 only.
Query classes: common, mid, two (first two words), typo (one edit), prefix (2 to 4 letters); scopes: unscoped and list (city + list type).
"""
import argparse, http.client, json, os, random, re, sys, time
import numpy as np, psycopg

ap = argparse.ArgumentParser()
ap.add_argument("--engine", default="")
ap.add_argument("--make-queries", action="store_true")
ap.add_argument("--docs", type=int, default=1_000_000)
ap.add_argument("--db", default="bench_search")
ap.add_argument("--n", type=int, default=100)
ap.add_argument("--pid", type=int, default=0, help="server pid for RSS reading")
ap.add_argument("--data-dir", default="", help="engine data dir for disk size")
ap.add_argument("--socket-dir", default="/var/lib/postgresql/bench_pg16"); ap.add_argument("--port", type=int, default=5544)
a = ap.parse_args()
if not a.db.startswith("bench_"): sys.exit("refusing: database name must start with bench_")
HERE = os.path.dirname(os.path.abspath(__file__))
QFILE = os.path.join(HERE, "results", "engine_queries_1m.json")
con = psycopg.connect(f"host={a.socket_dir} port={a.port} dbname={a.db} user=postgres", autocommit=True); cur = con.cursor()
cur.execute("set pg_trgm.word_similarity_threshold = 0.4; set statement_timeout = 5000")
rnd = random.Random(11)

def prefixes(path): 
    p = path.split("."); return [".".join(p[:i]) for i in range(1, len(p) + 1)]

if a.make_queries:
    cur.execute("select word, df from words_1m"); df = dict(cur.fetchall())
    top = {w for w, _ in sorted(df.items(), key=lambda t: -t[1])[:25]}
    N = 1_000_000
    def wclass(w):
        d = df.get(w, 0)
        return "common" if w in top else ("mid" if 200 <= d <= 5000 else ("rare" if d <= 30 else "other"))
    def typo(w):
        i = rnd.randrange(1, len(w) - 1); op = rnd.choice("sdt")
        if op == "s": return w[:i] + rnd.choice("abcdefghilmnoprstu" if w.isascii() else "اسنرمتلکب") + w[i + 1:]
        if op == "d": return w[:i] + w[i + 1:]
        return w[:i] + w[i + 1] + w[i] + w[i + 2:]
    cur.execute("select place_path, count(*) from entry_1m where publish_state='published' group by 1 having count(*) >= 30"); leaf = cur.fetchall()
    city = {}
    for p, n in leaf: c = ".".join(p.split(".")[:3]); city[c] = city.get(c, 0) + n
    cities = sorted(city.items(), key=lambda t: -t[1])[:60]
    cur.execute("select id, path from concept"); cpath = dict(cur.fetchall())
    out = []
    for scope in ("unscoped", "list"):
        for cls in ("common", "mid", "two", "typo", "prefix"):
            got = 0; tries = 0
            while got < a.n and tries < 4000:
                tries += 1
                if scope == "unscoped":
                    cur.execute("select id, name_fold, script from entry_1m where id = any(%s) and publish_state='published' limit 20", [[rnd.randrange(1, N + 1) for _ in range(40)]])
                    path = None; root = None
                else:
                    path = rnd.choices([c for c, _ in cities], [n for _, n in cities])[0]
                    cur.execute("""select e.id, e.name_fold, e.script, c.path from entry_1m e join concept c on c.id = e.concept_id
                                   where e.country_code = %s and e.place_path like %s and e.publish_state='published' and e.id > %s order by e.id limit 60""",
                                [path.split(".")[0], path + "%", rnd.randrange(1, N)])
                rows = cur.fetchall()
                if not rows: continue
                r = rnd.choice(rows); ws = r[1].split()
                q = None
                if cls in ("common", "mid"):
                    c = [w for w in ws if wclass(w) == cls and len(w) >= 3]
                    if c: q = c[0]
                elif cls == "two" and len(ws) >= 2: q = " ".join(ws[:2])
                elif cls == "typo":
                    c = [w for w in ws if len(w) >= 5 and wclass(w) in ("mid", "rare", "other")]
                    if c: w = rnd.choice(c); q = typo(w)
                elif cls == "prefix" and len(ws[0]) >= 3: q = ws[0][:min(len(ws[0]) - 1, rnd.choice([2, 3, 4]))]
                if q is None: continue
                d = dict(scope=scope, cls=cls, q=q, script=r[2], eid=r[0], place=path)
                if scope == "list": d["concept"] = r[3].split(".")[0]
                if cls == "typo": d["orig"] = w
                out.append(d); got += 1
    json.dump(out, open(QFILE, "w"), ensure_ascii=False); print("queries", len(out)); sys.exit()

queries = json.load(open(QFILE))
cur.execute("select id, path from concept"); CPATH = dict(cur.fetchall())
def docs_iter(limit):
    c2 = con.cursor(name="docs"); 
    c2.execute("select id, name_fold, country_code, place_path, concept_id, level, static_score, script from entry_1m where publish_state='published' order by id limit %s", [limit])
    for r in c2:
        cp = CPATH[r[4]]
        yield {"id": str(r[0]), "name": r[1], "country": r[2], "place_anc": prefixes(r[3]), "concept_anc": prefixes(cp), "level": r[5], "score": r[6], "script": r[7]}

class H:
    def __init__(self, port): self.c = http.client.HTTPConnection("127.0.0.1", port, timeout=120)
    def req(self, m, path, body=None, headers=None, raw=False):
        hd = {"Content-Type": "application/json"}; hd.update(headers or {})
        data = body if isinstance(body, (bytes, str)) else (json.dumps(body, ensure_ascii=False).encode() if body is not None else None)
        if isinstance(data, str): data = data.encode()
        self.c.request(m, path, data, hd); r = self.c.getresponse(); t = r.read()
        if r.status >= 300 and not raw: raise RuntimeError(f"{m} {path} -> {r.status} {t[:300]}")
        return t if raw else (json.loads(t) if t else {})

def rss_mb(pid):
    if not pid: return None
    for l in open(f"/proc/{pid}/status"):
        if l.startswith("VmRSS"): return round(int(l.split()[1]) / 1024)
def du(path):
    if not path: return None
    tot = 0
    for r, _, fs in os.walk(path):
        for f in fs:
            try: tot += os.path.getsize(os.path.join(r, f))
            except OSError: pass
    return round(tot / 1e6)

res = {"engine": a.engine, "docs": a.docs}
# ------------------------------------------------------------------ engines
if a.engine == "meilisearch":
    h = H(7700); hd = {}
    h.req("DELETE", "/indexes/entries", raw=True); time.sleep(1)
    h.req("POST", "/indexes", {"uid": "entries", "primaryKey": "id"})
    h.req("PATCH", "/indexes/entries/settings", {"filterableAttributes": ["country", "place_anc", "concept_anc", "level", "script"], "sortableAttributes": ["score"],
          "searchableAttributes": ["name"], "rankingRules": ["words", "typo", "proximity", "attribute", "sort", "exactness"], "pagination": {"maxTotalHits": 1000}})
    t0 = time.time(); batch = []; last = None
    for d in docs_iter(a.docs):
        batch.append(d)
        if len(batch) >= 100_000:
            last = h.req("POST", "/indexes/entries/documents", "\n".join(json.dumps(x, ensure_ascii=False) for x in batch), headers={"Content-Type": "application/x-ndjson"})["taskUid"]; batch = []
    if batch: last = h.req("POST", "/indexes/entries/documents", "\n".join(json.dumps(x, ensure_ascii=False) for x in batch), headers={"Content-Type": "application/x-ndjson"})["taskUid"]
    while h.req("GET", f"/tasks/{last}")["status"] in ("enqueued", "processing"): time.sleep(2)
    st = h.req("GET", f"/tasks/{last}")["status"]; res["index_seconds"] = round(time.time() - t0, 1); res["last_task_status"] = st
    def search(q):
        body = {"q": q["q"], "limit": 25, "sort": ["score:desc"] if False else None}
        body = {"q": q["q"], "limit": 25, "attributesToRetrieve": ["id", "name"], "facets": ["level"]}
        if q["scope"] == "list": body["filter"] = f'place_anc = "{q["place"]}" AND concept_anc = "{q["concept"]}" AND country = "{q["place"].split(".")[0]}"'
        r = h.req("POST", "/indexes/entries/search", body); return [x["name"] for x in r["hits"]]
elif a.engine == "typesense":
    h = H(8108); hd = {"X-TYPESENSE-API-KEY": "bench"}
    h.req("DELETE", "/collections/entries", headers=hd, raw=True)
    h.req("POST", "/collections", {"name": "entries", "fields": [{"name": "name", "type": "string"}, {"name": "country", "type": "string", "facet": True},
          {"name": "place_anc", "type": "string[]", "facet": True}, {"name": "concept_anc", "type": "string[]", "facet": True},
          {"name": "level", "type": "int32", "facet": True}, {"name": "script", "type": "string", "facet": True}, {"name": "score", "type": "int64"}],
          "default_sorting_field": "score"}, headers=hd)
    t0 = time.time(); batch = []
    def flush():
        r = h.req("POST", "/collections/entries/documents/import?action=create", "\n".join(json.dumps(x, ensure_ascii=False) for x in batch), headers=hd, raw=True)
        bad = r.count(b'"success":false')
        if bad: print("import failures", bad, r[:200])
    for d in docs_iter(a.docs):
        batch.append(d)
        if len(batch) >= 50_000: flush(); batch = []
    if batch: flush()
    res["index_seconds"] = round(time.time() - t0, 1)
    def search(q):
        p = {"q": q["q"], "query_by": "name", "per_page": 25, "num_typos": 2, "prefix": "true", "facet_by": "level", "sort_by": "_text_match:desc,score:desc"}
        if q["scope"] == "list": p["filter_by"] = f'place_anc:={q["place"]} && concept_anc:={q["concept"]} && country:={q["place"].split(".")[0]}'
        from urllib.parse import urlencode
        r = h.req("GET", "/collections/entries/documents/search?" + urlencode(p), headers=hd); return [x["document"]["name"] for x in r["hits"]]
elif a.engine == "opensearch":
    h = H(9200)
    h.req("DELETE", "/entries", raw=True)
    h.req("PUT", "/entries", {"settings": {"number_of_shards": 1, "number_of_replicas": 0, "refresh_interval": "-1",
          "analysis": {"analyzer": {"nm": {"type": "custom", "tokenizer": "standard", "filter": ["lowercase", "arabic_normalization", "persian_normalization"]}}}},
          "mappings": {"properties": {"name": {"type": "text", "analyzer": "nm"}, "country": {"type": "keyword"}, "place_anc": {"type": "keyword"},
                       "concept_anc": {"type": "keyword"}, "level": {"type": "byte"}, "script": {"type": "keyword"}, "score": {"type": "long"}}}})
    t0 = time.time(); batch = []
    def flush():
        lines = []
        for d in batch: lines.append(json.dumps({"index": {"_id": d["id"]}})); lines.append(json.dumps({k: v for k, v in d.items() if k != "id"}, ensure_ascii=False))
        r = h.req("POST", "/entries/_bulk", "\n".join(lines) + "\n", headers={"Content-Type": "application/x-ndjson"})
        if r.get("errors"): print("bulk errors")
    for d in docs_iter(a.docs):
        batch.append(d)
        if len(batch) >= 10_000: flush(); batch = []
    if batch: flush()
    h.req("PUT", "/entries/_settings", {"index": {"refresh_interval": "1s"}}); h.req("POST", "/entries/_refresh")
    res["index_seconds_before_merge"] = round(time.time() - t0, 1)
    h.req("POST", "/entries/_forcemerge?max_num_segments=1", raw=True); res["index_seconds"] = round(time.time() - t0, 1)
    def search(q):
        words = q["q"].split()
        must = {"match": {"name": {"query": q["q"], "fuzziness": "AUTO", "operator": "and"}}} if q["cls"] == "typo" else (
            {"match_phrase_prefix": {"name": {"query": q["q"]}}} if q["cls"] in ("prefix",) else {"match": {"name": {"query": q["q"], "operator": "and"}}})
        flt = []
        if q["scope"] == "list": flt = [{"term": {"place_anc": q["place"]}}, {"term": {"concept_anc": q["concept"]}}, {"term": {"country": q["place"].split(".")[0]}}]
        body = {"size": 25, "_source": ["name"], "query": {"function_score": {"query": {"bool": {"must": [must], "filter": flt}},
                "field_value_factor": {"field": "score", "modifier": "log1p", "factor": 0.001, "missing": 1}, "boost_mode": "sum"}},
                "aggs": {"lv": {"terms": {"field": "level"}}}}
        r = h.req("POST", "/entries/_search", body); return [x["_source"]["name"] for x in r["hits"]["hits"]]
elif a.engine == "postgres":
    def search(q):
        sc, p = "", {}
        if q["scope"] == "list":
            cur.execute("select array_agg(descendant_id) from concept_closure where ancestor_id = (select id from concept where path = %s)", [q["concept"]]); cids = cur.fetchone()[0]
            sc = " and country_code = %(cc)s and (place_path = %(p)s or place_path like %(pl)s) and concept_id = any(%(c)s)"
            p = {"cc": q["place"].split(".")[0], "p": q["place"], "pl": q["place"] + ".%", "c": cids}
        w = re.sub(r"[^\w ]", "", q["q"]).split()
        if q["cls"] == "typo":
            alts = []
            for x in w:
                cur.execute("select word from words_1m where word % %(w)s order by similarity(word, %(w)s) desc, df desc limit 3", {"w": x}); g = [r[0] for r in cur.fetchall()] or [x]
                alts.append("(" + " | ".join(g) + ")")
            tsq = " & ".join(alts)
        else: tsq = " & ".join(w[:-1] + [w[-1] + (":*" if q["cls"] != "common" or True else "")])
        cur.execute(f"""select name_fold from (select name_fold, static_score from entry_1m where publish_state='published' {sc} and tsv @@ to_tsquery('simple', %(t)s)
                       order by static_score desc limit 200) c order by word_similarity(%(q)s, name_fold) * 0.6 + static_score / 1e6 * 0.4 desc limit 25""", dict(p, t=tsq, q=q["q"]))
        return [r[0] for r in cur.fetchall()]
else:
    sys.exit("choose --engine")

res["rss_mb_after_index"] = rss_mb(a.pid); res["disk_mb"] = du(a.data_dir)
# ------------------------------------------------------------------ queries
cells = {}
for q in queries:
    cells.setdefault((q["scope"], q["cls"]), []).append(q)
out = []
for (sc, cls), qs in cells.items():
    lat, nrows, hits, rec = [], [], 0, 0
    for i, q in enumerate(qs):
        t = time.perf_counter()
        try: names = search(q)
        except Exception as ex: names = []; print("ERR", str(ex)[:120])
        ms = (time.perf_counter() - t) * 1000
        if i < 3: continue
        lat.append(ms); nrows.append(len(names))
        if cls == "typo": rec += any(q["orig"] in n.split() for n in names)
    arr = np.array(lat)
    row = dict(engine=a.engine, scope=sc, cls=cls, n=len(lat), p50=round(float(np.percentile(arr, 50)), 2), p95=round(float(np.percentile(arr, 95)), 2),
               max=round(float(arr.max()), 1), mean_rows=round(float(np.mean(nrows)), 1), zero_rows=round(sum(1 for x in nrows if x == 0) / len(nrows), 3))
    if cls == "typo": row["typo_recall25"] = round(rec / len(lat), 3)
    out.append(row); print(row, flush=True)
res["cells"] = out; res["rss_mb_after_queries"] = rss_mb(a.pid)
json.dump(res, open(os.path.join(HERE, "results", f"engines_{a.engine}.json"), "w"), indent=1, ensure_ascii=False)
