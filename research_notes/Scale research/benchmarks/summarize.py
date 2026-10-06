"""Print markdown tables from results/*.json(l) for the note. Usage: python summarize.py"""
import json, glob, os
H = os.path.dirname(os.path.abspath(__file__)) + "/results/"
def jl(p): return [json.loads(l) for l in open(p)] if os.path.exists(p) else []
print("## index sizes and build times")
for sc in ("1m", "5m"):
    p = H + f"build_{sc}.json"
    if not os.path.exists(p): continue
    b = json.load(open(p)); po = json.load(open(H + f"post_{sc}.json")) if os.path.exists(H + f"post_{sc}.json") else {}
    mb = lambda x: round(x / 1e6, 1)
    st = b["steps"]
    print(f"{sc}: heap_without_tsv={mb(b['heap_bytes_before_tsv'])}MB heap_with_tsv={mb(b['heap_bytes_with_tsv'])}MB variant_heap={mb(b['variant_heap_bytes'])}MB")
    for k in ("heap_pk", "btree_list_query", "btree_name_prefix", "gin_trgm_name", "gin_tsv", "variant_btree", "variant_gin_trgm"):
        print(f"   {k:20s} {mb(st[k]['bytes']):8} MB  {st[k]['seconds']:6} s")
    if po:
        for k in ("idx_score_partial", "words_gin"):
            if k in po: print(f"   {k:20s} {mb(po[k]['bytes']):8} MB  {po[k]['seconds']:6} s")
        print("   distinct words", po.get("distinct_words"), "words heap MB", mb(po.get("words_heap_bytes", 0)))
for sc in ("1m", "5m"):
    rows = jl(H + f"search_{sc}.jsonl")
    if not rows: continue
    print(f"\n## latency {sc}  (p50 / p95 ms)")
    scopes = []; 
    for r in rows:
        if r["scope"] not in scopes: scopes.append(r["scope"])
    for s in scopes:
        print(f"\n### {sc} {s}")
        for r in rows:
            if r["scope"] != s: continue
            extra = f" recall25={r['typo_recall25']}" if "typo_recall25" in r else ""
            to = f" TIMEOUTS={r['timeouts']}" if r["timeouts"] else ""
            print(f"| {r['cls']:7s}| {r['method']:8s}| {r['p50']:8.2f} / {r['p95']:8.2f} | p99 {r['p99']:8.1f} | n={r['n']} rows={r['mean_rows']}{extra}{to}")
