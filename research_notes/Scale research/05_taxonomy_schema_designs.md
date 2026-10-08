# Taxonomy schema designs: multi-parent concepts, slug history, crosswalk, facets, memberships, store rule and migration plan

Date: 2026-10-08. Scope: English only. Status: design, built from saved measurements. No new benchmark or database server was started to write this note. Nothing under `backend/` was changed.

Grades: R reported or read from a file, S secondary, I inference (inputs stated), H hypothesis. "MEAS" means a number printed in a saved result file; the file is named in section 10. "UNVERIFIED" means the number was not opened at the source or no result file exists.

## 0. Bottom line

| ID | Decision | Basis |
|---|---|---|
| T1 | **Multi-parent graph: edge table as the truth plus a closure table for reads.** Recursive CTE stays as the nightly checker and the fallback. `ltree` is rejected. | Section 2: closure page median 3.7 ms, p95 395 ms; ltree resolver 289.6 ms; ltree copied onto rows 1,397 ms and 36 to 44% slower inserts (MEAS) |
| T2 | `Concept.parent` stays as the denormalised primary parent. New `ConceptEdge` (one primary edge per child, up to 3 secondary edges) and `ConceptClosure`. | MD-02, MD-03, M1 to M3 |
| T3 | `ConceptSlug` table with every slug ever used; resolver reads only that table; 200, 301 or 410. Entries store concept ids, never slugs. | C09, D-05, MD-07 |
| T4 | `ClassificationScheme` (edition, licence class, publish flag) and a `ConceptCrosswalk` with SKOS relation (exact, close, broad, narrow, related), state, confidence, evidence, and a `CrosswalkReview` row for "no code exists". | C06, MD-08 |
| T5 | Facet registry: `FacetDef`, `FacetApplicability` (subtree through the closure), `FacetValue`, `FacetRule`, and a narrow `EntryFacet` table. | C07, D-03, MD-06 |
| T6 | `EntryConcept` replaces `Entry.secondary_concepts`: role, state, source, evidence, confidence, `broad`, and copied `country_code`, `place_path`, `listable`, `best_level`, `sort_key`. | D-04, A1 to A8, MD-04, MD-20 |
| T7 | Store rule: store a (place, node) cell at 25 published members, or 10 verified, or pinned. Everything else is answered live with a `LIMIT 26` probe. Empty pairs resolve virtually (200, `noindex,follow`, nearest populated links). | D-06, R3, R4, MD-10, MD-11 |
| T8 | Zero-downtime migration in expand, backfill, dual-write, switch, contract steps (section 8). Backfill in 5,000-row batches; build secondary indexes after the load, concurrently. | b06: 5,000-row batches max stall 128 ms against 11,074 ms for one UPDATE (MEAS); taxonomy_08: 15.6 s against 60.9 s for 5.96M rows (MEAS) |

What is NOT measured (section 11): the roll-up build and incremental benchmarks for the taxonomy data set (`taxonomy_05`, `taxonomy_06`), the resolve and facet-filter timing (`taxonomy_09`), the DDL lock timing (`taxonomy_12`, `b07`), the per-row size of the designed table (`taxonomy_13`), and the proof run of the design (`taxonomy_prove_design.py`). Their scripts exist; their result files do not. No number from them appears here.

## 1. What the saved results cover

Scratch data set (scripts `taxonomy_01_generate_concepts.sql`, `taxonomy_02_generate_entries.sql`): 50,000 concepts in 6 levels (1 root, 30 sectors, 560 industries, 3,400 families, 8,400 products, 37,609 variants), 2,000,000 entries, 5,959,839 membership rows (about 2.98 a row per entry), 85% published, 220 countries, skewed. The membership table in the benchmark is the narrow `ec` table (entry, concept, role, place_path, published, sort_key), not the designed `EntryConcept`.

Graph shapes (`taxonomy_01_generate_concepts.sql`, tree stats in `taxonomy_tree_stats_*.txt`):

| Shape | Parents a node | Closure rows | Closure a node | Closure size | ltree paths | ltree size |
|---|---|---|---|---|---|---|
| seedlike (the real seed: 21 secondary links in 1,170 nodes) | 1.02 | 290,117 | 5.80 | 28 MB | 53,579 | 17 MB |
| moderate | 1.10 | 321,905 | 6.44 | 31 MB | 70,154 | 23 MB |
| stress (the page benchmark used this one, see caveat K2) | 2.00 | 1,004,185 | 20.08 | 100 MB | 591,833 | 171 MB |

(Sizes are the `pg_total_relation_size` rows of the stats files, including indexes.)

## 2. Closure table against ltree against recursive CTE

Question: "published entries under node X at place Y, page of 25, sorted", plus the count. 250 (node, place) pairs, 5 node levels by 5 place levels, 3 repetitions, warm = repetitions 2 and 3, 30 s timeout. All 7,500 timed rows are status `ok` (no timeouts) (MEAS, `taxonomy_query_raw.csv`).

Page query, median / p95 ms (MEAS, `taxonomy_query_tables.md`):

| Variant | All 250 | Cell under 100 members | 100k+ members | Node level L1 (sector) | Node level L5 (variant) |
|---|---|---|---|---|---|
| closure (join `concept_closure`, then membership list index) | **3.7 / 395** | 2.0 / 208 | 1,468.5 / 2,015 | 241.2 / 1,653 | 1.0 / 2 |
| rcte (recursive CTE over `concept_edge`) | 5.1 / 526 | 2.4 / 258 | **856.0 / 2,010** | 306.8 / 1,214 | 1.2 / 4 |
| closure + place-major index | 8.8 / 333 | 7.0 / 35 | 1,322.1 / 1,981 | **127.1 / 1,859** | 0.8 / 13 |
| closure + place as ltree with GiST | 8.0 / 562 | 2.0 / 286 | 1,402.7 / 1,960 | 309.2 / 1,812 | 1.1 / 50 |
| ltree resolver (GiST on `concept_path` finds the node set) | 289.6 / 808 | 281.7 / 499 | 1,546.3 / 2,205 | 299.0 / 1,789 | 286.4 / 585 |
| ltree copied onto each membership row (`cpaths ltree[]` + GiST) | 1,397.4 / 4,939 | 1,267.7 / 4,955 | 3,191.2 / 4,641 | 956.7 / 4,407 | 2,210.6 / 6,479 |

Count query, all 250 pairs, median / p95 ms (MEAS): closure 2.7 / 326; rcte 2.9 / 428; closure + place-major index 8.2 / 315; ltree resolver 200.5 / 626.

Single-page plans for four representative cells, `EXPLAIN (ANALYZE)` execution time (MEAS, `taxonomy_plans.txt`): small cell (1 member) closure 0.787 ms, rcte 0.163 ms; medium (20 members) closure 2.257 ms, rcte 1.981 ms; large (3,152 members) closure 174.0 ms, rcte 266.2 ms; huge (760,681 members, sector in the world) closure 1,976.8 ms, rcte 1,134.3 ms.

Graph edits, rolled-back transactions on the stress graph, median ms (MEAS, `taxonomy_07_graph_edits.log`):

| Child level | Descendants (median) | Members below | Closure add | Closure remove | ltree add | ltree remove | ltree copy on membership rows |
|---|---|---|---|---|---|---|---|
| L2 | 503.5 | 47,073 | 16.1 (1,007 rows) | 366.4 | 16.0 | 1.9 | 7,064.1 (47,073 rows) |
| L3 | 42.5 | 3,839 | 2.2 (177.5 rows) | 195.6 | 2.4 | 0.7 | 2,954.4 |
| L4 | 9.5 | 794.5 | 0.9 (61.5 rows) | 154.5 | 1.9 | 0.7 | 1,823.1 |
| L5 | 1.0 | 78.5 | 0.5 (12.5 rows) | 138.9 | 1.3 | 0.7 | 1,738.9 |

Membership inserts, one transaction per new entry (1 entry row + 3 membership rows), pgbench (MEAS, `taxonomy_08_inserts.log`):

| Design | 1 client entries/s | 4 clients entries/s | Latency 1 client |
|---|---|---|---|
| A: membership table, 3 indexes | 1,501.6 | 2,640.1 | 0.666 ms |
| A+: same plus place-major index | 1,262.1 (-16%) | 2,266.1 (-14%) | 0.792 ms |
| B: ltree[] on the row + GiST | 847.3 (-44%) | 1,702.7 (-36%) | 1.180 ms |

The place-major index is 357,662,720 bytes (342 MB) on 5.96M rows and took 5.6 s to build (MEAS).

Rebuild: the whole closure of the stress graph (1,004,185 rows) rebuilt by recursion in 6.6 s, then compared with the live table: 0 missing, 0 extra (MEAS, `taxonomy_11b_rebuild_closure_dag.txt`). The 50,000-node first backfill (282,995 closure rows) took 1.5 s (MEAS, `taxonomy_11_backfill_graph.txt`).

What a simpler model would lose (MEAS, `taxonomy_10_recall.txt`): of the 250 pairs, a primary-edge-only tree sees 12.7% of the entries a full-graph page holds, and the current repository rule (primary edges and primary membership only) sees 6.2%. The current rule misses entries on 194 of 250 pages; on average a page shows 34.0% of its entries. Synthetic data, so the percentages are not forecasts, but the direction is firm: secondary parents and secondary products must count.

Reading and choice `I`:

1. Closure and recursive CTE tie on pages within noise at this size (3.7 against 5.1 ms median, p95 395 against 526). The CTE is faster on the largest cells and on the smallest. Closure is faster on mid-size cells in the plan runs.
2. `ltree` loses on reads (290 ms for the resolver, 1.4 s for the copy) and the copy on the membership row also costs 36 to 44% of insert rate and 1.7 to 7.1 s to rewrite one edge change. The ltree path set also grows faster than closure on a multi-parent graph (171 MB against 100 MB at stress).
3. Closure costs 16 ms to add a secondary edge at the top (L2) and 139 to 366 ms to remove one. Taxonomy edits are staff work and rare, so this is acceptable. A full rebuild is 6.6 s for 1.0M rows, so a repair is cheap.
4. Why closure over CTE: the roll-up build and the set-based `GROUP BY` join the closure once per membership; a flat table gives the planner real row counts; the CTE cost depends on the graph shape (more parents, more branching) and was not measured on the seed-like graph (caveat K2). The CTE is kept in `check_consistency()` as the independent oracle.
5. The huge cells (a sector at the world level, 760k members) take 1.1 to 2.0 s live in every variant. That is the reason the store rule exists: such cells are stored and served from the roll-up plus a cached top-N page (note 01, R7), never computed per request.
6. The place-major index helps sector-level pages (127 ms against 241 ms median) and hurts small pages (7.0 against 2.0 ms) and inserts (-14 to -16%). Ship the `ec_list` index first; add `ec_place_list` only when the measured trigger fires (section 8, step 9).

## 3. Exact models: concepts, graph, closure

`Concept` changes (additive; `parent` stays):

```python
class Concept(UidModel):
    class Kind(models.TextChoices):
        FAMILY = "family"
        LIST_TYPE = "list_type"
        SPECIALITY = "speciality"
        SERVICE = "service"
        PRODUCT = "product"

    class Status(models.TextChoices):
        ACTIVE = "active"
        RESIDUAL = "residual"  # imported catch-all (HS "other"): hidden, must be split or merged before launch (rule T5)
        MERGED = "merged"
        RETIRED = "retired"  # never deleted (rule I3)

    class Scale(models.TextChoices):
        HYPER_LOCAL = "hyper_local"
        CITY = "city"
        NATIONAL = "national"
        GLOBAL = "global"

    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.PROTECT, related_name="children")
    kind = models.CharField(max_length=12, choices=Kind.choices)
    slug = models.SlugField(max_length=120)
    entity_type_default = models.CharField(max_length=12, default="business")
    natural_scale = models.CharField(max_length=12, choices=Scale.choices, default=Scale.CITY)
    template = models.ForeignKey(
        "AddonTemplate", null=True, blank=True, on_delete=models.SET_NULL, related_name="concepts"
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    # NEW (C09, D-05). `parent` stays as the denormalised PRIMARY parent (breadcrumb, canonical address); the
    # `ConceptEdge` row with is_primary=True is the source of truth and a nightly check compares the two.
    level = models.PositiveSmallIntegerField(null=True, blank=True)  # role level: 0 root family, 1 sector ... 5 variant, 6 and 7 assembly steps; null = not set yet
    merged_into = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.PROTECT, related_name="merged_from"
    )  # set when status = merged; slugs of this node keep resolving through it
    retired_at = models.DateTimeField(null=True, blank=True)
    created_by_id = models.BigIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=clock.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["kind", "slug"], name="uniq_concept_slug_per_kind"),
            models.CheckConstraint(condition=Q(level__lte=7), name="concept_level_max_7"),
            models.CheckConstraint(
                condition=Q(merged_into__isnull=True) | Q(status="merged"), name="concept_merged_into_needs_status"
            ),
            models.CheckConstraint(condition=~Q(merged_into=F("id")), name="concept_not_merged_into_self"),
        ]

    def __str__(self):
        return self.slug

    def label(self, language="en"):
        labels = list(self.labels.all())
        for lb in labels:
            if lb.language == language and lb.kind == ConceptLabel.Kind.PREFERRED:
                return lb.text
        for lb in labels:
            if lb.language == language:  # a synonym or local name in the page language beats an English preferred name
                return lb.text
        for lb in labels:
            if lb.kind == ConceptLabel.Kind.PREFERRED:
                return lb.text
        return self.slug
```

Graph tables:

```python
class ConceptEdge(models.Model):
    """Multi-parent tree (D-04, M1 to M3). One primary edge per child; up to 3 secondary edges (service and trigger
    enforce the cap). Parent and child sit one level apart. This table is the source of truth for the graph."""

    class Reason(models.TextChoices):
        PRIMARY = "primary"
        USE = "use"
        MATERIAL = "material"
        REGULATORY = "regulatory"
        TRADE = "trade"

    parent = models.ForeignKey("Concept", on_delete=models.PROTECT, related_name="child_edges")
    child = models.ForeignKey("Concept", on_delete=models.PROTECT, related_name="parent_edges")
    is_primary = models.BooleanField(default=False)
    reason = models.CharField(max_length=10, choices=Reason.choices, default=Reason.PRIMARY)
    created_at = models.DateTimeField(default=clock.now)
    created_by_id = models.BigIntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["parent", "child"], name="uniq_concept_edge"),
            models.UniqueConstraint(
                fields=["child"], condition=Q(is_primary=True), name="uniq_primary_edge_per_child"
            ),
            models.CheckConstraint(condition=~Q(parent=F("child")), name="concept_edge_not_self"),
            models.CheckConstraint(
                condition=(Q(is_primary=True, reason="primary") | Q(is_primary=False) & ~Q(reason="primary")),
                name="concept_edge_primary_reason",
            ),
        ]

class ConceptClosure(models.Model):
    """All ancestor and descendant pairs, self rows included (depth 0). Written only by taxonomy.closure."""

    pk = models.CompositePrimaryKey("ancestor", "descendant")
    ancestor = models.ForeignKey("Concept", on_delete=models.CASCADE, related_name="+", db_index=False)
    descendant = models.ForeignKey("Concept", on_delete=models.CASCADE, related_name="+", db_index=False)
    depth = models.PositiveSmallIntegerField()

    class Meta:
        indexes = [models.Index(fields=["descendant", "ancestor"], name="closure_desc_anc")]
```

Closure maintenance (the only code allowed to write edges, closure and `Concept.parent`). Taxonomy edits are staff-only and rare, so one advisory lock for all of them is acceptable; it is not acceptable on any entry write path (D-10):

```python
@transaction.atomic
def add_edge(parent, child, *, primary=False, reason=ConceptEdge.Reason.USE, by_id=None):
    _lock()
    if parent.pk == child.pk:
        raise GraphError("a node cannot be its own parent")
    if parent.level is not None and child.level is not None and parent.level + 1 != child.level:
        raise GraphError("parent must sit exactly one level above the child (rule M2)")
    ensure_self_row(parent)
    ensure_self_row(child)
    if ConceptClosure.objects.filter(ancestor=child, descendant=parent).exists():
        raise GraphError("this edge would make a cycle (rule M3)")
    if primary:
        if ConceptEdge.objects.filter(child=child, is_primary=True).exists():
            raise GraphError("the child already has a primary parent; use set_primary_parent")
        reason = ConceptEdge.Reason.PRIMARY
    elif ConceptEdge.objects.filter(child=child, is_primary=False).count() >= MAX_SECONDARY_PARENTS:
        raise GraphError("at most 3 secondary parents (rule M2)")
    ConceptEdge.objects.create(parent=parent, child=child, is_primary=primary, reason=reason, created_by_id=by_id)
    t = _closure_table()
    with connection.cursor() as cur:
        cur.execute(
            f"""INSERT INTO {t} (ancestor_id, descendant_id, depth)
                SELECT a.ancestor_id, d.descendant_id, a.depth + d.depth + 1
                FROM {t} a JOIN {t} d ON d.ancestor_id = %s
                WHERE a.descendant_id = %s
                ON CONFLICT (ancestor_id, descendant_id) DO UPDATE SET depth = LEAST(EXCLUDED.depth, {t}.depth)""",
            [child.pk, parent.pk],
        )
    if primary:
        Concept.objects.filter(pk=child.pk).update(parent=parent)
    log_change("edge_add", child, by_id, parent=parent.uid, primary=primary, reason=str(reason))

@transaction.atomic
def remove_edge(parent, child):
    """Remove a secondary edge, then rebuild the closure rows of the child's subtree that came from outside it."""
    _lock()
    edge = ConceptEdge.objects.get(parent=parent, child=child)
    if edge.is_primary:
        raise GraphError("remove the primary edge by moving the node (set_primary_parent), never by deleting it")
    edge.delete()
    rebuild_subtree(child)
    log_change("edge_remove", child, parent=parent.uid)

@transaction.atomic
def set_primary_parent(child, new_parent, *, by_id=None):
    _lock()
    old = ConceptEdge.objects.filter(child=child, is_primary=True).first()
    if old and old.parent_id == new_parent.pk:
        return
    if ConceptClosure.objects.filter(ancestor=child, descendant=new_parent).exists():
        raise GraphError("this move would make a cycle")
    if old:
        old.delete()
    existing = ConceptEdge.objects.filter(parent=new_parent, child=child).first()
    if existing:  # a secondary edge to the same parent becomes the primary one
        existing.delete()
    ConceptEdge.objects.create(parent=new_parent, child=child, is_primary=True, reason="primary", created_by_id=by_id)
    Concept.objects.filter(pk=child.pk).update(parent=new_parent)
    rebuild_subtree(child)
    log_change("reparent", child, by_id, old=old.parent.uid if old else None, new=new_parent.uid)

def rebuild_subtree(node):
    """Recompute every (ancestor, descendant) row whose descendant is in the subtree of `node` and whose ancestor is
    outside it. Rows inside the subtree never depend on an edge above `node`, so they are kept. Needs level to be set."""
    t = _closure_table()
    ensure_self_row(node)
    with connection.cursor() as cur:
        cur.execute(f"CREATE TEMP TABLE _sub ON COMMIT DROP AS SELECT descendant_id AS id FROM {t} WHERE ancestor_id = %s", [node.pk])
        cur.execute(f"DELETE FROM {t} WHERE descendant_id IN (SELECT id FROM _sub) AND ancestor_id NOT IN (SELECT id FROM _sub)")
        levels = [r[0] for r in _levels(cur)]
        for lvl in levels:
            cur.execute(
                f"""INSERT INTO {t} (ancestor_id, descendant_id, depth)
                    SELECT cl.ancestor_id, e.child_id, cl.depth + 1
                    FROM {ConceptEdge._meta.db_table} e
                    JOIN taxonomy_concept c ON c.id = e.child_id AND c.level = %s AND c.id IN (SELECT id FROM _sub)
                    JOIN {t} cl ON cl.descendant_id = e.parent_id
                    ON CONFLICT (ancestor_id, descendant_id) DO UPDATE SET depth = LEAST(EXCLUDED.depth, {t}.depth)""",
                [lvl],
            )
        cur.execute("DROP TABLE IF EXISTS _sub")

def check_consistency():
    """Nightly check. Returns a dict of counts that must all be zero."""
    t = _closure_table()
    with connection.cursor() as cur:
        cur.execute(
            f"""SELECT count(*) FROM taxonomy_concept c LEFT JOIN {ConceptEdge._meta.db_table} e ON e.child_id = c.id AND e.is_primary
                WHERE c.parent_id IS DISTINCT FROM e.parent_id AND (c.parent_id IS NOT NULL OR e.parent_id IS NOT NULL)"""
        )
        parent_mismatch = cur.fetchone()[0]
        cur.execute(
            f"""WITH RECURSIVE r(a, d, depth) AS (
                  SELECT id, id, 0 FROM taxonomy_concept
                  UNION
                  SELECT r.a, e.child_id, r.depth + 1 FROM r JOIN {ConceptEdge._meta.db_table} e ON e.parent_id = r.d)
                SELECT (SELECT count(*) FROM (SELECT a, d FROM r EXCEPT SELECT ancestor_id, descendant_id FROM {t}) x),
                       (SELECT count(*) FROM (SELECT ancestor_id, descendant_id FROM {t} EXCEPT SELECT a, d FROM r) y)"""
        )
        missing, extra = cur.fetchone()
    return {"parent_mismatch": parent_mismatch, "closure_missing": missing, "closure_extra": extra}
```

Database backstop (migration `taxonomy/0006_graph_guards.py`): a `BEFORE INSERT` trigger on `taxonomy_conceptedge` that raises on a level mismatch, a fourth secondary parent, or a cycle:

```python
"""Database backstops for the concept graph (PostgreSQL only). The services in taxonomy.closure check the same rules first."""

from django.db import migrations

SQL = """
CREATE OR REPLACE FUNCTION taxonomy_conceptedge_guard() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE pl int; cl int;
BEGIN
  SELECT level INTO pl FROM taxonomy_concept WHERE id = NEW.parent_id;
  SELECT level INTO cl FROM taxonomy_concept WHERE id = NEW.child_id;
  IF pl IS NOT NULL AND cl IS NOT NULL AND pl + 1 <> cl THEN
    RAISE EXCEPTION 'concept_edge_level: parent must be one level above the child';
  END IF;
  IF NOT NEW.is_primary AND (SELECT count(*) FROM taxonomy_conceptedge WHERE child_id = NEW.child_id AND NOT is_primary) >= 3 THEN
    RAISE EXCEPTION 'concept_edge_secondary_cap: at most 3 secondary parents';
  END IF;
  IF EXISTS (SELECT 1 FROM taxonomy_conceptclosure WHERE ancestor_id = NEW.child_id AND descendant_id = NEW.parent_id) THEN
    RAISE EXCEPTION 'concept_edge_cycle';
  END IF;
  RETURN NEW;
END $$;
DROP TRIGGER IF EXISTS taxonomy_conceptedge_guard ON taxonomy_conceptedge;
CREATE TRIGGER taxonomy_conceptedge_guard BEFORE INSERT ON taxonomy_conceptedge
  FOR EACH ROW EXECUTE FUNCTION taxonomy_conceptedge_guard();
"""
REVERSE = "DROP TRIGGER IF EXISTS taxonomy_conceptedge_guard ON taxonomy_conceptedge; DROP FUNCTION IF EXISTS taxonomy_conceptedge_guard();"


def forwards(apps, schema_editor):
    if schema_editor.connection.vendor == "postgresql":
        schema_editor.execute(SQL)


def backwards(apps, schema_editor):
    if schema_editor.connection.vendor == "postgresql":
        schema_editor.execute(REVERSE)


class Migration(migrations.Migration):
    dependencies = [("taxonomy", "0005_backfill_graph")]
    operations = [migrations.RunPython(forwards, backwards)]
```

`Concept.level` is a nullable small integer with `CHECK (level <= 7)`. A node may only be a child of a node exactly one level above (M2). Residual nodes (imported HS "other") get `status = residual`, are hidden and must be split or merged before launch.

## 4. Concept slug history and redirects

```python
class ConceptSlug(models.Model):
    """Every list-type slug ever used (C09, S4). The address resolver reads only this table. A current row answers 200;
    a retired row answers 301 to the current slug of the concept it points at (following merged_into). A slug is never
    given to a different concept, so old links never change meaning. Replaces ReservedSlug rows of kind list_type."""

    class Reason(models.TextChoices):
        CREATED = "created"
        RENAME = "rename"
        MERGE = "merge"
        PROMOTED = "promoted"  # a variant became a list type (rule T3)

    slug = models.SlugField(max_length=120)
    concept = models.ForeignKey("Concept", on_delete=models.PROTECT, related_name="slugs")
    is_current = models.BooleanField(default=True)
    reason = models.CharField(max_length=10, choices=Reason.choices, default=Reason.CREATED)
    created_at = models.DateTimeField(default=clock.now)
    retired_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["slug"], name="uniq_concept_slug_ever"),
            models.UniqueConstraint(
                fields=["concept"], condition=Q(is_current=True), name="uniq_current_slug_per_concept"
            ),
            models.CheckConstraint(
                condition=(Q(is_current=True, retired_at__isnull=True) | Q(is_current=False, retired_at__isnull=False)),
                name="concept_slug_current_xor_retired",
            ),
        ]

class TaxonomyChange(models.Model):
    """Append-only log of structural changes (C09): what was renamed, merged, split, moved or retired. `release` is empty
    until the monthly release closes it; the release number comes from core.RegistryVersion (key "taxonomy")."""

    class Kind(models.TextChoices):
        CREATE = "create"
        RENAME = "rename"
        MERGE = "merge"
        SPLIT = "split"
        RETIRE = "retire"
        REPARENT = "reparent"
        EDGE_ADD = "edge_add"
        EDGE_REMOVE = "edge_remove"
        PROMOTE = "promote"  # a variant became a list type (rule T3)

    concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.SET_NULL, related_name="changes")
    kind = models.CharField(max_length=12, choices=Kind.choices)
    payload = models.JSONField(default=dict, blank=True)  # {"old_slug": ..., "new_slug": ..., "into": uid, "parent": uid}
    release = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    at = models.DateTimeField(default=clock.now)
    by_id = models.BigIntegerField(null=True, blank=True)
```

Rules:

| ID | Rule |
|---|---|
| S1 | The resolver reads `ConceptSlug` only. `Concept.slug` is the current slug, kept in step by `register_slug`. |
| S2 | A slug is never given to a different concept (unique across all time). Going back to an old name of the same node reuses the row. |
| S3 | Current row: 200. Retired row: 301 to the current slug of the node after following `merged_into` (flattened to one hop). Retired node: 410. Unknown slug: 404, not a virtual page. |
| S4 | A slug that collides with a place or a system address is refused (shared URL namespace, `ReservedSlug`). |
| S5 | Every rename, merge, split, move, retire or promote writes a `TaxonomyChange` row; the monthly release stamps the release number. |

```python
@transaction.atomic
def register_slug(concept, slug, reason=ConceptSlug.Reason.CREATED):
    _check_free(slug, concept)
    now = timezone.now()
    ConceptSlug.objects.filter(concept=concept, is_current=True).exclude(slug=slug).update(is_current=False, retired_at=now)
    row, created = ConceptSlug.objects.get_or_create(slug=slug, defaults={"concept": concept, "reason": reason})
    if not created and not row.is_current:  # going back to an old name of the same node
        row.is_current, row.retired_at = True, None
        row.save(update_fields=["is_current", "retired_at"])
    ReservedSlug.objects.get_or_create(slug=slug, kind="list_type")
    Concept.objects.filter(pk=concept.pk).update(slug=slug)
    return row

def rename(concept, new_slug, by_id=None):
    old = concept.slug
    row = register_slug(concept, new_slug, ConceptSlug.Reason.RENAME)
    log_change("rename", concept, by_id, old_slug=old, new_slug=new_slug)
    return row

@transaction.atomic
def merge(loser, winner):
    if loser.pk == winner.pk:
        raise TaxonomyError("cannot merge a node into itself")
    final = winner
    for _ in range(MAX_MERGE_HOPS):
        if final.merged_into_id is None:
            break
        final = final.merged_into
    if final.pk == loser.pk:
        raise TaxonomyError("merge would create a loop")
    Concept.objects.filter(pk=loser.pk).update(status=Concept.Status.MERGED, merged_into=final)
    # flatten chains that already pointed at the loser, so resolution stays one hop
    Concept.objects.filter(merged_into=loser).update(merged_into=final)
    log_change("merge", loser, into=final.uid)

def resolve_slug(slug):
    row = ConceptSlug.objects.select_related("concept").filter(slug=slug).first()
    if row is None:
        return SlugResolution(404)
    concept = row.concept
    hops = 0
    while concept.merged_into_id and hops < MAX_MERGE_HOPS:
        concept, hops = concept.merged_into, hops + 1
    if concept.status == Concept.Status.RETIRED:
        return SlugResolution(410, concept)
    current = ConceptSlug.objects.filter(concept=concept, is_current=True).values_list("slug", flat=True).first()
    if current == slug and concept.pk == row.concept_id:
        return SlugResolution(200, concept)
    return SlugResolution(301, concept, current)
```

Entries hold `concept_id`, so a rename touches one `Concept` row and two `ConceptSlug` rows and no entry (acceptance test `test_entries_untouched_by_rename`).

## 5. Concept crosswalk with SKOS relation types

```python
class ClassificationScheme(models.Model):
    """One edition of an outside classification (C06, D-05). HS 2017 and HS 2022 are two rows."""

    class Licence(models.TextChoices):
        OPEN = "open"
        ATTRIBUTION = "attribution"
        SHARE_ALIKE = "share_alike"
        RESTRICTED = "restricted"  # HS, ISIC, CPC, UNSPSC, GPC, eCl@ss until written permission exists
        UNKNOWN = "unknown"

    key = models.SlugField(max_length=30, unique=True)  # hs2022, isic4, cpc21, unspsc, gpc, ecl, naics2022, wikidata, overture, foursquare, osm, schema_org, seed
    name = models.CharField(max_length=80)
    edition = models.CharField(max_length=20, blank=True)
    licence_class = models.CharField(max_length=12, choices=Licence.choices, default=Licence.UNKNOWN)
    publish_codes = models.BooleanField(default=False)  # codes are shown or exported only when True (decision 4 of the summary)
    source_url = models.URLField(blank=True)

    def __str__(self):
        return self.key

class ConceptCrosswalk(models.Model):
    """A mapping from one of our nodes to one outside code, with a SKOS relation (C06). Direction: the outside code is
    `relation` of our node (broad = the outside code is broader than our node). LLM proposes, a person approves; a
    proposed or rejected row is never shown. Unmapped is a valid state (see CrosswalkReview)."""

    class Relation(models.TextChoices):
        EXACT = "exact"  # skos:exactMatch
        CLOSE = "close"  # skos:closeMatch
        BROAD = "broad"  # skos:broadMatch: the outside code is broader than our node
        NARROW = "narrow"  # skos:narrowMatch: the outside code is narrower than our node
        RELATED = "related"  # skos:relatedMatch

    class State(models.TextChoices):
        PROPOSED = "proposed"
        APPROVED = "approved"
        REJECTED = "rejected"

    concept = models.ForeignKey(Concept, on_delete=models.CASCADE, related_name="crosswalks")
    # Old columns, kept until the backfill is checked, then dropped in the contract step.
    system = models.CharField(max_length=20, blank=True)
    match_type = models.CharField(max_length=10, blank=True, default="exact")
    # New columns.
    scheme = models.ForeignKey(ClassificationScheme, null=True, on_delete=models.PROTECT, related_name="crosswalks")
    code = models.CharField(max_length=80)
    code_label = models.CharField(max_length=200, blank=True)
    relation = models.CharField(max_length=8, choices=Relation.choices, default=Relation.EXACT)
    state = models.CharField(max_length=8, choices=State.choices, default=State.PROPOSED)
    confidence = models.FloatField(null=True, blank=True)
    proposed_by = models.CharField(max_length=12, default="import")  # import, llm, staff
    evidence = models.CharField(max_length=300, blank=True)
    approved_by_id = models.BigIntegerField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=clock.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["concept", "scheme", "code"], name="uniq_crosswalk_row"),
            # exactMatch is one to one among approved rows: a node has one exact code per scheme, a code one exact node
            models.UniqueConstraint(
                fields=["concept", "scheme"],
                condition=Q(relation="exact", state="approved"),
                name="uniq_exact_per_concept_scheme",
            ),
            models.UniqueConstraint(
                fields=["scheme", "code"],
                condition=Q(relation="exact", state="approved"),
                name="uniq_exact_per_scheme_code",
            ),
            models.CheckConstraint(
                condition=Q(confidence__isnull=True) | (Q(confidence__gte=0) & Q(confidence__lte=1)),
                name="crosswalk_confidence_0_1",
            ),
            models.CheckConstraint(
                condition=~Q(state="approved") | (Q(approved_by_id__isnull=False) & Q(approved_at__isnull=False)),
                name="crosswalk_approved_has_approver",
            ),
        ]
        indexes = [models.Index(fields=["scheme", "code"], name="crosswalk_scheme_code")]

class CrosswalkReview(models.Model):
    """Records that a person looked at a node for a scheme and found no code ("none_exists"), so absence is a fact and
    not a gap. Without a row, a missing mapping means "not reviewed"."""

    class Outcome(models.TextChoices):
        NONE_EXISTS = "none_exists"
        DEFERRED = "deferred"

    concept = models.ForeignKey(Concept, on_delete=models.CASCADE, related_name="crosswalk_reviews")
    scheme = models.ForeignKey(ClassificationScheme, on_delete=models.CASCADE, related_name="+")
    outcome = models.CharField(max_length=12, choices=Outcome.choices)
    reviewed_by_id = models.BigIntegerField(null=True, blank=True)
    reviewed_at = models.DateTimeField(default=clock.now)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["concept", "scheme"], name="uniq_crosswalk_review")]
```

| Relation | SKOS term | Meaning here |
|---|---|---|
| exact | exactMatch | Same thing. One to one among approved rows: one exact code per node and scheme, one exact node per code. |
| close | closeMatch | Nearly the same, used for search, not for equivalence. |
| broad | broadMatch | The outside code is broader than our node (HS heading above our product). |
| narrow | narrowMatch | The outside code is narrower than our node. |
| related | relatedMatch | Associated, not a hierarchy. |

State flow: `proposed` (import or LLM) then `approved` (a person, with approver and time, enforced by a check) or `rejected`. Only approved rows are shown. A scheme with `publish_codes = False` (HS, ISIC, UNSPSC, GPC, eCl@ss until written permission, MD-16) hides codes from pages and exports. "No code exists" is a fact stored as a `CrosswalkReview` row; no row means "not reviewed". The old `system` and `match_type` columns are copied into the new ones by migration `0005` and dropped in the contract step.

## 6. Facet registry

```python
class FacetDef(models.Model):
    """One facet (process, material, cert, spec, moq, ...). Declared once; applies to whole subtrees through
    FacetApplicability. The registry is data: staff add facets and values without a deployment."""

    class Kind(models.TextChoices):
        ENUM = "enum"
        MULTI_ENUM = "multi_enum"
        NUMBER_BAND = "number_band"
        BOOL = "bool"
        IDENTIFIER_LIST = "identifier_list"
        PLACE_LIST = "place_list"

    class Scope(models.TextChoices):
        COMPANY = "company"  # lives in Entry.addons, on the company
        PRODUCT = "product"  # lives on the attachment (EntryConcept), per product line
        BOTH = "both"

    key = models.SlugField(max_length=40, unique=True)
    label_key = models.CharField(max_length=120)
    kind = models.CharField(max_length=16, choices=Kind.choices)
    scope = models.CharField(max_length=8, choices=Scope.choices, default=Scope.PRODUCT)
    filterable = models.BooleanField(default=True)
    show = models.CharField(max_length=1, default="P")  # P public, L locked, H hidden, I internal (as AddonField.show)
    landing_page = models.BooleanField(default=False)  # promoted facet landing page, e.g. LFP battery makers
    max_values_per_entry = models.PositiveSmallIntegerField(default=8)
    version = models.PositiveIntegerField(default=1)
    deprecated_at = models.DateTimeField(null=True, blank=True)

class FacetApplicability(models.Model):
    """The facet applies at this node and to every descendant (resolved with the closure table)."""

    facet = models.ForeignKey(FacetDef, on_delete=models.CASCADE, related_name="applicability")
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE, related_name="+")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["facet", "concept"], name="uniq_facet_applicability")]

class FacetValue(models.Model):
    """One allowed value of a facet, optionally limited to a subtree (FIFA Quality Pro only under football nodes)."""

    facet = models.ForeignKey(FacetDef, on_delete=models.CASCADE, related_name="values")
    slug = models.SlugField(max_length=60)
    label_key = models.CharField(max_length=120)
    aliases = models.JSONField(default=list, blank=True)
    only_under = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.CASCADE, related_name="+")
    scheme = models.ForeignKey(ClassificationScheme, null=True, blank=True, on_delete=models.PROTECT, related_name="+")
    code = models.CharField(max_length=40, blank=True)  # AISI, DIN, ISO 7153-1, certificate scheme id
    deprecated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["facet", "slug"], name="uniq_facet_value_slug")]

class FacetRule(models.Model):
    """Allowed combinations: `forbid` (a together with b is invalid) or `require` (a needs some value of b's facet)."""

    class Kind(models.TextChoices):
        FORBID = "forbid"
        REQUIRE = "require"

    kind = models.CharField(max_length=8, choices=Kind.choices)
    value_a = models.ForeignKey(FacetValue, on_delete=models.CASCADE, related_name="+")
    value_b = models.ForeignKey(FacetValue, on_delete=models.CASCADE, related_name="+")
    only_under = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.CASCADE, related_name="+")

    class Meta:
        constraints = [
            models.CheckConstraint(condition=~Q(value_a=F("value_b")), name="facet_rule_distinct_values"),
            models.UniqueConstraint(fields=["kind", "value_a", "value_b", "only_under"], name="uniq_facet_rule", nulls_distinct=False),
        ]
```

`EntryFacet` holds only filterable values (company scope: `concept` is null; product scope: the node):

```python
class EntryFacet(models.Model):
    """A filterable facet value on an entry (company scope: concept is null) or on one of its attachments (product
    scope). Only filterable facets are stored here; the full record stays in Entry.addons and ValueMeta."""

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="facet_values")
    concept = models.ForeignKey("taxonomy.Concept", null=True, blank=True, on_delete=models.CASCADE, related_name="+")
    facet = models.ForeignKey("taxonomy.FacetDef", on_delete=models.PROTECT, related_name="+")
    value = models.ForeignKey("taxonomy.FacetValue", on_delete=models.PROTECT, related_name="+")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["entry", "concept", "facet", "value"], name="uniq_entry_facet", nulls_distinct=False
            )
        ]
        indexes = [
            models.Index(fields=["facet", "value", "entry"], name="entryfacet_filter"),
        ]
```

Applicability to a subtree is resolved with the closure (`FacetApplicability.concept` plus all descendants). Allowed values can be limited to a subtree (`FacetValue.only_under`: "FIFA Quality Pro" only under football). `FacetRule` forbids or requires combinations. A cap of 80 listable children under one parent is checked by the loader (`test_child_cap_blocks_81st_listable_child`); the seed's measured maximum is 15 (MEAS, `taxonomy_seed_facts.txt`). Row estimate for the narrow table: 90 million rows, about 11 GB (note 01, 2.7, `H`, not measured here).

## 7. Entry to concept membership

```python
class EntryConcept(models.Model):
    """Membership of an entry in a node (D-04, A1 to A8). One row per (entry, node). Exactly one primary row per entry.
    The place_path, listable and sort_key columns are copied from the entry by entries.services.sync_entry_concepts
    (1 to 15 rows through the primary key) and reconciled nightly, so a list page is one index range scan."""

    class Role(models.IntegerChoices):
        PRIMARY = 1
        SECONDARY = 2
        INFERRED = 3  # from Product or Speciality rows; shown only after review

    class State(models.IntegerChoices):
        PROPOSED = 1
        ACCEPTED = 2
        REJECTED = 3

    class Source(models.IntegerChoices):
        OWNER = 1
        CONTRIBUTOR = 2
        SURVEYOR = 3
        AGENT = 4
        IMPORT = 5
        INFERRED = 6
        LEGACY = 7  # copied from the old secondary_concepts table

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="memberships")
    concept = models.ForeignKey("taxonomy.Concept", on_delete=models.PROTECT, related_name="memberships")
    role = models.SmallIntegerField(choices=Role.choices, default=Role.SECONDARY)
    state = models.SmallIntegerField(choices=State.choices, default=State.PROPOSED)
    source = models.SmallIntegerField(choices=Source.choices, default=Source.CONTRIBUTOR)
    evidence_ref = models.BigIntegerField(null=True, blank=True)  # ValueMeta, Product or certificate row that supports it
    confidence = models.FloatField(null=True, blank=True)
    broad = models.BooleanField(default=False)  # evidence names only a higher node (A3); such rows list last
    rank = models.PositiveSmallIntegerField(default=0)  # owner's order among secondaries on the entry page
    added_by_id = models.BigIntegerField(null=True, blank=True)
    added_at = models.DateTimeField(default=clock.now)
    valid_to = models.DateTimeField(null=True, blank=True)
    merged_from = models.BigIntegerField(null=True, blank=True)  # NEW (C05): id of the absorbed entry this row was copied from; unmerge deletes by it
    # copied from the entry
    country_code = models.CharField(max_length=2)
    place_path = models.CharField(max_length=500)
    listable = models.BooleanField(default=False)  # entry published, not deleted or merged, and state accepted
    best_level = models.SmallIntegerField(default=3)  # 0 surveyor, 1 owner, 2 ai, 3 none
    last_verified_at = models.DateTimeField(null=True, blank=True)
    sort_key = models.IntegerField(default=0)  # (role > 1) * 100,000,000 + best_level * 1,000,000 + min(days since check, 999,999)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["entry", "concept"], name="uniq_entry_concept"),
            models.UniqueConstraint(fields=["entry"], condition=Q(role=1), name="uniq_primary_per_entry"),
            models.CheckConstraint(condition=Q(role__in=[1, 2, 3]), name="entry_concept_role"),
            models.CheckConstraint(
                condition=Q(confidence__isnull=True) | (Q(confidence__gte=0) & Q(confidence__lte=1)),
                name="entry_concept_confidence",
            ),
            models.CheckConstraint(condition=~Q(role=1) | Q(state=2), name="entry_concept_primary_accepted"),
        ]
        indexes = [
            # I3, the list page: node, then place prefix. Covering, so the page needs no heap visit.
            models.Index(
                fields=["concept", "place_path"],
                opclasses=["int4_ops", "text_pattern_ops"],
                include=["entry", "sort_key"],
                condition=Q(listable=True),
                name="ec_list",
            ),
            # I3b, place-major twin for small places and large node sets (see the benchmark, section 3.3)
            models.Index(
                fields=["place_path", "concept"],
                opclasses=["text_pattern_ops", "int4_ops"],
                include=["entry", "sort_key"],
                condition=Q(listable=True),
                name="ec_place_list",
            ),
            models.Index(fields=["state"], condition=Q(state=1), name="ec_review_queue"),  # I5
        ]
```

| ID | Rule |
|---|---|
| A1 | Exactly one primary row per entry: partial unique index `uniq_primary_per_entry` and `CHECK (role <> 1 OR state = 2)`. |
| A2 | Up to 24 secondary rows (soft warning at 10). Service check plus a database trigger (`entries/0008_entry_concept_guard.py`); legacy rows (source 7) are exempt so the backfill cannot fail. |
| A3 | `broad = true` when the evidence names only a higher node; such rows sort last. |
| A4 | `source`, `evidence_ref`, `confidence` (0 to 1, checked) and dates on every row. A secondary row without evidence stays `proposed` and is on no list page. |
| A7 | An agent can only propose (`state = proposed`); a person accepts. |
| D1 | `place_path`, `country_code`, `listable`, `best_level` and `sort_key` are copies from the entry, written by `sync_entry_concepts` (1 to 25 rows through the unique key) in the same transaction as the change, and reconciled nightly. The list page then reads one table. |
| D2 | `sort_key = tier * 100,000,000 + best_level * 1,000,000 + days since check`, tier 0 primary and open, 1 secondary and open, 2 suspected or temporarily closed, 3 closed in grace. Paid placement never enters the key (rule 4). |

```python
def tier_for(role, status):
    """List order, best first: 0 primary and open, 1 secondary and open, 2 suspected or temporarily closed, 3 closed
    and still inside the grace period. Paid placement never enters this key (rule 4)."""
    if status == Entry.Status.PERM_CLOSED:
        return 3
    if status in (Entry.Status.SUSPECTED, Entry.Status.TEMP_CLOSED):
        return 2
    return 0 if role == EntryConcept.Role.PRIMARY else 1

def sort_key_for(role, best_level, last_verified_at, now, status=Entry.Status.OPEN):
    days = 999_999 if last_verified_at is None else min(999_999, max(0, (now - last_verified_at).days))
    return tier_for(role, status) * 100_000_000 + LEVEL_RANK[best_level] * 1_000_000 + days

def sync_entry_concepts(entry, now=None, best_level=None):
    """Copy place_path, listable, best level and sort key onto the entry's membership rows (1 to 25 rows through
    uniq_entry_concept). Called by every service that changes publish state, place, deletion, merge or a check."""
    from .services import current_level

    now = now or clock.now()
    best_level = best_level or current_level(entry, now)
    listable = _listable(entry, now)
    for m in EntryConcept.objects.filter(entry=entry):
        EntryConcept.objects.filter(pk=m.pk).update(
            country_code=entry.country_code,
            place_path=entry.place_path,
            listable=listable and m.state == EntryConcept.State.ACCEPTED,
            best_level=LEVEL_RANK[best_level],
            last_verified_at=entry.last_verified_at,
            sort_key=sort_key_for(m.role, best_level, entry.last_verified_at, now, entry.status),
        )

@transaction.atomic
def set_primary(entry, concept, *, source=EntryConcept.Source.CONTRIBUTOR, evidence_ref=None, confidence=None, by_id=None):
    """Make `concept` the entry's one primary node. The old primary becomes a secondary (never lost)."""
    locked = Entry.objects.select_for_update().get(pk=entry.pk)  # serialises membership edits of one entry only
    old = EntryConcept.objects.filter(entry=locked, role=EntryConcept.Role.PRIMARY).first()
    if old and old.concept_id == concept.pk:
        return old
    if old:
        EntryConcept.objects.filter(pk=old.pk).update(role=EntryConcept.Role.SECONDARY)  # demote first: one primary at a time
    row = EntryConcept.objects.filter(entry=locked, concept=concept).first()
    if row:
        EntryConcept.objects.filter(pk=row.pk).update(role=EntryConcept.Role.PRIMARY, state=EntryConcept.State.ACCEPTED)
    else:
        row = EntryConcept.objects.create(
            entry=locked, concept=concept, role=EntryConcept.Role.PRIMARY, state=EntryConcept.State.ACCEPTED,
            source=source, evidence_ref=evidence_ref, confidence=confidence, added_by_id=by_id,
        )
    Entry.objects.filter(pk=locked.pk).update(primary_concept=concept)  # keep the denormalised copy in step
    locked.primary_concept = concept
    sync_entry_concepts(locked)
    return row

@transaction.atomic
def add_secondary(entry, concept, *, source, evidence_ref=None, confidence=None, broad=False, by_id=None):
    """Add a secondary membership. Rules: cap 24 (soft warning above 10), no duplicate, agents may only propose (A7),
    and a membership without evidence stays 'proposed' so it is not on any list page."""
    locked = Entry.objects.select_for_update().get(pk=entry.pk)
    if EntryConcept.objects.filter(entry=locked, concept=concept).exists():
        raise MembershipError("already a member of this node")
    n = EntryConcept.objects.filter(entry=locked, role=EntryConcept.Role.SECONDARY).count()
    if n >= MAX_SECONDARY:
        raise MembershipError("at most 24 secondary nodes: attach to a higher node instead (A2)")
    if concept.status != Concept.Status.ACTIVE:
        raise MembershipError("node is not active")
    evidenced = evidence_ref is not None
    agent = source == EntryConcept.Source.AGENT
    state = EntryConcept.State.ACCEPTED if (evidenced and not agent) else EntryConcept.State.PROPOSED
    row = EntryConcept.objects.create(
        entry=locked, concept=concept, role=EntryConcept.Role.SECONDARY, state=state, source=source,
        evidence_ref=evidence_ref, confidence=confidence, broad=broad, added_by_id=by_id,
        country_code=locked.country_code, place_path=locked.place_path,
    )
    sync_entry_concepts(locked)
    return row

def reconcile(limit=100000):
    """Nightly: rows whose copied columns differ from the entry. Returns the number fixed."""
    from django.db import connection

    with connection.cursor() as cur:
        cur.execute(
            """UPDATE entries_entryconcept m SET place_path = e.place_path, country_code = e.country_code
               FROM entries_entry e WHERE e.id = m.entry_id AND (m.place_path <> e.place_path OR m.country_code <> e.country_code)"""
        )
        return cur.rowcount
```

An entry has exactly one home place, so a place move rewrites `place_path` on its (at most 25) rows; there is no per-ancestor write. Counting "once at each ancestor" is done at read and roll-up time with `count(DISTINCT entry_id)` (M4).

## 8. Store rule, roll-up and virtual empty pages

Rule from the founder (D-06, E28), sizing from note 01 section 4.4 (`I`, not re-measured): at most 335M cell touches / 25 = **13.4 million stored cells** at 5M manufacturing entries, against 58.1M non-empty cells without the rule. The thin cells are answered live: one page is one index range scan.

```python
"""Store rule for roll-up cells (C08, D-06, summary decision 2): a (place, node) cell is stored when it has 25 published
members, 10 verified members, or is pinned. It is dropped below 20 and 8 (hysteresis, so a cell at the edge does
not flap). Every other cell is
answered live and costs at most 24 member rows."""

STORE_MIN_TOTAL = 25
STORE_MIN_VERIFIED = 10
DROP_BELOW_TOTAL = 20
DROP_BELOW_VERIFIED = 8
PROBE_LIMIT = STORE_MIN_TOTAL + 1


def should_store(published, verified, pinned, currently_stored):
    if pinned:
        return True
    if currently_stored:
        return published >= DROP_BELOW_TOTAL or verified >= DROP_BELOW_VERIFIED
    return published >= STORE_MIN_TOTAL or verified >= STORE_MIN_VERIFIED
```

The design adds **hysteresis**: create at 25 published or 10 verified, drop only below 20 published and 8 verified, so a cell at the edge does not flap on each recount. This is a design addition, not the founder's wording; see open decision O3. The database check is the drop rule.

```python
class RollupCell(models.Model):
    """Counts for one (place, concept) cell, including everything below the place. Only non-empty cells exist."""

    country_code = models.CharField(max_length=2)
    place_path = models.CharField(max_length=500)
    concept = models.ForeignKey("taxonomy.Concept", on_delete=models.CASCADE, related_name="+")
    total = models.PositiveIntegerField(default=0)
    published = models.PositiveIntegerField(default=0)
    verified = models.PositiveIntegerField(default=0)  # NEW: published entries with an unexpired surveyor or owner check
    pinned = models.BooleanField(default=False)  # NEW: a PlaceList row exists for this cell
    by_level = models.JSONField(default=dict)
    verified_12m = models.PositiveIntegerField(default=0)
    with_contact_pct = models.PositiveSmallIntegerField(default=0)
    updated_at = models.DateTimeField(default=clock.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["country_code", "place_path", "concept"], name="uniq_rollup_cell"),
            # Store rule with hysteresis: a cell is created at 25 published members or 10 verified or when pinned (service),
            # and is dropped below 20 published and 8 verified. The check is the drop rule, so a cell in the 20 to 24 band is legal.
            models.CheckConstraint(
                condition=Q(published__gte=20) | Q(verified__gte=8) | Q(pinned=True), name="rollup_cell_store_rule"
            ),
        ]
        indexes = [models.Index(fields=["country_code", "place_path"], name="rollup_place_idx")]

class PlaceTotal(models.Model):
    """NEW. Entries per home-place subtree across all list types, kept for every place that has entries. Navigation
    ("Lahore: 12,400 entries") must not depend on RollupCell, which now stores only cells above the store rule."""

    country_code = models.CharField(max_length=2)
    place_path = models.CharField(max_length=500)
    total = models.PositiveIntegerField(default=0)
    published = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(default=clock.now)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["country_code", "place_path"], name="uniq_place_total")]
```

`PlaceTotal` keeps "Lahore: 12,400 entries" for every place that has entries, independent of the store rule, so navigation does not read `RollupCell`.

Set-based recount, per country (replaces `rollups.recount_cell`, `recount_all`, `descendant_concept_ids`): step 1 `GROUP BY (home place, ancestor node)` with `count(DISTINCT entry_id)` over the membership join closure; step 2 each place prefix is a plain `SUM` of step 1 (an entry has one home place, so no distinct is needed on the place axis); step 3 keep a cell by the store rule or pin. The code is in the design copy `analytics/recount.py`; the SQL core is:

```python
@transaction.atomic
def recount_country(country_code, now=None):
    """Exact recount of every stored cell of one country. Returns (cells_kept, cells_removed)."""
    now = now or timezone.now()
    params = {
        "cc": country_code,
        "since": now - timedelta(days=365),
        "min_total": STORE_MIN_TOTAL,
        "min_verified": STORE_MIN_VERIFIED,
        "drop_total": DROP_BELOW_TOTAL,
        "drop_verified": DROP_BELOW_VERIFIED,
    }
    with connection.cursor() as cur:
        cur.execute(LEAF_SQL, params)
        cur.execute(CELLS_SQL)
        cur.execute(KEEP_SQL, params)
        cur.execute(
            """INSERT INTO analytics_rollupcell
                 (country_code, place_path, concept_id, total, published, verified, pinned, by_level, verified_12m, with_contact_pct, updated_at)
               SELECT %(cc)s, place_path, concept_id, total, published, verified, pinned,
                      jsonb_build_object('surveyor', l0, 'owner', l1, 'ai', l2, 'none', l3), verified_12m,
                      CASE WHEN published > 0 THEN round(100.0 * with_contact / published) ELSE 0 END, %(now)s
               FROM _keep
               ON CONFLICT (country_code, place_path, concept_id) DO UPDATE SET
                 total = EXCLUDED.total, published = EXCLUDED.published, verified = EXCLUDED.verified, pinned = EXCLUDED.pinned,
                 by_level = EXCLUDED.by_level, verified_12m = EXCLUDED.verified_12m,
                 with_contact_pct = EXCLUDED.with_contact_pct, updated_at = EXCLUDED.updated_at""",
            {**params, "now": now},
        )
        kept = cur.rowcount
        cur.execute(
            """DELETE FROM analytics_rollupcell r WHERE r.country_code = %s
               AND NOT EXISTS (SELECT 1 FROM _keep k WHERE k.place_path = r.place_path AND k.concept_id = r.concept_id)""",
            [country_code],
        )
        removed = cur.rowcount
    return kept, removed
```

Reference timings for why the old loop cannot stay (MEAS, `b03b_rollup_real.txt`, other script, same repository code): `recount_cell` on 1k entries 8.83 s against 60 ms in one SQL statement (225x); on 100k entries 142.48 s against 455 ms (307x); one edited entry touches 12 cells and the real code scans 303,000 entries; `refresh_for_entry` for one edit took 513.1 s. Delta apply with batching (MEAS, `b03c_rollup_delta.txt`): 3.804 ms per entry at batch 1, 0.107 ms at batch 1,000 (9,367 entries/s), 4 parallel consumers with SKIP LOCKED 20,307 entries/s, zero difference to an exact recount after each run.

### How virtual (empty or thin) pages resolve

```python
def member_rows(place, concept):
    """Listable memberships of the node and every node below it, at the place and every place below it."""
    nodes = ConceptClosure.objects.filter(ancestor_id=concept.pk).values("descendant_id")
    return EntryConcept.objects.filter(listable=True, concept_id__in=nodes).filter(place_q(place.path))

def first_page(place, concept, limit=25):
    ids = list(
        member_rows(place, concept)
        .values("entry_id")
        .annotate(sk=Min("sort_key"))  # an entry in two nodes under X is listed once, at its best position
        .order_by("sk", "entry_id")
        .values_list("entry_id", flat=True)[:limit]
    )
    by_id = {e.pk: e for e in Entry.objects.filter(pk__in=ids)}
    return [by_id[i] for i in ids if i in by_id]

def probe(place, concept, limit=PROBE_LIMIT):
    """How many distinct members, counted up to `limit`. Used where no stored cell exists."""
    ids = member_rows(place, concept).values_list("entry_id", flat=True).distinct()[:limit]
    return len(list(ids))

def nearest_populated(place, concept):
    """Links for an empty or thin page: same node at the parent places, child places that have it, parent nodes here."""
    up = {
        c.place_path: c
        for c in RollupCell.objects.filter(concept=concept, place_path__in=_ancestor_paths(place.path), published__gt=0)
    }
    same_node_up = next((up[p] for p in _ancestor_paths(place.path) if p in up), None)
    node_ids = list(ConceptClosure.objects.filter(descendant_id=concept.pk).exclude(ancestor_id=concept.pk).order_by("depth").values_list("ancestor_id", flat=True))
    parent_nodes = list(RollupCell.objects.filter(place_path=place.path, concept_id__in=node_ids, published__gt=0).order_by("total")[:3])
    prefix = place.path + "." if place.path else ""
    children = list(
        RollupCell.objects.filter(concept=concept, place_path__startswith=prefix, published__gt=0)
        .exclude(place_path=place.path)
        .order_by("-published")[:5]
    )
    return {"parent_place": same_node_up, "parent_nodes": parent_nodes, "child_places": children}

def resolve_list(place, concept, index_threshold=10):
    cell = RollupCell.objects.filter(place_path=place.path, concept=concept).order_by("-total").first()
    if cell:
        indexable = cell.pinned or cell.verified >= index_threshold
        return ListResolution(
            "stored", 200, "index,follow" if indexable else "noindex,follow", cell, cell.total, in_sitemap=indexable
        )
    n = probe(place, concept)
    if n == 0:
        return ListResolution("virtual_empty", 200, "noindex,follow", None, 0, False, nearest_populated(place, concept))
    return ListResolution("live", 200, "noindex,follow", None, n, False, nearest_populated(place, concept))
```

| Request | Condition | Answer |
|---|---|---|
| Stored cell | `RollupCell` exists | 200. Indexable (`index,follow`, in sitemap) only if pinned or verified >= `index_threshold` (default 10); otherwise `noindex,follow`. |
| Live | No cell, probe finds 1 to 25 distinct members | 200, `noindex,follow`, rows from the membership index, links to nearest populated lists. Not in the sitemap. |
| Virtual empty | No cell, probe finds 0, slug and place both exist | 200, `noindex,follow`, "add the first entry" action and nearest links: same node at the nearest populated parent place, parent nodes at this place (up to 3, smallest first), child places that have the node (up to 5, largest first). Never a 404 (C11). |
| Unknown | Slug not in `ConceptSlug` or place not found | 404 (`test_unknown_slug_or_place_is_404_not_virtual`). |

Probe cost: the live page for a small cell is 0.8 ms (closure) in the saved plan (MEAS, `taxonomy_plans.txt`); the probe is `LIMIT 26`, so a thin cell never costs more than 26 member rows. The sitemap lists stored indexable cells only (the repository's existing full-scan sitemap took 164.8 s for one index, MEAS `b09_sitemap.txt`; the precomputed table took 1.8 s for 106,667 URLs; that script died before its 5M-URL step, see K7).

Sector and world cells over 100k members are served from the stored cell plus a cached top-N page, never by a live scan (section 2, point 5).

## 9. Zero-downtime migration plan

Principles: expand, backfill, dual-write, verify, switch, contract. Every migration adds, none drops. Each step is reversible until the contract step. All migrations run with `lock_timeout = 3s` and a retry, because a waiting `ALTER` queues every later reader behind it. Lock durations for these exact steps were NOT measured (`b07_migration_locks.py` and `taxonomy_12_ddl_locks.py` have no result files); the rules below are standard PostgreSQL behaviour `I` until those runs exist.

| Step | Migration or job | What it does | Lock and risk | Rollback |
|---|---|---|---|---|
| E1 | `taxonomy/0004_depth_designs` | New tables (edge, closure, slug, change, scheme, review, facet x4); nullable columns on `Concept` (level, merged_into, retired_at); `PlaceList.reason`; checks on `Concept` (tens of thousands of rows) | New tables: none for readers. Checks on `Concept` scan a small table. | Reverse migration |
| E2 | `taxonomy/0005_backfill_graph` | Idempotent: one primary edge per parent link; `level` by recursion; closure by recursion; `ConceptSlug` from list-type slugs; schemes from `ConceptCrosswalk.system` | Small tables, one transaction | Truncate new tables |
| E3 | `taxonomy/0006_graph_guards` | Trigger on edge insert | Trigger creation takes a short lock on a small table | Drop trigger |
| E4 | `entries/0007_depth_designs` | `EntryConcept`, `EntryFacet`, `Brand`, `MergeEvent`, `EntryStatusEvent`, `ClosureSignal`; `Entry.closure_score`, `moved_to`, `brand`; status choice `suspected_closed` | **The foreign keys from new tables to `entries_entry` need a lock on `entries_entry` while they are added.** Create the new tables with `db_constraint=False` or add the FK `NOT VALID` then `VALIDATE`; nullable FK columns on `Entry` the same way (design copy uses plain `AddField`; change it). The `choices` change is a no-op in SQL. | Reverse migration |
| E4b | `analytics/0004_depth_designs` | `PlaceTotal`; `RollupCell.verified`, `pinned`; **check constraint added `NOT VALID`** through `SeparateDatabaseAndState`, so existing small cells do not block the deploy | `NOT VALID` takes a brief lock and checks no rows | Drop constraint |
| E5 | Command `backfill_entry_concept` (not a migration) | Copies `primary_concept` (role 1) and `secondary_concepts` (role 2, source 7 legacy) into `EntryConcept`, `ON CONFLICT DO NOTHING`, resumable, idempotent. **Batch 5,000 entries**, throttled by replica lag; the design copy uses 50,000, lower it. | Measured on 1M rows (b06, MEAS): one UPDATE 11.4 s with a 11,074 ms stall of concurrent traffic; fixed 5,000-row batches 10.5 s, max stall 128 ms, replica lag 2.8 MB / 0.09 s; throttled adaptive 19.7 s, max stall 134 ms | Truncate `EntryConcept` |
| E5b | `entries/0009_entry_concept_indexes` (non-atomic) | Create `ec_list` (covering, partial `WHERE listable`) and `ec_review_queue` with `CREATE INDEX CONCURRENTLY` **after** the backfill. The table keeps only the primary key and the two unique constraints during the load. | 5.96M rows: indexes after load 15.6 s total (6.6 s copy + 9.0 s index), WAL 0.60 GB; indexes first 60.9 s, WAL 2.98 GB (MEAS, `taxonomy_08_inserts.log`) | Drop index |
| E6 | Code release | Dual-write: `set_primary`, `add_secondary`, place move, publish, merge and check services call `sync_entry_concepts`. Nightly `reconcile`. | Write path adds 1 to 25 keyed updates | Flag off |
| E7 | Shadow compare | For two weeks run both read paths; log pages where the new count is below the old count (must be none) and where it is above (explained by secondary routes). Run `check_consistency()` and `reconcile()` nightly: all zero. | Read only | None needed |
| E8 | First set-based recount, per country, in country order | Writes `RollupCell` with `verified`, `pinned`; prunes cells below the drop rule; fills `PlaceTotal` | Per country transaction; hot cells never updated per entry | Keep old cells until switch |
| E9 | `VALIDATE CONSTRAINT rollup_cell_store_rule` | After pruning | Takes `SHARE UPDATE EXCLUSIVE`, does not block writes | None needed |
| E10 | Switch reads (flag `LIST_READ_FROM=entry_concept`) | List pages, counts, sitemap, nearest links read the new path; `ec_place_list` added `CONCURRENTLY` only if p95 of sector-level pages exceeds the agreed budget (it halved the L1 median from 241 to 127 ms but cost 14 to 16% of insert rate, MEAS) | Index build 5.6 s on 5.96M rows (MEAS) | Flag back |
| C1 | Contract, one release later | Drop `Entry.secondary_concepts` (table `entries_entry_secondary_concepts`); drop `ConceptCrosswalk.system` and `match_type`, make `scheme` non-null; drop `ReservedSlug` list-type rows; make `Concept.level` non-null once all rows have it | Dropping a table or column after nothing reads it | Restore from backup only; hence a release gap |

`Concept.parent` is never dropped: it is the denormalised primary parent and `check_consistency()` compares it with the primary edge every night.

## 10. Acceptance tests (pytest names)

Written for the proof run `taxonomy_prove_design.py` (79 checks, one per name). **No saved output of that run exists** (the file has no result log), so every name below is a requirement to be run, not a passing test. The names are the ones to create in `backend/taxonomy/tests/`, `backend/entries/tests/`, `backend/analytics/tests/` and `backend/catalog/tests/`.

```text
test_closure_matches_edges_after_random_graph
test_add_secondary_edge_adds_ancestors_to_all_descendants
test_cycle_is_rejected
test_parent_must_be_one_level_above
test_fourth_secondary_parent_rejected
test_second_primary_edge_rejected_by_database
test_remove_secondary_edge_keeps_ancestors_reachable_by_other_path
test_remove_secondary_edge_when_node_keeps_two_parents
test_set_primary_parent_moves_subtree_and_updates_parent_column
test_descendants_one_query
test_parent_column_equals_primary_edge
test_one_primary_per_entry_db_constraint
test_set_primary_demotes_old_primary_to_secondary
test_unevidenced_secondary_not_on_list_page
test_secondary_membership_appears_on_list_page
test_agent_secondary_stays_proposed
test_secondary_cap_enforced_service_and_trigger
test_entry_counted_once_at_ancestor_with_two_routes
test_list_page_under_node_includes_secondary_parent_route
test_place_filter_includes_places_below_and_excludes_siblings
test_unpublished_entry_not_listable
test_merged_or_deleted_entry_not_listable
test_entry_move_updates_place_path_of_all_memberships
test_reconcile_fixes_drift
test_backfill_copies_primary_and_secondary
test_rename_writes_history_and_old_slug_301
test_old_slug_cannot_be_taken_by_other_concept
test_rename_back_to_old_slug_reuses_row
test_merge_old_slugs_redirect_to_winner
test_merge_chain_flattened_single_hop
test_merge_into_self_or_loop_rejected
test_retired_slug_returns_410
test_slug_colliding_with_place_rejected
test_entries_untouched_by_rename
test_changes_logged_and_release_assigns_version
test_db_check_slug_current_xor_retired
test_exact_match_unique_per_concept_and_scheme
test_exact_code_belongs_to_one_concept
test_approved_requires_approver_db_check
test_confidence_range_db_check
test_scheme_without_publish_flag_hides_codes
test_unmapped_review_row_is_unique_and_cleared_by_approval
test_backfill_maps_old_system_to_scheme
test_facet_not_applicable_outside_subtree
test_value_only_under_node
test_forbid_rule_blocks_combination
test_require_rule_demands_other_facet
test_enum_single_value
test_child_cap_blocks_81st_listable_child
test_facet_values_filter_list_page
test_seed_has_no_node_over_cap
test_should_store_rule_table
test_recount_stores_cell_at_25_and_not_at_24
test_recount_stores_cell_at_10_verified
test_pinned_cell_stored_when_small
test_legacy_placelist_row_does_not_pin
test_recount_rolls_up_to_every_place_and_node_above
test_recount_equals_bruteforce
test_hysteresis_keeps_cell_at_22_drops_at_19
test_database_check_rejects_cell_below_drop_rule
test_virtual_empty_returns_200_noindex_with_nearest_links
test_live_page_for_substore_cell
test_stored_cell_indexable_only_with_verified_or_pinned
test_place_total_independent_of_store_rule
test_unknown_slug_or_place_is_404_not_virtual
test_merge_unions_memberships_into_survivor
test_merged_entry_leaves_list_pages_and_survivor_appears_once
test_unmerge_restores_children_credit_and_memberships
test_unmerge_absorbed_returns_to_draft_not_published
test_second_applied_merge_of_same_absorbed_rejected_by_database
test_agent_signals_never_close_alone
test_signals_expire_and_score_recomputed
test_suspected_status_ranks_below_open_on_list
test_closed_entry_listed_last_in_grace_then_delisted
test_reopen_needs_human_and_clears_signals
test_moved_entry_changes_place_lists_and_keeps_history
test_branch_rule_table
test_brand_unique_wikidata
test_branch_counts_once_at_own_place
```

Grouping: graph and closure (`test_closure_*`, `test_add_*`, `test_remove_*`, `test_cycle_*`, `test_*_parent_*`, `test_descendants_one_query`); membership and list pages (`test_*membership*`, `test_secondary_*`, `test_place_filter_*`, `test_entry_counted_once_*`, `test_list_page_*`); slugs and merges (`test_rename_*`, `test_old_slug_*`, `test_merge_*`, `test_retired_slug_*`); crosswalk and facets (`test_exact_*`, `test_approved_*`, `test_scheme_*`, `test_facet_*`, `test_*_rule_*`, `test_value_only_under_node`); store rule and virtual pages (`test_recount_*`, `test_should_store_rule_table`, `test_hysteresis_*`, `test_pinned_*`, `test_virtual_empty_*`, `test_live_page_*`, `test_stored_cell_indexable_*`, `test_place_total_*`, `test_unknown_slug_*`); entries (`test_unmerge_*`, `test_closed_entry_*`, `test_branch_*`, `test_brand_*`, `test_agent_*`, `test_signals_*`). The last group covers C03, C05 and C13 models (`Brand`, `MergeEvent`, `EntryStatusEvent`, `ClosureSignal`) that the design copy also holds; they are listed in the migration but not specified in this note.

Added by this note (not in the proof file, to be written):

```text
test_migration_expand_steps_take_no_long_lock            (needs b07 / taxonomy_12 style measurement first)
test_backfill_entry_concept_is_resumable_after_kill
test_backfill_entry_concept_batches_never_exceed_5000
test_list_read_new_path_equals_old_path_plus_secondary    (shadow compare, E7)
test_sitemap_lists_only_stored_indexable_cells
test_check_consistency_zero_after_nightly_job
```

## 11. Every measured number, with its script and result file

All files are under `research_notes/Scale research/benchmarks/` (scripts) and `.../benchmarks/results/` (outputs). Grade MEAS unless stated.

| # | Number | Script | Result file |
|---|---|---|---|
| 1 | 50,000 concepts, levels 1/30/560/3,400/8,400/37,609 | `taxonomy_01_generate_concepts.sql` | `taxonomy_tree_stats_*.txt` |
| 2 | Parents a node: seedlike 1.02, moderate 1.10, stress 2.00 | `taxonomy_01_generate_concepts.sql`, `taxonomy_realistic_trees.sh` | `taxonomy_tree_stats_seedlike.txt`, `_moderate.txt`, `_stress.txt` |
| 3 | Closure rows 290,117 / 321,905 / 1,004,185 (5.80 / 6.44 / 20.08 a node) | same | same |
| 4 | Closure size 28 / 31 / 100 MB; ltree paths 53,579 / 70,154 / 591,833; ltree size 17 / 23 / 171 MB | same | same |
| 5 | Page latency, all variants, by cell size, node level, place level | `taxonomy_bench_queries.py`, `taxonomy_report_query_tables.py` | `taxonomy_query_raw.csv` (7,500 rows, all `ok`), `taxonomy_query_tables.md` |
| 6 | closure 3.7 / 395 ms; rcte 5.1 / 526; ltree resolver 289.6 / 808; ltree copy 1,397.4 / 4,939; place-major 8.8 / 333; closure + ltree place 8.0 / 562 (median / p95) | same | `taxonomy_query_tables.md` |
| 7 | Count query: closure 2.7 / 326; rcte 2.9 / 428; place-major 8.2 / 315; ltree resolver 200.5 / 626 | same | `taxonomy_query_tables.md` |
| 8 | Plans: execution 0.787 / 2.257 / 174.0 / 1,976.8 ms (closure), 0.163 / 1.981 / 266.2 / 1,134.3 ms (rcte) for 1 / 20 / 3,152 / 760,681 members | `taxonomy_plans.py` | `taxonomy_plans.txt` |
| 9 | Place-major index 357,662,720 bytes; build 5.6 s | `taxonomy_08_inserts.py` | `taxonomy_08_inserts.log`, `taxonomy_inserts.json` |
| 10 | Edge edit costs by child level (add 16.1 / 2.2 / 0.9 / 0.5 ms; remove 366.4 / 195.6 / 154.5 / 138.9 ms; closure rows written 1,007 / 177.5 / 61.5 / 12.5; ltree copy rewrite 7,064.1 / 2,954.4 / 1,823.1 / 1,738.9 ms, rows 47,073 / 3,839 / 794.5 / 78.5) | `taxonomy_07_graph_edits.py` | `taxonomy_07_graph_edits.log`, `taxonomy_graph_edits.json` |
| 11 | Inserts: A 1,501.6 / 2,640.1 entries/s; A+ 1,262.1 / 2,266.1; B 847.3 / 1,702.7 (1 / 4 clients); latency 0.666 / 0.792 / 1.180 ms | `taxonomy_08_inserts.py` | `taxonomy_08_inserts.log` |
| 12 | Backfill of 5,959,839 memberships: indexes first 60.9 s, WAL 2.98 GB; indexes after 15.6 s (6.6 + 9.0), WAL 0.60 GB | `taxonomy_08_inserts.py` | `taxonomy_08_inserts.log` |
| 13 | Closure rebuild 1,004,185 rows in 6.6 s, check 1.6 s, 0 missing 0 extra | `taxonomy_11b_rebuild_closure_dag.sql` | `taxonomy_11b_rebuild_closure_dag.txt` |
| 14 | First graph backfill: 49,999 edges 0.12 s, closure 282,995 rows 1.5 s, 50,000 slugs 0.17 s | `taxonomy_11_backfill_graph.sql` | `taxonomy_11_backfill_graph.txt` |
| 15 | Recall: full 100%; primary-tree 12.7%; current code 6.2%; 194 of 250 pages miss entries; mean 34.0% seen per page | `taxonomy_10_recall.sql` | `taxonomy_10_recall.txt` |
| 16 | Seed facts: 1,170 nodes (30/177/489/434/40), 21 secondary links, max 15 listable children, 26 facet keys, 559 (key, value) pairs, 0 catch-all names | `taxonomy_seed_facts.py` | `taxonomy_seed_facts.txt` |
| 17 | Real `recount_cell`: 8.83 s (1k) to 142.48 s (100k) against 60 to 455 ms in SQL (200x to 307x); 513.1 s for one edit | `b03b_rollup_real.py` (other note) | `b03b_rollup_real.txt` |
| 18 | Delta apply 3.804 ms per entry at batch 1, 0.107 at batch 1,000; 20,307 entries/s with 4 consumers | `b03c_rollup_delta.py` (other note) | `b03c_rollup_delta.txt` |
| 19 | 1M-row backfill: one UPDATE 11.4 s, stall 11,074 ms; 5,000-row batches 10.5 s, stall 128 ms; adaptive 19.7 s, stall 134 ms | `b06_backfill.py` (other note) | `b06_backfill.txt` |
| 20 | Real-code sitemap 164.8 s per index fetch; precomputed 1.8 s for 106,667 URLs | `b09_sitemap.py` (other note) | `b09_sitemap.txt` (ends in a Python error, partial) |
| 21 | 13.4M stored cells at most, 58.1M non-empty cells, 335M touches (grade `I`/`H`, from note 01, not from a run in this folder) | none | `01_manufacturing_depth_taxonomy.md` section 4.4 |

## 12. Caveats and gaps

| ID | Caveat |
|---|---|
| K1 | **Missing results.** No result file exists for `taxonomy_05_rollup_build.py` (its log `taxonomy_05_rollup_build.log` is 0 bytes; the script header says the first version was stopped when its table passed 60 million rows and 3.9 GB), `taxonomy_06_rollup_incremental.py`, `taxonomy_09_resolve_and_facets.py`, `taxonomy_12_ddl_locks.py`, `taxonomy_13_design_table_size.sql`, `b07_migration_locks.py` and `taxonomy_prove_design.py`. The machine load log `taxonomy_machine_load_2026-10-07.log` ends at 18:59 on 2026-10-07 with PostgreSQL in crash recovery (`startup recovering ...`) and a heavy `CREATE TABLE AS` running at 18:58, so those runs look interrupted by the server stop, not finished. No number from them is used. |
| K2 | The query benchmark runs do not record the graph mix. The default of `taxonomy_01_generate_concepts.sql` is the stress mix, and the stress closure row count (1,004,185) equals the rebuilt count in file 13, so the stress mix is the best reading `I`. The real seed is nearer the seedlike mix (1.02 parents), where closure and ltree are both much smaller; page timings on that graph are not measured. |
| K3 | The data is synthetic (skewed random). Percentages in the recall table and the cell-size mix are not forecasts. |
| K4 | The benchmark membership table `ec` has 6 columns and an `int` concept id. The designed `EntryConcept` is wider (about 20 columns, `bigint` ids, 5 indexes with the check and unique ones), so real rows are bigger and inserts slower than table 11. `taxonomy_13` was meant to measure that and has no result. |
| K5 | Insert rates were taken on a shared machine with other benchmarks running at times (load log shows load average 2.4 to 4.2). Treat ratios as better than absolute rates. |
| K6 | Cell counts (13.4M, 58.1M) are the arithmetic of note 01, grade `I`/`H`. The set-based build on the taxonomy data set that would confirm them did not complete. |
| K7 | `b09_sitemap.txt` is partial: it stopped at the 5,000,000-URL step on a Python placeholder error. Only the 106,667-URL numbers are valid. |
| K8 | The design code was read from an earlier design copy at `/var/tmp/benchdj/backend` (dated 2026-10-06), not from the repository, which is unchanged. That copy has not been proven by a saved test run (K1). The models and functions above are pasted from it by script. Some changes noted in section 9 (FK `NOT VALID`, batch size 5,000) are changes this note asks for on top of it. |
| K9 | Single advisory lock on all taxonomy edits is fine for staff edits but would be wrong on any entry path (D-10). Closure removal of a heavily shared edge (L2, 366 ms, 670 ms p95) is the slowest edit measured. |
| K10 | `ltree` rejection is for the membership copy and for the resolver at this scale. ltree for the place path of a small table was not tested apart from the `closure_ltplace` variant, which was slower on medium and large cells in the plan runs (8.7 s and 17.6 s for one page, MEAS `taxonomy_plans.txt`). |
| K11 | Tie risk: recursive CTE is as fast as closure on pages and needs no maintenance. If the real graph stays near 1.02 parents a node, the closure table's extra write path may not pay for itself. Re-test both on the seedlike graph before the contract step. |

## 13. Open decisions for the founder, with suggested defaults

| ID | Decision | Suggested default |
|---|---|---|
| O1 | Closure table or recursive CTE as the read path | Closure (T1). Revisit at 1M entries if seedlike pages tie. |
| O2 | Add the place-major index `ec_place_list` | Not at launch. Add when sector-level page p95 passes the budget; costs 14 to 16% of insert rate and 342 MB per 6M rows. |
| O3 | Hysteresis on the store rule (create at 25 or 10 verified, drop below 20 or 8) | Yes. It is not in D-06; it stops cells flapping. |
| O4 | Publish crosswalk codes (HS, ISIC, UNSPSC, GPC, eCl@ss) | No, until written permission and counsel's view (MD-16). `publish_codes = False` by default. |
| O5 | Batch size and throttle for the entry backfill | 5,000 entries a batch, pause on replica lag over 5 MB. |
| O6 | Run the unfinished measurements (roll-up build, facet filters, DDL lock timing, proof run) | Yes, in one session when the founder lifts the pause on heavy work; until then the migration lock rules in section 9 stay grade `I`. |
| O7 | Remove the old tables | One release after the switch (step C1), not in the same release. |
