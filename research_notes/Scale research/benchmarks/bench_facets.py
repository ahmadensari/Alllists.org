"""Facet count cost: live GROUP BY versus a precomputed JSON cell, at 1M and 5M entries.

Usage: python bench_facets.py --db bench_search --scale 1m|5m   (refuses databases not starting with bench_)
Creates facet_cell_<scale>(city_path, root_concept_id, total, facets jsonb) from published entries, times the build, then times
(a) live: select level, script, count(*) for the same scope (city + root list type, city only, country, whole table)
(b) cell: primary-key lookup of the stored JSON.
"""
import argparse, json, random, sys, time
import numpy as np, psycopg
ap = argparse.ArgumentParser()
ap.add_argument("--db", required=True); ap.add_argument("--scale", choices=["1m", "5m"], required=True)
ap.add_argument("--socket-dir", default="/var/lib/postgresql/bench_pg16"); ap.add_argument("--port", type=int, default=5544)
ap.add_argument("--n", type=int, default=100)
a = ap.parse_args()
if not a.db.startswith("bench_"): sys.exit("refusing: database name must start with bench_")
E, F = f"entry_{a.scale}", f"facet_cell_{a.scale}"
con = psycopg.connect(f"host={a.socket_dir} port={a.port} dbname={a.db} user=postgres", autocommit=True); cur = con.cursor()
cur.execute("set statement_timeout = 20000")
out = {"scale": a.scale}
t = time.time()
cur.execute(f"drop table if exists {F}")
cur.execute(f"""create table {F} as
  with base as (select split_part(e.place_path,'.',1)||'.'||split_part(e.place_path,'.',2)||'.'||split_part(e.place_path,'.',3) as city_path, cc.ancestor_id as root_id,
                       e.level::text as lv, e.script as sc
                from {E} e join concept_closure cc on cc.descendant_id = e.concept_id join concept c on c.id = cc.ancestor_id and c.parent_id is null
                where e.publish_state = 'published'),
       lvl as (select city_path, root_id, lv, count(*) n from base group by 1, 2, 3),
       scr as (select city_path, root_id, sc, count(*) n from base group by 1, 2, 3),
       tot as (select city_path, root_id, count(*) n from base group by 1, 2)
  select t.city_path, t.root_id, t.n::int as total,
         (select jsonb_object_agg(lv, n) from lvl l where l.city_path = t.city_path and l.root_id = t.root_id) as level,
         (select jsonb_object_agg(sc, n) from scr s where s.city_path = t.city_path and s.root_id = t.root_id) as script
  from tot t""")
cur.execute(f"alter table {F} add primary key (city_path, root_id)"); cur.execute(f"analyze {F}")
out["build_seconds"] = round(time.time() - t, 1)
cur.execute(f"select count(*), pg_total_relation_size('{F}') from {F}"); n, sz = cur.fetchone()
out["cells"] = n; out["table_bytes"] = sz; out["bytes_per_cell"] = round(sz / n)
cur.execute(f"select city_path, root_id, total from {F} where total >= 25 order by random() limit 300"); cells = cur.fetchall()
res = {}
def timeit(name, fn, n=a.n):
    lat = []
    for i in range(n + 3):
        t0 = time.perf_counter(); fn(i); ms = (time.perf_counter() - t0) * 1000
        if i >= 3: lat.append(ms)
    arr = np.array(lat); res[name] = dict(p50=round(float(np.percentile(arr, 50)), 2), p95=round(float(np.percentile(arr, 95)), 2), n=len(lat))
    print(name, res[name], flush=True)
cur.execute("select ancestor_id, array_agg(descendant_id) from concept_closure group by 1"); clo = dict(cur.fetchall())
def live_city_concept(i):
    p, r, _ = cells[i % len(cells)]
    cur.execute(f"select level, count(*) from {E} where publish_state='published' and country_code=%s and place_path like %s and concept_id = any(%s) group by 1", [p.split(".")[0], p + ".%", clo[r]])
    cur.fetchall()
def live_city(i):
    p, r, _ = cells[i % len(cells)]
    cur.execute(f"select level, count(*) from {E} where publish_state='published' and country_code=%s and place_path like %s group by 1", [p.split(".")[0], p + ".%"]); cur.fetchall()
def live_country(i):
    cur.execute(f"select level, count(*) from {E} where publish_state='published' and country_code='pk' group by 1"); cur.fetchall()
def live_all(i):
    cur.execute(f"select level, count(*) from {E} where publish_state='published' group by 1"); cur.fetchall()
def cell_lookup(i):
    p, r, _ = cells[i % len(cells)]; cur.execute(f"select total, level, script from {F} where city_path=%s and root_id=%s", [p, r]); cur.fetchall()
timeit("live_city_plus_list_type", live_city_concept); timeit("live_city_all_types", live_city)
timeit("live_country_all_types", live_country, 20); timeit("live_whole_table", live_all, 10); timeit("stored_cell_lookup", cell_lookup, 300)
cur.execute(f"select avg(total), percentile_cont(0.5) within group (order by total), max(total) from {F} where total >= 25"); out["cell_size_avg_median_max_(cells>=25)"] = [float(x) for x in cur.fetchone()]
out["timings_ms"] = res
json.dump(out, open(f"results/facets_{a.scale}.json", "w"), indent=1); print(json.dumps(out, indent=1))
