"""ESCI-style labelling rules and ranking metrics for the AllLists search evaluation.

Library plus self test:  python esci_eval.py --selftest
Metrics: NDCG@k with linear gains (DCG = sum gain_i / log2(i + 1)), MRR, precision@k of E, zero-result rate.
Gain sets: STRICT is the Amazon KDD Cup 2022 setting (E 1.0, S 0.1, C 0.01, I 0.0; reported, see the note);
TOLERANT (E 1.0, S 0.5, C 0.1, I 0.0) is our proposal for a directory where a nearby or adjacent result still helps.
"""
import csv, math, sys

STRICT = {"E": 1.0, "S": 0.1, "C": 0.01, "I": 0.0}
TOLERANT = {"E": 1.0, "S": 0.5, "C": 0.1, "I": 0.0}

def dcg(labels, gains, k=10):
    return sum(gains[l] / math.log2(i + 2) for i, l in enumerate(labels[:k]))

def ndcg(ranked_labels, all_labels, gains, k=10):
    """ranked_labels: labels of the returned list in order. all_labels: labels of every judged document for the query
    (the ideal list is built from these, so un-retrieved good documents lower the score)."""
    ideal = sorted(all_labels, key=lambda l: -gains[l])
    d = dcg(ideal, gains, k)
    return dcg(ranked_labels, gains, k) / d if d > 0 else None   # None: no good document exists, query excluded

def mrr(ranked_labels):
    for i, l in enumerate(ranked_labels, 1):
        if l == "E": return 1.0 / i
    return 0.0

def precision_e(ranked_labels, k=10):
    top = ranked_labels[:k]
    return sum(1 for l in top if l == "E") / max(1, len(top))

def load_seed(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def _under(path, prefixes):
    return any(path == p or path.startswith(p + ".") for p in prefixes if p)

def _concept_in(slug, wanted):
    return any(slug == w or slug.startswith(w + ".") for w in wanted if w)

def label_entry(entry, q):
    """entry: dict(concept_slug, place_path, name_fold, closed, published). q: a seed row. Returns E, S, C or I.
    Rules: not published or closed -> I. must_terms (brand queries) not all in the name -> I.
    E: concept under an exact concept AND place under the exact place. S: exact concept in the substitute place (same
    province), or a substitute concept in the exact place. C: complement concept in the exact or substitute place."""
    if entry.get("closed") or not entry.get("published", True): return "I"
    name = entry["name_fold"]
    must = [t for t in q["must_terms"].split("|") if t]
    if must and not all(t in name for t in " ".join(must).split()): return "I"
    ex_c = q["exact_concepts"].split("|"); sub_c = q["substitute_concepts"].split("|"); comp_c = q["complement_concepts"].split("|")
    ex_p = q["exact_places"].split("|"); sub_p = q["substitute_places"].split("|")
    c, p = entry["concept_slug"], entry["place_path"]
    if _concept_in(c, ex_c) and _under(p, ex_p): return "E"
    if (_concept_in(c, ex_c) and _under(p, sub_p)) or (_concept_in(c, sub_c) and _under(p, ex_p)): return "S"
    if _concept_in(c, comp_c) and _under(p, sub_p): return "C"
    return "I"

def selftest():
    g = STRICT
    # perfect list
    assert abs(ndcg(list("EEE"), list("EEEI"), g) - 1.0) < 1e-9
    # hand computed: ideal [E,E,S] dcg = 1 + 1/log2(3) + 0.1/2 ; got [S,E,E]
    got = 0.1 / math.log2(2) + 1 / math.log2(3) + 1 / math.log2(4)
    ideal2 = 1 + 1 / math.log2(3) + 1 / math.log2(4)
    assert abs(ndcg(list("SEE"), list("EEE"), g) - got / ideal2) < 1e-9
    assert ndcg(list("III"), list("III"), g) is None
    assert abs(mrr(list("SIE")) - 1 / 3) < 1e-9 and mrr(list("SSS")) == 0.0
    assert precision_e(list("EESIIEEEEE")) == 0.7
    # worse ranking never scores higher than better ranking
    assert ndcg(list("IIE"), list("EII"), g) < ndcg(list("EII"), list("EII"), g)
    q = dict(must_terms="", exact_concepts="hotels", exact_places="pk.punjab.lahore", substitute_concepts="", substitute_places="pk.punjab",
             complement_concepts="")
    e = dict(concept_slug="hotels.budget", place_path="pk.punjab.lahore.dha", name_fold="x hotel", closed=False, published=True)
    assert label_entry(e, q) == "E"
    assert label_entry({**e, "place_path": "pk.punjab.multan"}, q) == "S"
    assert label_entry({**e, "place_path": "pk.sindh.karachi"}, q) == "I"
    assert label_entry({**e, "closed": True}, q) == "I"
    assert label_entry({**e, "concept_slug": "schools"}, q) == "I"
    qn = {**q, "must_terms": "pearl continental"}
    assert label_entry({**e, "name_fold": "pearl continental hotel"}, qn) == "E" and label_entry(e, qn) == "I"
    print("esci_eval selftest ok")

if __name__ == "__main__":
    if "--selftest" in sys.argv: selftest()
    else: print(__doc__)
