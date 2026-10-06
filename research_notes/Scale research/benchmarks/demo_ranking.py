"""Harness proof for the ranking design: run the seed queries (structured intent, oracle query understanding) over the synthetic
1M entries, label every candidate with the ESCI rules in esci_eval.py, and compare ranking formulas by NDCG@10.

What this proves: the harness works end to end, and the mechanism (stored prior pushes closed or stale entries down).
What it does NOT prove: real-world quality. The synthetic 'closed' flag was generated to depend on verification level and
age (see gen_data.py), so a prior built from those fields will help by construction. Treat the size of the gain as an
illustration, not a forecast.
Usage: python demo_ranking.py --db bench_search   (read only; refuses databases not starting with bench_)
"""
import argparse, json, math, random, sys
import numpy as np, psycopg
from esci_eval import STRICT, TOLERANT, load_seed, label_entry, ndcg, mrr, precision_e

ap = argparse.ArgumentParser()
ap.add_argument("--db", required=True); ap.add_argument("--scale", default="1m")
ap.add_argument("--socket-dir", default="/var/lib/postgresql/bench_pg16"); ap.add_argument("--port", type=int, default=5544)
ap.add_argument("--seed-file", default="judgement_seed.csv"); ap.add_argument("--out", default="results/ranking_demo.json")
a = ap.parse_args()
if not a.db.startswith("bench_"): sys.exit("refusing: database name must start with bench_")
E = f"entry_{a.scale}"
con = psycopg.connect(f"host={a.socket_dir} port={a.port} dbname={a.db} user=postgres", autocommit=True); cur = con.cursor()
cur.execute("select id, path from concept"); slug = {i: p for i, p in cur.fetchall()}; cid = {p: i for i, p in slug.items()}
cur.execute("select ancestor_id, array_agg(descendant_id) from concept_closure group by 1"); closure = dict(cur.fetchall())
STOP = set("in mein ke ka ki ko near me the best a of for with wala wale karne ke qareeb sath se hai chahiye aur ya and".split())
PLACES = set("lahore karachi islamabad rawalpindi murree multan peshawar sialkot faisalabad gujranwala pakistan dha gulberg clifton".split())
random.seed(3)

def concept_ids(slugs):
    out = set()
    for s in slugs:
        if s in cid: out.update(closure[cid[s]])
    return list(out)

def ranker_scores(rows, q, kind):
    toks = [t for t in q["query"].lower().split() if t not in STOP and t not in PLACES]
    must = [t for t in q["must_terms"].split("|") if t]
    res = []
    for r in rows:
        name = r["name_fold"]; words = set(name.split())
        text = (sum(1 for t in toks if t in words or any(w.startswith(t[:5]) for w in words)) / len(toks)) if toks else 0.5
        if must and all(t in name for t in " ".join(must).split()): text = 1.0
        prior = r["static_score"] / 1e6 / 1000.0          # 0..1
        fresh = 0.0 if r["age"] < 0 else math.exp(-r["age"] / 365.0)
        if kind == "alpha": s = name  # alphabetical (the current list-page default order)
        elif kind == "random": s = random.random()
        elif kind == "text": s = text + 1e-6 * random.random()
        elif kind == "prior": s = prior
        elif kind == "blend_add": s = 0.35 * text + 0.65 * prior
        elif kind == "product": s = (0.15 + text) * (0.2 + prior)
        res.append(s)
    return res

rows_q = load_seed(a.seed_file)
agg = {k: {"strict": [], "tolerant": [], "mrr": [], "p10e": []} for k in ["alpha", "random", "text", "prior", "blend_add", "product"]}
per_seg = {}
skipped = 0
for q in rows_q:
    ex = [s for s in q["exact_concepts"].split("|") if s]; sub = [s for s in q["substitute_concepts"].split("|") if s]
    ids = concept_ids(ex + sub)
    if not ids: skipped += 1; continue
    prov = q["substitute_places"].split("|")[0]
    cc = prov.split(".")[0]
    cur.execute(f"""select id, name_fold, concept_id, place_path, closed, static_score, verified_age_days from {E}
                    where publish_state='published' and country_code=%s and (place_path = %s or place_path like %s) and concept_id = any(%s)""",
                [cc, prov, prov + ".%", ids])
    rows = [dict(id=r[0], name_fold=r[1], concept_slug=slug[r[2]], place_path=r[3], closed=r[4], static_score=r[5], age=r[6], published=True)
            for r in cur.fetchall()]
    if not rows: skipped += 1; continue
    labels = [label_entry(r, q) for r in rows]
    if "E" not in labels and "S" not in labels: skipped += 1; continue
    for kind in agg:
        sc = ranker_scores(rows, q, kind)
        order = sorted(range(len(rows)), key=lambda i: sc[i], reverse=(kind != "alpha"))
        rl = [labels[i] for i in order[:10]]
        for name, g in (("strict", STRICT), ("tolerant", TOLERANT)):
            v = ndcg(rl, labels, g, 10)
            if v is not None:
                agg[kind][name].append(v); per_seg.setdefault((kind, q["segment"]), []).append(v) if name == "strict" else None
        agg[kind]["mrr"].append(mrr(rl)); agg[kind]["p10e"].append(precision_e(rl))
out = {"queries_total": len(rows_q), "queries_used": len(agg["text"]["strict"]), "skipped_no_candidates": skipped, "rankers": {}, "per_segment_strict": {}}
for k, v in agg.items():
    out["rankers"][k] = {m: round(float(np.mean(x)), 4) for m, x in v.items()}
for (k, seg), v in per_seg.items():
    out["per_segment_strict"].setdefault(k, {})[seg] = round(float(np.mean(v)), 4)
json.dump(out, open(a.out, "w"), indent=1)
print(json.dumps(out, indent=1))
