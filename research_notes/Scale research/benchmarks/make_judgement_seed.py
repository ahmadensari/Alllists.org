"""Build judgement_seed.csv: the pilot seed query set (Pakistan hotels, surgical instruments Sialkot, plumbers, schools).

The file holds QUERIES and machine-readable LABEL RULES, not judged documents. Document labels (E, S, C, I) come from
(a) esci_eval.py rule labelling for synthetic checks and (b) native-speaker judges for real pooled results.
Concept slugs match the benchmark taxonomy and the proposed AllLists slugs; places are place-tree paths.
"""
import csv

H, S, P, SC = "hotels", "manufacturing.surgical-instruments", "plumbers", "schools"
PB = "pk.punjab"
CITY = {"lahore": f"{PB}.lahore", "karachi": "pk.sindh.karachi", "islamabad": "pk.islamabad.islamabad", "rawalpindi": f"{PB}.rawalpindi",
        "murree": f"{PB}.murree", "multan": f"{PB}.multan", "peshawar": "pk.kpk.peshawar", "sialkot": f"{PB}.sialkot",
        "faisalabad": f"{PB}.faisalabad", "gujranwala": f"{PB}.gujranwala", "pakistan": "pk"}
SUBP = {"pk.punjab": ["lahore", "rawalpindi", "murree", "multan", "sialkot", "faisalabad", "gujranwala"], "pk.sindh": ["karachi"],
        "pk.islamabad": ["islamabad"], "pk.kpk": ["peshawar"]}
def province(path):
    return ".".join(path.split(".")[:2]) if path != "pk" else "pk"

rows = []
def add(seg, lang, q, qtype, concept, place, ex_c=None, sub_c="", comp_c="", filt="", must="", rtype="entries", note="", sub_p=None):
    place_path = CITY.get(place, place)
    ex_c = ex_c or concept
    sub_p = province(place_path) if sub_p is None else sub_p
    rows.append(dict(query=q, segment=seg, language=lang, query_type=qtype, intent_concept=concept, intent_place=place_path,
                     result_type=rtype, exact_concepts=ex_c, exact_places=place_path, substitute_concepts=sub_c,
                     substitute_places=sub_p, complement_concepts=comp_c, facet_filters=filt, must_terms=must, notes=note))

# ---------------- hotels ----------------
seg = "hotels"
for c in ["lahore", "karachi", "islamabad", "murree", "rawalpindi", "multan", "peshawar"]:
    add(seg, "en", f"hotels in {c}", "head", H, c, note="list page intent; the list page itself should rank first among result groups", rtype="list")
add(seg, "en", "hotels in pakistan", "head", H, "pakistan", note="country scope; navigates to list page", rtype="list")
add(seg, "en", "budget hotels lahore", "torso", H, "lahore", ex_c="hotels.budget", sub_c="hotels", filt="price_band=budget")
add(seg, "en", "cheap hotels in karachi", "torso", H, "karachi", ex_c="hotels.budget", sub_c="hotels", filt="price_band=budget")
add(seg, "en", "5 star hotels islamabad", "torso", H, "islamabad", ex_c="hotels", filt="star_rating=5", note="needs structured star rating; text alone cannot satisfy")
add(seg, "en", "family hotel murree", "torso", H, "murree", ex_c="hotels", sub_c="hotels.guest-houses", filt="family_friendly=true")
add(seg, "en", "guest house islamabad", "torso", H, "islamabad", ex_c="hotels.guest-houses", sub_c="hotels")
add(seg, "en", "guest houses in lahore", "torso", H, "lahore", ex_c="hotels.guest-houses", sub_c="hotels")
add(seg, "en", "hotels near airport lahore", "torso", H, "lahore", filt="near=airport", note="needs coordinates; area names alone are a weak substitute")
add(seg, "en", "hotel with parking multan", "tail", H, "multan", filt="amenity=parking")
add(seg, "en", "business hotel karachi clifton", "tail", "hotels.business", "pk.sindh.karachi.clifton", ex_c="hotels.business", sub_c="hotels", sub_p="pk.sindh.karachi")
add(seg, "en", "hotels near gulberg lahore", "tail", H, "pk.punjab.lahore.gulberg", sub_p="pk.punjab.lahore")
add(seg, "en", "pearl continental lahore", "navigational", H, "lahore", must="pearl continental", note="brand query; exact entry first")
add(seg, "en", "serena hotel islamabad", "navigational", H, "islamabad", must="serena")
add(seg, "en", "avari hotel lahore", "navigational", H, "lahore", must="avari")
add(seg, "en", "resorts in murree", "torso", "hotels.resorts", "murree", ex_c="hotels.resorts", sub_c="hotels")
add(seg, "en", "hotels in lahor", "typo", H, "lahore", note="one-letter deletion in the place name; place lookup must recover")
add(seg, "en", "hotal lahore", "typo", H, "lahore", note="common misspelling of hotel")
add(seg, "en", "hotels sialkot", "head", H, "sialkot", note="export-buyer visitor intent; small city")
add(seg, "en", "hotels in faisalabad", "head", H, "faisalabad")
add(seg, "en", "hotels gujranwala", "head", H, "gujranwala")
# roman urdu hotels
add(seg, "roman_ur", "lahore mein hotel", "head", H, "lahore")
add(seg, "roman_ur", "karachi hotal", "typo", H, "karachi", note="spelling variant hotal")
add(seg, "roman_ur", "sasta hotel lahore", "torso", H, "lahore", ex_c="hotels.budget", sub_c="hotels", filt="price_band=budget", note="sasta = cheap")
add(seg, "roman_ur", "murree mein family hotel", "torso", H, "murree", sub_c="hotels.guest-houses", filt="family_friendly=true")
add(seg, "roman_ur", "musafir khana islamabad", "torso", "hotels.guest-houses", "islamabad", ex_c="hotels.guest-houses", sub_c="hotels", note="musafir khana = inn or lodging")
add(seg, "roman_ur", "guest house rawalpindi", "torso", H, "rawalpindi", ex_c="hotels.guest-houses", sub_c="hotels")
add(seg, "roman_ur", "hotal multan", "typo", H, "multan")
add(seg, "roman_ur", "hotel faisalabad station ke qareeb", "tail", H, "faisalabad", filt="near=railway_station", note="qareeb = near")
add(seg, "roman_ur", "bachon ke sath hotel murree", "tail", H, "murree", filt="family_friendly=true")
add(seg, "roman_ur", "kam kiraye wala hotel karachi", "tail", H, "karachi", ex_c="hotels.budget", sub_c="hotels", filt="price_band=budget", note="kam kiraya = low rent")
add(seg, "roman_ur", "islamabad ke hotel", "head", H, "islamabad")
add(seg, "roman_ur", "peshawar mein hotel", "head", H, "peshawar")

# ---------------- surgical instruments, Sialkot ----------------
seg = "surgical"
SI = S
add(seg, "en", "surgical instruments sialkot", "head", SI, "sialkot", sub_p="pk.punjab", note="core pilot query; list page and manufacturers", rtype="list")
add(seg, "en", "surgical instruments manufacturers sialkot", "head", SI, "sialkot", filt="role=manufacturer")
add(seg, "en", "surgical instruments exporter pakistan", "head", SI, "pakistan", filt="role=exporter", sub_p="pk")
add(seg, "en", "forceps manufacturer sialkot", "torso", f"{S}.forceps", "sialkot", ex_c=f"{S}.forceps", sub_c=SI, filt="role=manufacturer")
add(seg, "en", "surgical scissors sialkot", "torso", f"{S}.scissors", "sialkot", ex_c=f"{S}.scissors", sub_c=SI)
add(seg, "en", "needle holder manufacturer sialkot", "torso", f"{S}.needle-holders", "sialkot", ex_c=f"{S}.needle-holders", sub_c=SI)
add(seg, "en", "dental instruments sialkot", "torso", f"{S}.dental", "sialkot", ex_c=f"{S}.dental", sub_c=SI)
add(seg, "en", "orthopedic instruments sialkot", "torso", f"{S}.orthopaedic", "sialkot", ex_c=f"{S}.orthopaedic", sub_c=SI, note="US spelling; taxonomy uses orthopaedic")
add(seg, "en", "ISO 13485 surgical instruments sialkot", "tail", SI, "sialkot", filt="certification=iso13485", note="certification facet")
add(seg, "en", "CE marked surgical instruments sialkot", "tail", SI, "sialkot", filt="certification=ce")
add(seg, "en", "surgical instruments OEM private label sialkot", "tail", SI, "sialkot", filt="service=oem")
add(seg, "en", "scalpel handle supplier pakistan", "tail", f"{S}.scalpels", "pakistan", ex_c=f"{S}.scalpels", sub_c=SI, sub_p="pk")
add(seg, "en", "stainless steel surgical instruments pakistan", "torso", SI, "pakistan", filt="material=stainless_steel", sub_p="pk")
add(seg, "en", "surgical instruments sialkot minimum order 100 pieces", "tail", SI, "sialkot", filt="moq<=100")
add(seg, "en", "retractors manufacturer sialkot", "tail", f"{S}.retractors", "sialkot", ex_c=f"{S}.retractors", sub_c=SI)
add(seg, "en", "surgical kits sialkot", "tail", f"{S}.kits", "sialkot", ex_c=f"{S}.kits", sub_c=SI)
add(seg, "en", "surgical instrments sialkot", "typo", SI, "sialkot", note="missing u")
add(seg, "en", "sialkot surgcal instruments", "typo", SI, "sialkot", note="missing i")
add(seg, "en", "sialkot surgical", "head", SI, "sialkot", note="short form")
add(seg, "en", "surgical instruments lahore", "head", SI, "lahore", sub_c="", sub_p="pk.punjab", note="expected few results; substitute is Sialkot")
add(seg, "en", "forceps suppliers pakistan", "torso", f"{S}.forceps", "pakistan", ex_c=f"{S}.forceps", sub_c=SI, sub_p="pk")
# roman urdu surgical
add(seg, "roman_ur", "jarrahi auzar sialkot", "head", SI, "sialkot", note="jarrahi auzar = surgical instruments")
add(seg, "roman_ur", "surgical instruments banane wale sialkot", "torso", SI, "sialkot", filt="role=manufacturer", note="banane wale = makers")
add(seg, "roman_ur", "sialkot surgical factory", "torso", SI, "sialkot", filt="role=manufacturer")
add(seg, "roman_ur", "sialkot qainchi forceps wholesale", "tail", f"{S}.forceps", "sialkot", ex_c=f"{S}.forceps|{S}.scissors", sub_c=SI, note="qainchi = scissors")
add(seg, "roman_ur", "dental auzar sialkot", "torso", f"{S}.dental", "sialkot", ex_c=f"{S}.dental", sub_c=SI)
add(seg, "roman_ur", "operation ke auzar sialkot", "torso", SI, "sialkot", note="operation ke auzar = surgical tools")
add(seg, "roman_ur", "surgical items export sialkot", "tail", SI, "sialkot", filt="role=exporter")
add(seg, "roman_ur", "sialkot mein surgical instruments ki factory", "tail", SI, "sialkot", filt="role=manufacturer")
add(seg, "roman_ur", "surgical instrments sialkot", "typo", SI, "sialkot")
add(seg, "roman_ur", "jarahi auzar sialkot", "typo", SI, "sialkot", note="variant spelling of jarrahi")

# ---------------- plumbers ----------------
seg = "plumbers"
PL = P
for c in ["lahore", "karachi", "islamabad", "rawalpindi", "faisalabad"]:
    add(seg, "en", f"plumber in {c}", "head", PL, c, rtype="list")
add(seg, "en", "plumbers karachi", "head", PL, "karachi")
add(seg, "en", "emergency plumber islamabad", "torso", "plumbers.emergency", "islamabad", ex_c="plumbers.emergency", sub_c=PL)
add(seg, "en", "24 hour plumber lahore", "torso", "plumbers.emergency", "lahore", ex_c="plumbers.emergency", sub_c=PL, filt="hours=24")
add(seg, "en", "plumber near me", "near_me", PL, "lahore", note="place from edge guess or browser location; judged with place set to Lahore")
add(seg, "en", "bathroom fitting plumber rawalpindi", "tail", PL, "rawalpindi", filt="service=bathroom_fitting")
add(seg, "en", "geyser repair plumber karachi", "tail", PL, "karachi", filt="service=geyser", note="geyser = water heater")
add(seg, "en", "water tank cleaning lahore", "tail", PL, "lahore", ex_c="", sub_c=PL, comp_c="cleaning-services", note="adjacent service; no exact list type in the pilot, plumbers are substitutes")
add(seg, "en", "drain blockage plumber lahore", "tail", PL, "lahore", filt="service=drain")
add(seg, "en", "plumber dha lahore", "tail", PL, "pk.punjab.lahore.dha", sub_p="pk.punjab.lahore", note="area scope")
add(seg, "en", "plumber clifton karachi", "tail", PL, "pk.sindh.karachi.clifton", sub_p="pk.sindh.karachi")
add(seg, "en", "plumbing contractors islamabad", "torso", PL, "islamabad", filt="role=contractor")
add(seg, "en", "plumbr karachi", "typo", PL, "karachi")
add(seg, "en", "plumer lahore", "typo", PL, "lahore")
add(seg, "en", "plumber multan", "head", PL, "multan")
add(seg, "en", "sanitary works lahore", "torso", PL, "lahore", sub_c="", note="trade synonym of plumbing work")
# roman urdu plumbers
add(seg, "roman_ur", "plumber lahore", "head", PL, "lahore")
add(seg, "roman_ur", "nal saaz lahore", "torso", PL, "lahore", note="nal saaz = plumber (pipe maker); spelling varies (nal saz, nalsaz)")
add(seg, "roman_ur", "nalka mistri karachi", "torso", PL, "karachi", note="nalka = tap; mistri = tradesman")
add(seg, "roman_ur", "plumber mistri islamabad", "torso", PL, "islamabad")
add(seg, "roman_ur", "paani ki leakage plumber karachi", "tail", PL, "karachi", filt="service=leak", note="paani = water")
add(seg, "roman_ur", "ghar mein plumber chahiye lahore", "tail", PL, "lahore", note="need a plumber at home")
add(seg, "roman_ur", "sasta plumber islamabad", "torso", PL, "islamabad", filt="price_band=budget")
add(seg, "roman_ur", "tanki saaf karne wala lahore", "tail", PL, "lahore", ex_c="", sub_c=PL, comp_c="cleaning-services", note="tank cleaner")
add(seg, "roman_ur", "bathroom fitting ka mistri rawalpindi", "tail", PL, "rawalpindi", filt="service=bathroom_fitting")
add(seg, "roman_ur", "gas aur paani pipe fitting karachi", "tail", PL, "karachi", filt="service=pipe_fitting")
add(seg, "roman_ur", "plumbar lahore", "typo", PL, "lahore")
add(seg, "roman_ur", "nalsaz karachi", "typo", PL, "karachi", note="joined spelling")

# ---------------- schools ----------------
seg = "schools"
for c in ["lahore", "islamabad", "karachi", "rawalpindi", "faisalabad", "multan"]:
    add(seg, "en", f"schools in {c}", "head", SC, c, rtype="list")
add(seg, "en", "best schools in islamabad", "torso", SC, "islamabad", filt="quality=high", note="quality intent; needs rating or verification, not only text")
add(seg, "en", "private schools karachi", "torso", SC, "karachi", filt="sector=private")
add(seg, "en", "montessori school lahore", "torso", "schools.montessori", "lahore", ex_c="schools.montessori", sub_c=SC)
add(seg, "en", "o level schools lahore", "torso", "schools.o-level", "lahore", ex_c="schools.o-level", sub_c=SC, filt="curriculum=cambridge")
add(seg, "en", "girls school rawalpindi", "torso", "schools.girls", "rawalpindi", ex_c="schools.girls", sub_c=SC)
add(seg, "en", "boys schools in lahore dha", "tail", "schools.boys", "pk.punjab.lahore.dha", ex_c="schools.boys", sub_c=SC, sub_p="pk.punjab.lahore")
add(seg, "en", "english medium school sialkot", "torso", SC, "sialkot", filt="medium=english")
add(seg, "en", "cambridge school islamabad", "torso", SC, "islamabad", filt="curriculum=cambridge")
add(seg, "en", "school near me", "near_me", SC, "lahore", note="judged with place set to Lahore")
add(seg, "en", "cheap private school faisalabad", "tail", SC, "faisalabad", filt="fee_band=low")
add(seg, "en", "school admission 2027 lahore", "tail", SC, "lahore", filt="admission=open", note="needs admission status field; freshness matters")
add(seg, "en", "international school karachi", "torso", SC, "karachi", filt="curriculum=international")
add(seg, "en", "boarding school murree", "tail", SC, "murree", filt="boarding=true")
add(seg, "en", "primary school peshawar", "torso", "schools.primary", "peshawar", ex_c="schools.primary", sub_c=SC)
add(seg, "en", "scool lahore", "typo", SC, "lahore")
add(seg, "en", "montesori school karachi", "typo", "schools.montessori", "karachi", ex_c="schools.montessori", sub_c=SC)
add(seg, "en", "schols in islamabad", "typo", SC, "islamabad", rtype="list")
add(seg, "en", "the city school lahore", "navigational", SC, "lahore", must="city school", note="brand query")
add(seg, "en", "beaconhouse school lahore", "navigational", SC, "lahore", must="beaconhouse")
# roman urdu schools
add(seg, "roman_ur", "lahore ke achay school", "torso", SC, "lahore", filt="quality=high", note="achay = good")
add(seg, "roman_ur", "karachi mein private school", "torso", SC, "karachi", filt="sector=private")
add(seg, "roman_ur", "school mein admission islamabad", "tail", SC, "islamabad", filt="admission=open")
add(seg, "roman_ur", "ladkiyon ka school rawalpindi", "torso", "schools.girls", "rawalpindi", ex_c="schools.girls", sub_c=SC, note="ladkiyon = girls")
add(seg, "roman_ur", "sasta school faisalabad", "torso", SC, "faisalabad", filt="fee_band=low")
add(seg, "roman_ur", "montessori lahore", "head", "schools.montessori", "lahore", ex_c="schools.montessori", sub_c=SC)
add(seg, "roman_ur", "english medium school multan", "torso", SC, "multan", filt="medium=english")
add(seg, "roman_ur", "bachon ka school gulberg lahore", "tail", SC, "pk.punjab.lahore.gulberg", sub_p="pk.punjab.lahore", note="bachon = children")
add(seg, "roman_ur", "kam fees wala school lahore", "tail", SC, "lahore", filt="fee_band=low")
add(seg, "roman_ur", "o level ka school karachi", "tail", "schools.o-level", "karachi", ex_c="schools.o-level", sub_c=SC)
add(seg, "roman_ur", "hifz academy lahore", "tail", SC, "lahore", filt="type=hifz", note="Quran memorisation school; may need a new list type")
add(seg, "roman_ur", "skool lahore", "typo", SC, "lahore", note="phonetic spelling")
add(seg, "roman_ur", "madrasa islamabad", "torso", SC, "islamabad", filt="type=madrasa", note="religious school; own list type likely")
# a few Urdu-script rows; wording must be confirmed by a native speaker before judging
for q, seg_, c, pl, note in [("ہوٹل لاہور", "hotels", H, "lahore", "hotel Lahore"), ("سکول اسلام آباد", "schools", SC, "islamabad", "school Islamabad"),
                             ("پلمبر کراچی", "plumbers", PL, "karachi", "plumber Karachi"),
                             ("جراحی کے اوزار سیالکوٹ", "surgical", SI, "sialkot", "surgical instruments Sialkot"),
                             ("لاہور میں سستا ہوٹل", "hotels", H, "lahore", "cheap hotel in Lahore"),
                             ("کراچی کے اچھے سکول", "schools", SC, "karachi", "good schools of Karachi")]:
    add(seg_, "ur", q, "head", c, pl, note=f"Urdu script ({note}); native speaker to confirm the wording")

for i, r in enumerate(rows, 1):
    r["query_id"] = f"Q{i:03d}"
    r["status"] = "seed_unjudged"
cols = ["query_id", "segment", "language", "query", "query_type", "result_type", "intent_concept", "intent_place", "exact_concepts",
        "exact_places", "substitute_concepts", "substitute_places", "complement_concepts", "facet_filters", "must_terms", "status", "notes"]
with open("../benchmarks/judgement_seed.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
    for r in rows: w.writerow({c: r.get(c, "") for c in cols})
from collections import Counter
print(len(rows), Counter(r["segment"] for r in rows), Counter(r["language"] for r in rows), Counter(r["query_type"] for r in rows))
