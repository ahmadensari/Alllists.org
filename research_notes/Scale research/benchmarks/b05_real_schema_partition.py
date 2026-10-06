"""B05: turn the REAL entries_entry table (as made by the project's migrations, loaded with 1M rows by b03a) into a country-list-partitioned
table with hand-written SQL, without Django knowing, then run the real Django ORM and real project functions against it.

Works on a copy: CREATE DATABASE bench_part_real TEMPLATE bench_django (nothing in bench_django changes).

Steps proved here (the migration plan in note 06, section 5):
  1  create partitioned twin + partitions + indexes (instant, empty)
  2  mirror trigger on the old table (insert / update / delete) so writes during the copy are not lost
  3  keyset-batched copy (5,000 rows) while a writer keeps inserting and updating
  4  verify (row counts and a per-country checksum equal)
  5  swap in one short transaction: lock, rename, move index names, drop the 40 foreign keys that pointed at entries_entry(id)
  6  re-create integrity: composite FK (country_code, entry_id) for the 14 children that carry country_code; list the others
  7  real Django: ORM create/filter/update/delete, recount_cell, `makemigrations --check`

Run: PYTHONDONTWRITEBYTECODE=1 DJANGO_ALLOW_TEST_KEY=1 .venv/bin/python b05_real_schema_partition.py
"""

import os
import random
import subprocess
import sys
import threading
import time

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from common import Timer, admin, connect, drop_db  # noqa: E402

import psycopg  # noqa: E402

SRC, DB = "bench_django", "bench_part_real"
COUNTRIES = ["PK", "IN", "BD", "LK", "NP", "AE", "SA", "TR", "EG", "NG"]
BACKEND = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "backend"))


def main():
    with admin() as a:
        a.execute(f'DROP DATABASE IF EXISTS "{DB}" WITH (FORCE)')
        with Timer() as t:
            a.execute(f'CREATE DATABASE "{DB}" TEMPLATE "{SRC}"')
    print(f"template copy of {SRC}: {t.s:.1f}s")
    c = connect(DB)
    n_old = c.execute("SELECT count(*) FROM entries_entry").fetchone()[0]
    fks = c.execute("SELECT conrelid::regclass::text, conname FROM pg_constraint WHERE confrelid = 'entries_entry'::regclass AND contype = 'f' AND conrelid <> 'entries_entry'::regclass").fetchall()
    selfk = c.execute("SELECT conname FROM pg_constraint WHERE conrelid = 'entries_entry'::regclass AND confrelid = 'entries_entry'::regclass").fetchall()
    kids = {r[0] for r in c.execute("SELECT table_name FROM information_schema.columns WHERE column_name = 'country_code' AND table_schema = 'public'").fetchall()}
    print(f"entries_entry rows={n_old:,}; foreign keys from other tables={len(fks)}; self foreign keys={len(selfk)}")

    # 1. twin
    t0 = time.perf_counter()
    try:
        c.execute("CREATE TABLE entries_entry_p (LIKE entries_entry INCLUDING DEFAULTS INCLUDING IDENTITY) PARTITION BY LIST (country_code)")
        print("step 1: LIKE .. INCLUDING IDENTITY on a partitioned table: OK")
        identity = True
    except psycopg.Error as e:
        print("step 1: LIKE .. INCLUDING IDENTITY failed:", str(e).splitlines()[0])
        c.execute("CREATE TABLE entries_entry_p (LIKE entries_entry INCLUDING DEFAULTS) PARTITION BY LIST (country_code)")
        identity = False
    for cc in COUNTRIES:
        c.execute(f"CREATE TABLE entries_entry_{cc.lower()} PARTITION OF entries_entry_p FOR VALUES IN ('{cc}')")
    c.execute("CREATE TABLE entries_entry_default PARTITION OF entries_entry_p DEFAULT")
    c.execute("ALTER TABLE entries_entry_p ADD PRIMARY KEY (country_code, id)")
    c.execute("CREATE UNIQUE INDEX p_uid_key ON entries_entry_p (country_code, uid)")
    idx = c.execute("SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'entries_entry' AND indexname NOT IN ('entries_entry_pkey', 'entries_entry_uid_key', 'entries_entry_uid_741a5617_like') ORDER BY 1").fetchall()
    newidx = []
    for name, d in idx:
        tmp = "p_" + name[-40:]
        c.execute(d.replace("public.entries_entry ", "public.entries_entry_p ").replace(f"INDEX {name} ", f"INDEX {tmp} "))
        newidx.append((tmp, name))
    # the old default for id: use the same sequence so ids keep increasing
    seq = c.execute("SELECT pg_get_serial_sequence('entries_entry', 'id')").fetchone()[0]
    print(f"step 1 done in {time.perf_counter() - t0:.2f}s: {len(COUNTRIES)} partitions + default, {len(newidx) + 2} indexes (identity={identity}, old sequence={seq})")

    # 2. mirror trigger
    cols = [r[0] for r in c.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'entries_entry' ORDER BY ordinal_position").fetchall()]
    collist = ", ".join(cols)
    sets = ", ".join(f"{k} = EXCLUDED.{k}" for k in cols if k not in ("id", "country_code"))
    c.execute(f"""
CREATE OR REPLACE FUNCTION entries_entry_mirror() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF TG_OP = 'DELETE' THEN
    DELETE FROM entries_entry_p WHERE country_code = OLD.country_code AND id = OLD.id;
    RETURN OLD;
  END IF;
  IF TG_OP = 'UPDATE' AND OLD.country_code <> NEW.country_code THEN
    DELETE FROM entries_entry_p WHERE country_code = OLD.country_code AND id = OLD.id;
  END IF;
  INSERT INTO entries_entry_p ({collist}) VALUES ({", ".join("NEW." + k for k in cols)})
    ON CONFLICT (country_code, id) DO UPDATE SET {sets};
  RETURN NEW;
END $$;
CREATE TRIGGER entries_entry_mirror_t AFTER INSERT OR UPDATE OR DELETE ON entries_entry FOR EACH ROW EXECUTE FUNCTION entries_entry_mirror();
""")

    # 3. copy in keyset batches with a concurrent writer
    stop = [False]
    wstat = {"n": 0, "max": 0.0}

    def writer():
        w = connect(DB)
        rng = random.Random(9)
        mx = w.execute("SELECT max(id) FROM entries_entry").fetchone()[0]
        i = 0
        while not stop[0]:
            t = time.perf_counter()
            k = rng.random()
            if k < 0.5:
                w.execute("UPDATE entries_entry SET updated_at = now(), name = name || '.' WHERE id = %s", (rng.randint(1, mx),))
            elif k < 0.8:
                w.execute("INSERT INTO entries_entry (uid, country_code, entity_type, name, name_lang, name_fold, description, status, publish_state, address, address_text, place_path, precision_class, coord_source, service_area, website, size_band, languages, price_band, payment_methods, addons, claim_state, listing_plan, visibility_flags, created_via, created_at, updated_at, tombstone_reason, place_id, primary_concept_id) "
                          "VALUES (%s, 'PK', 'business', 'live', 'en', 'live', '', 'open', 'draft', '{}', '', 'pk.p1.c1', '', '', '{}', '', '', '[]', '', '[]', '{}', 'unclaimed', 'basic', '[]', 'import', now(), now(), '', 111, 1101)", (f"L{i:025d}",))
                i += 1
            else:
                w.execute("UPDATE entries_entry SET publish_state = 'published' WHERE id = %s", (rng.randint(1, mx),))
            wstat["max"] = max(wstat["max"], time.perf_counter() - t)
            wstat["n"] += 1
            time.sleep(0.002)
        w.close()

    wt = threading.Thread(target=writer)
    wt.start()
    t0 = time.perf_counter()
    last, copied = 0, 0
    while True:
        hi = c.execute("SELECT max(id) FROM (SELECT id FROM entries_entry WHERE id > %s ORDER BY id LIMIT 5000) b", (last,)).fetchone()[0]
        if hi is None:
            break
        with c.transaction():
            c.execute(f"INSERT INTO entries_entry_p ({collist}) SELECT {collist} FROM entries_entry WHERE id > %s AND id <= %s ON CONFLICT (country_code, id) DO NOTHING", (last, hi))
        copied += 5000
        last = hi
    copy_s = time.perf_counter() - t0
    stop[0] = True
    wt.join()
    print(f"step 3: copied in {copy_s:.1f}s ({n_old / copy_s:,.0f} rows/s) while a writer did {wstat['n']:,} statements, slowest {wstat['max'] * 1000:.0f} ms (mirror trigger cost included)")
    c.execute("ANALYZE entries_entry_p")

    # 4. verify
    a = c.execute("SELECT count(*), md5(string_agg(id::text || uid || name || publish_state, ',' ORDER BY id)) FROM entries_entry").fetchone()
    b = c.execute("SELECT count(*), md5(string_agg(id::text || uid || name || publish_state, ',' ORDER BY id)) FROM entries_entry_p").fetchone()
    print(f"step 4: old rows={a[0]:,} checksum={a[1][:10]}  new rows={b[0]:,} checksum={b[1][:10]}  equal={a == b}")

    # 5. swap
    with Timer() as lock_t:
        with c.transaction():
            c.execute("SET LOCAL lock_timeout = '5s'")
            c.execute("LOCK TABLE entries_entry IN ACCESS EXCLUSIVE MODE")
            c.execute("DROP TRIGGER entries_entry_mirror_t ON entries_entry")
            for tbl, con in fks:
                c.execute(f'ALTER TABLE {tbl} DROP CONSTRAINT "{con}"')
            for con, in selfk:
                c.execute(f'ALTER TABLE entries_entry DROP CONSTRAINT "{con}"')
            mx = c.execute("SELECT max(id) FROM entries_entry").fetchone()[0]
            c.execute("ALTER TABLE entries_entry RENAME TO entries_entry_old")
            c.execute("ALTER TABLE entries_entry_p RENAME TO entries_entry")
            c.execute("ALTER INDEX entries_entry_pkey RENAME TO entries_entry_old_pkey")
            c.execute("ALTER INDEX entries_entry_p_pkey RENAME TO entries_entry_pkey")
            for tmp, old in newidx:
                c.execute(f'ALTER INDEX "{old}" RENAME TO "{old}_old"')
                c.execute(f'ALTER INDEX "{tmp}" RENAME TO "{old}"')
            c.execute("ALTER INDEX p_uid_key RENAME TO entries_entry_uid_key")
            if identity:
                c.execute(f"ALTER TABLE entries_entry ALTER COLUMN id RESTART WITH {mx + 1}")
            else:
                c.execute(f"ALTER TABLE entries_entry ALTER COLUMN id SET DEFAULT nextval('{seq}')")
    print(f"step 5: swap transaction held ACCESS EXCLUSIVE on entries_entry for {lock_t.s * 1000:.0f} ms (includes dropping {len(fks)} foreign keys)")

    # 6. integrity again
    with_cc, without_cc = [], []
    for tbl, con in fks:
        cols_t = [r[0] for r in c.execute("SELECT column_name FROM information_schema.columns WHERE table_name = %s", (tbl,)).fetchall()]
        (with_cc if "country_code" in cols_t else without_cc).append((tbl, con))
    done = []
    with Timer() as t:
        for tbl, con in with_cc:
            ecol = next(r[0] for r in c.execute("SELECT column_name FROM information_schema.columns WHERE table_name = %s AND column_name LIKE '%%entry_id'", (tbl,)).fetchall())
            c.execute(f'ALTER TABLE {tbl} ADD CONSTRAINT "{tbl}_entry_cc_fk" FOREIGN KEY (country_code, {ecol}) REFERENCES entries_entry (country_code, id) NOT VALID')
            c.execute(f'ALTER TABLE {tbl} VALIDATE CONSTRAINT "{tbl}_entry_cc_fk"')
            done.append(tbl)
    print(f"step 6: composite FKs re-added and validated on {len(done)} tables that already carry country_code ({t.s:.1f}s on small tables)")
    print(f"        {len(without_cc)} referencing tables have no country_code column ({sorted({x[0] for x in without_cc})[:6]} ...): add the column or db_constraint=False + orphan check")

    # 7. real Django
    code = r"""
import os, sys, time
sys.path.insert(0, %r); os.chdir(%r)
os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"
import django; django.setup()
from django.db import connection
from entries.models import Entry, Contact
from places.models import Place
from taxonomy.models import Concept
from analytics.rollups import recount_cell
from core import clock
place = Place.objects.get(path="pk.p1.c1"); concept = Concept.objects.get(pk=1101)
e = Entry.objects.create(country_code="PK", name="Partition Test", name_fold="partition test", place=place, place_path=place.path, primary_concept=concept)
print("ORM create ->", e.pk, e.uid)
print("ORM filter count PK city:", Entry.objects.filter(country_code="PK", place_path="pk.p1.c1").count())
Entry.objects.filter(pk=e.pk).update(publish_state="published")
print("ORM update ok; get by pk:", Entry.objects.get(pk=e.pk).publish_state)
Contact.objects.create(entry=e, country_code="PK", kind="phone", value_enc="x", value_hash="h" * 8)
print("Contact create with composite FK in place ok")
print("explain list query:")
with connection.cursor() as cur:
    cur.execute("EXPLAIN SELECT id FROM entries_entry WHERE country_code='PK' AND place_path='pk.p1.c1' AND primary_concept_id=1101 AND publish_state='published' ORDER BY name_fold LIMIT 25")
    print("\n".join("   " + r[0] for r in cur.fetchall()[:8]))
t = time.perf_counter(); cell = recount_cell("PK", "pk.p1.c1", 1101); print("real recount_cell on partitioned table: total", cell.total, "in %%.2fs" %% (time.perf_counter() - t))
e.delete()
print("ORM delete (Python cascade over children) ok; rows left with that uid:", Entry.objects.filter(uid=e.uid).count())
""" % (BACKEND, BACKEND)
    env = dict(os.environ, POSTGRES_DB=DB, DJANGO_ALLOW_TEST_KEY="1", PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True)
    print(r.stdout + r.stderr[-1500:])
    r = subprocess.run([sys.executable, "manage.py", "makemigrations", "--check", "--dry-run"], env=env, cwd=BACKEND, capture_output=True, text=True)
    print("makemigrations --check:", (r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout + r.stderr).strip() else "")
    c.close()
    drop_db(DB)


if __name__ == "__main__":
    main()
