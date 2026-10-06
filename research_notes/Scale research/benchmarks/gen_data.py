"""Generate the synthetic entries for the search benchmark and load them into a bench_* database with COPY.

Usage: python gen_data.py --db bench_search --rows 5000000 [--socket-dir DIR --port 5544]
Refuses to run against any database whose name does not start with 'bench_'.
Tables created: place, concept, concept_closure, entry_5m, variant_5m (the 1M tables are cut from these later).
"""
import argparse, math, random, sys, time
import numpy as np
import psycopg
from bench_vocab import PAIRS, EN_BRANDS, NOUNS, PILOT_NOUNS, SYLL, PK_CITIES
from textfold_copy import fold

ap = argparse.ArgumentParser()
ap.add_argument("--db", required=True)
ap.add_argument("--rows", type=int, default=5_000_000)
ap.add_argument("--socket-dir", default="/var/lib/postgresql/bench_pg16")
ap.add_argument("--port", type=int, default=5544)
ap.add_argument("--chunk", type=int, default=250_000)
ap.add_argument("--seed", type=int, default=20261006)
a = ap.parse_args()
if not a.db.startswith("bench_"):
    sys.exit("refusing: database name must start with bench_")
rng = np.random.default_rng(a.seed)
random.seed(a.seed)

# ---------- places ----------
COUNTRIES = {"pk": 55, "in": 12, "ae": 8, "us": 8, "sa": 7, "gb": 6, "bd": 2, "tr": 2}
AREA_NAMES = "dha gulberg saddar model-town johar-town clifton north-nazimabad cantt civil-lines satellite-town blue-area".split()
places = []  # (path, level, country, weight)
def add_city(cc, region, city, w_city):
    n_areas = max(4, int(3 + 6 * w_city ** 0.8))
    ws = np.array([1 / (i + 1) ** 0.9 for i in range(n_areas)])
    ws = ws / ws.sum()
    cpath = f"{cc}.{region}.{city}"
    places.append((cpath, "city", cc, w_city * 0.08))          # 8% of the city's entries sit at city level
    for i in range(n_areas):
        nm = AREA_NAMES[i] if i < len(AREA_NAMES) else f"area{i:03d}"
        places.append((f"{cpath}.{nm}", "area", cc, w_city * 0.92 * ws[i]))
pk_w = sum(w for _, _, w in PK_CITIES)
tail_towns = [(["punjab", "sindh", "kpk", "balochistan"][i % 4], f"town{i:03d}", 0.12 / (1 + i / 10)) for i in range(70)]
tot_pk = pk_w + sum(w for _, _, w in tail_towns)
for prov, city, w in PK_CITIES + tail_towns:
    add_city("pk", prov, city, COUNTRIES["pk"] * w / tot_pk)
for cc in COUNTRIES:
    if cc == "pk":
        continue
    for r in range(3):
        for c in range(6):
            add_city(cc, f"r{r}", f"c{r}{c}", COUNTRIES[cc] / 18 * (1.0 / (1 + c * 0.35)) * 1.6)
pw = np.array([p[3] for p in places]); pw = pw / pw.sum()
print("places", len(places), "leaf areas", sum(1 for p in places if p[1] == "area"))
sialkot_ids = np.array([i for i, p in enumerate(places) if p[0].startswith("pk.punjab.sialkot")])

# ---------- concepts ----------
concepts = []  # (id, slug, path, depth, parent_id, weight)
def addc(slug, path, parent, w):
    cid = len(concepts) + 1
    concepts.append([cid, slug, path, path.count(".") + 1, parent, w, None])
    return cid
fam_w = [1 / (i + 1) ** 0.75 for i in range(46)]
fam_w = [w / sum(fam_w) * 0.80 for w in fam_w]
c_hotels = addc("hotels", "hotels", None, 0.01)
for s in ["budget", "guest-houses", "business", "resorts"]:
    addc(s, f"hotels.{s}", c_hotels, 0.005)
c_schools = addc("schools", "schools", None, 0.01)
for s in ["primary", "montessori", "o-level", "girls", "boys"]:
    addc(s, f"schools.{s}", c_schools, 0.006)
c_plumb = addc("plumbers", "plumbers", None, 0.012)
addc("emergency", "plumbers.emergency", c_plumb, 0.003)
c_mfg = addc("manufacturing", "manufacturing", None, 0.0)
c_surg = addc("surgical-instruments", "manufacturing.surgical-instruments", c_mfg, 0.0006)
surg_children = [addc(s, f"manufacturing.surgical-instruments.{s}", c_surg, 0.0002)
                 for s in ["forceps", "scissors", "needle-holders", "scalpels", "retractors", "dental", "orthopaedic", "kits"]]
fam_roots = []
for f in range(43):
    fr = addc(f"fam{f:02d}", f"fam{f:02d}", None, fam_w[f] * 0.15)
    fam_roots.append(fr)
    nchild = 8 + (f * 7) % 9
    cw = [1 / (i + 1) ** 0.9 for i in range(nchild)]
    cw = [x / sum(cw) for x in cw]
    for i in range(nchild):
        addc(f"t{i:02d}", f"fam{f:02d}.t{i:02d}", fr, fam_w[f] * 0.85 * cw[i])
cw = np.array([c[5] for c in concepts]); cw = cw / cw.sum()
cid_arr = np.array([c[0] for c in concepts])
print("concepts", len(concepts))
# pilot noun table: concept id -> family key
pilot_key = {}
for c in concepts:
    for k, root in (("hotels", "hotels"), ("schools", "schools"), ("plumbers", "plumbers"),
                    ("surgical", "manufacturing.surgical-instruments")):
        if c[2] == root or c[2].startswith(root + "."):
            pilot_key[c[0]] = k
generic_nouns = {c[0]: [random.randrange(len(NOUNS)), random.randrange(len(NOUNS))] for c in concepts}

# ---------- vocabulary (folded once) ----------
PR = [fold(r) for r, _ in PAIRS]; PU = [fold(u) for _, u in PAIRS]
EB = [fold(b) for b in EN_BRANDS]
SYR = [s for s, _ in SYLL]; SYU = [fold(u).replace(" ", "") for _, u in SYLL]
NPOOL = 300000
sur_r, sur_u = [], []
for i in range(NPOOL):
    k = 2 + (i % 3 == 0) + (i % 7 == 0)
    ix = [random.randrange(len(SYLL)) for _ in range(k)]
    sur_r.append("".join(SYR[j] for j in ix)); sur_u.append("".join(SYU[j] for j in ix))
CITY_EN = [fold(p[1]) for p in PAIRS[-30:-10]]

def zipf(n, size, k):
    return np.minimum((n * rng.random(size) ** k).astype(np.int64), n - 1)

def noun_tokens(cid, which, r):
    """which: 0 english, 1 roman, 2 urdu."""
    pk = pilot_key.get(cid)
    if pk:
        lst = PILOT_NOUNS[pk][which]
        return fold(lst[r % len(lst)])
    ix = generic_nouns[cid][r % 2]
    return fold(NOUNS[ix][which])

def build_chunk(start, n):
    pidx = rng.choice(len(places), size=n, p=pw)
    cidx = rng.choice(len(concepts), size=n, p=cw)
    is_sialkot = np.isin(pidx, sialkot_ids)
    surg_mask = is_sialkot & (rng.random(n) < 0.12)
    surg_pick = np.array(surg_children)[rng.integers(0, len(surg_children), n)]
    # concept ids
    cids = cid_arr[cidx].copy()
    cids[surg_mask] = surg_pick[surg_mask]
    cc_codes = np.array([p[2] for p in places])[pidx]
    r = rng.random(n)
    pk_row = cc_codes == "pk"
    script = np.where(pk_row, np.where(r < 0.45, 0, np.where(r < 0.83, 1, 2)), np.where(r < 0.9, 0, np.where(r < 0.95, 1, 2)))
    pat = rng.integers(0, 7, n)
    b1 = zipf(len(PAIRS), n, 2.0); b2 = zipf(len(PAIRS), n, 2.0)
    e1 = zipf(len(EB), n, 1.8); e2 = zipf(len(EB), n, 1.8)
    sur = zipf(NPOOL, n, 2.2)
    nr = rng.integers(0, 6, n)
    use_city = rng.random(n) < 0.08
    ci = rng.integers(0, len(CITY_EN), n)
    var_flag = rng.random(n) < 0.5
    # quality attributes
    lv = rng.choice(4, size=n, p=[0.60, 0.30, 0.07, 0.03])
    age = np.where(lv > 0, rng.exponential(150, n).astype(int), -1)
    comp = np.clip(rng.beta(2, 2, n) * 100, 0, 100).astype(int)
    stale = (age > 365) | (age < 0)
    closed = rng.random(n) < (0.03 + 0.07 * (lv == 0) + 0.05 * stale)
    pub = rng.random(n) < 0.92
    rows, vrows = [], []
    for i in range(n):
        cid = int(cids[i]); s = int(script[i]); p = int(pat[i]); eid = start + i
        sv = None
        if s == 0:
            b = EB[e1[i]]; b_ = EB[e2[i]]; nn = noun_tokens(cid, 0, int(nr[i]))
            sn = sur_r[sur[i]]
            if p == 0 or p == 5: nm = f"{b} {nn}"
            elif p == 1: nm = f"the {b} {nn}"
            elif p == 2: nm = f"{sn} and sons {nn}"
            elif p == 3: nm = f"{b} {b_} {nn}"
            elif p == 4: nm = f"{b} {nn} {sn}"
            else: nm = f"{CITY_EN[ci[i]]} {b} {nn}"
            if use_city[i] and p != 6: nm = f"{CITY_EN[ci[i]]} {nm}"
        else:
            # Roman Urdu (1) or Urdu (2), same plan rendered in both scripts
            W = PR if s == 1 else PU; Wo = PU if s == 1 else PR
            S = sur_r if s == 1 else sur_u; So = sur_u if s == 1 else sur_r
            nn = noun_tokens(cid, s, int(nr[i])); nno = noun_tokens(cid, 3 - s, int(nr[i]))
            BR = ("brothers" if s == 1 else "برادرز"); BRo = ("برادرز" if s == 1 else "brothers")
            AL = "al" if s == 1 else "ال"; ALo = "ال" if s == 1 else "al"
            def render(W, S, nn, BR, AL):
                if p == 0: return f"{W[b1[i]]} {nn}"
                if p == 1: return f"{nn} {W[b1[i]]}"
                if p == 2: return f"{W[b1[i]]} {W[b2[i]]} {nn}"
                if p == 3: return f"{S[sur[i]]} {BR} {nn}"
                if p == 4: return f"{AL} {W[b1[i]]} {nn}"
                if p == 5: return f"{nn} {AL} {W[b1[i]]}"
                return f"{S[sur[i]]} {nn}"
            nm = render(W, S, nn, BR, AL)
            if var_flag[i]:
                sv = render(Wo, So, nno, BRo, ALo)
        nm = " ".join(nm.split())
        rows.append((eid, places[pidx[i]][2], places[pidx[i]][0], cid, "published" if pub[i] else "draft", nm,
                     ("la", "ru", "ur")[s], int(lv[i]), int(age[i]), int(comp[i]), "t" if closed[i] else "f"))
        if sv:
            vrows.append((eid, " ".join(sv.split())))
    return rows, vrows

with psycopg.connect(f"host={a.socket_dir} port={a.port} dbname={a.db} user=postgres", autocommit=True) as con:
    cur = con.cursor()
    cur.execute("""drop table if exists variant_5m, entry_5m, concept_closure, concept, place cascade;
    create table place(id serial primary key, path text not null, level text, country_code text);
    create table concept(id int primary key, slug text, path text, depth int, parent_id int);
    create table concept_closure(ancestor_id int, descendant_id int, primary key(ancestor_id, descendant_id));
    create table entry_5m(id bigint, country_code text, place_path text, concept_id int, publish_state text, name_fold text,
        script text, level smallint, verified_age_days int, completeness smallint, closed boolean);
    create table variant_5m(entry_id bigint, text_fold text);""")
    with cur.copy("copy place(path, level, country_code) from stdin") as cp:
        for p in places: cp.write_row((p[0], p[1], p[2]))
    with cur.copy("copy concept from stdin") as cp:
        for c in concepts: cp.write_row((c[0], c[1], c[2], c[3], c[4]))
    byid = {c[0]: c for c in concepts}
    with cur.copy("copy concept_closure from stdin") as cp:
        for c in concepts:
            x = c[0]
            while x is not None:
                cp.write_row((x, c[0])); x = byid[x][4]
    t0 = time.time(); done = 0
    while done < a.rows:
        n = min(a.chunk, a.rows - done)
        rows, vrows = build_chunk(done + 1, n)
        with cur.copy("copy entry_5m from stdin") as cp:
            for r in rows: cp.write_row(r)
        with cur.copy("copy variant_5m from stdin") as cp:
            for v in vrows: cp.write_row(v)
        done += n
        print(f"{done:>9,} rows  {time.time()-t0:6.1f}s", flush=True)
print("done")
