# Hot-path solutions: roll-ups, audit chain, partitioning, backfills, migration lint, pgBouncer, sitemaps

Date: 2026-10-08. Covers challenges C16 to C24 of `03_capabilities_and_skills_matrix.md` and the write hot spots in `02_big_site_architecture.md` (3.1, 3.7, 3.8). English only.

## 0. How to read this note

- Every number comes from a saved file in `research_notes/Scale research/benchmarks/results/`. Grade: **M** = measured by us on the scratch machine below (grade R/S do not apply; these are first-hand but small-scale). **I** = inference, inputs stated. **H** = hypothesis, not measured.
- No new benchmark was run for this note. The scratch servers were shut down on purpose and heavy work is paused. Anything a result file does not contain is marked NOT MEASURED. Nothing is invented.
- Machine (M, from `taxonomy_machine_load_2026-10-07.log` and `nproc`/`free` at writing): 4 vCPU, 15 GB RAM, one local PostgreSQL 16 (Ubuntu package), client and server on the same box. The load log shows load average about 3 to 4 on 4 cores during the 2026-10-07 runs, because other benchmarks (a `CREATE TABLE AS` and a search query at about 95 percent CPU each) ran at the same time. **Every timing from 2026-10-07 (b03c, b05, b06, b08, b09) is therefore pessimistic and noisy.** Treat ratios as solid and absolute seconds as upper bounds. Disk type is not recorded (gap).
- Not hardware you would run production on. Absolute numbers will differ; the shapes (what scales with what) are the finding.

### Status of the result files (read this before trusting a number)

| File | Status |
|---|---|
| `b01_audit_real.txt` | Complete. |
| `b02_full.txt` / `b02_writers_run1.txt` | **Interrupted.** Writer tables complete, sealer line complete, then a Python traceback (`NoActiveSqlTransaction` in `verify_seals`). |
| `b02_seal_verify.txt` | Complete re-run of the seal, verify, tamper and deadlock parts after the fix. |
| `b02b_repeat.txt` | Complete (3 rounds, median and range). It repeats only the writer variants. |
| `b02_audit_alternatives.txt` | **Empty** (one newline). Do not cite. |
| `b03b_rollup_real.txt` | Complete; the real-code figures are slow and were measured once each. |
| `b03c_rollup_delta.txt` | Complete. Written 2026-10-07 under machine load. |
| `b04_partition_5m.py` | **No result file saved.** The 5M-row partition numbers (40 vs 250 partitions, planning time, DEFAULT trap) are NOT MEASURED here. |
| `b05_real_schema_partition.txt` | Complete (1M rows, real Django schema). |
| `b06_backfill.txt` | **Partial.** The three variants and the verification are complete. The "resume after kill" section prints only its header, and the "OFFSET versus keyset" section is missing. Resume behaviour is therefore NOT MEASURED; the script has it, the result does not. |
| `b07_migration_locks.py` | **No result file saved.** Lock-queue stall times, `CREATE INDEX CONCURRENTLY` cost, NOT VALID/VALIDATE cost are NOT MEASURED. |
| `squawk_real_migrations.txt` | Warnings list only, no summary line, no list of migrations that passed clean. Probably complete but unconfirmed. |
| `b08_pgbouncer.txt`, `b08b_django_via_pgbouncer.txt` | Complete. |
| `b09_sitemap.txt` / `_part1` | **Interrupted** at the 5,000,000-URL step (`incomplete placeholder '%'` bug in the script). |
| `b09_sitemap_part2.txt` | Complete re-run, includes the 5M step. Its "real code" line differs from part 1 (see 8). |
| `b10_partman.py` | **No result file saved.** pg_partman behaviour is NOT MEASURED. |

## 1. Summary of decisions

| # | Hot path | Decision | Headline measured number |
|---|---|---|---|
| 1 | Roll-up recount | Replace per-cell Python recount with a delta queue plus set-based SQL; nightly exact recount stays as the check | One edited entry: 513 s today vs 3.8 ms per entry delta (M) |
| 2 | Audit chain + lock 727001 | Keep a chain, but shard it (16 or 256 chains) and add periodic seals + external anchor; batch path for bulk | 8 writers: 449 rows/s now vs 1,592 (16 chains) vs 2,150 (unchained) (M) |
| 3 | Country partitioning | LIST partition by `country_code`, composite keys, hand-written SQL migration, copy-and-swap | Swap lock held 30 ms on 1M rows (M) |
| 4 | Backfills | Keyset batches, checkpoint table, lag guard, background job | Single UPDATE: 11.1 s worst stall vs 128 ms (M) |
| 5 | Migration lint | squawk in CI on `sqlmigrate` output + Django check for lock_timeout | 13 warnings in 5 existing migrations (M) |
| 6 | pgBouncer | Transaction mode, `max_prepared_statements=100`, no session advisory locks | 300 clients served by 20 server backends (M) |
| 7 | Sitemaps | Precomputed `sitemap_url` table and gzip shard files built off-line | 164.8 s per request vs 1.8 s to build once (M) |

## 2. Incremental roll-up recount (C20, C21)

### Problem and evidence

`backend/analytics/rollups.py` does `refresh_for_entry` as: for every place ancestor (up to 4) times every concept ancestor (about 3), call `recount_cell`. `recount_cell` loads every entry in the cell into Python (`_entries_in`, a list comprehension over `place_path__startswith`), then calls `current_level(e, now)` and `e.contact_set.exists()` per published entry. `recount_all` calls it for every cell. Cost is proportional to entries in the cell, times the number of cells touched by one edit.

Measured with the real code (`b03b_rollup_real.py` → `b03b_rollup_real.txt`, 1 run each, M):

| Cell | Entries | Real `recount_cell` | One SQL aggregate | Ratio |
|---|---|---|---|---|
| city, leaf | 1k | 8.83 s (8,010 queries) | 60 ms | 225x |
| province, mid | 5k | 19.46 s | 85 ms | 200x |
| province, root | 20k | 39.99 s | 209 ms | 202x |
| country, root | 100k | 142.48 s | 455 ms | 307x |

Results were identical in all four (`identical=True`). One edited entry touches 12 cells and scans 303,000 entries; the real `refresh_for_entry` took **513.1 s** for one edit (M). The same 12 cells by SQL aggregate took 3.08 s. Extrapolated to 100M entries (I, linear in cell size): a country-level cell at 10M entries would take about 4 hours per edit. This cannot run on the request path, and `recount_all` is unusable at scale.

Also noted from `b03c` (M): the exact two-stage SQL recount for 1,000,000 entries into 1,500 cells takes 7.1 s; the naive one-stage version (every entry times 4 place paths times 3 concepts) takes 72.6 s. Choose the two-stage form.

### Chosen design

1. **Exact nightly recount in SQL** (two-stage: `GROUP BY` the leaf `(country, place_path, concept)` first, then expand to ancestors). Keeps today's guarantee and is the check for everything below.
2. **Delta queue for edits.** A trigger-free design, written by the same code path that changes an entry: on publish, unpublish, delete, merge, move or level change, insert one row `(entry_id, old_cell_keys, new_cell_keys)` into `rollup_dirty`. A consumer claims batches with `FOR UPDATE SKIP LOCKED`, computes the entry's contribution before and after, and applies `+/-` to the cells in one statement, ordered by cell key to avoid deadlocks.
3. **Time sweeper.** `current_level` depends on the clock (a level expires). A sweeper selects entries whose answer changes between the last run and now, with two supporting indexes, and queues them.
4. **Fillfactor and HOT.** Set fillfactor 70 on the roll-up table and keep the updated columns un-indexed so updates stay HOT (C20).

```python
# sketch, analytics/rollup_delta.py (new file; rollups.py stays as the oracle in tests)
CLAIM = """
  DELETE FROM rollup_dirty WHERE id IN (
     SELECT id FROM rollup_dirty ORDER BY id LIMIT %s FOR UPDATE SKIP LOCKED)
  RETURNING entry_id"""

def apply_batch(cur, n=1000):
    ids = [r[0] for r in cur.execute(CLAIM, [n])]
    # contribution_now(entry) = one row per (country, ancestor path, ancestor concept) with
    # total/published/level/verified_12m/with_contact as 0/1 values
    # old contribution is stored on the entry (rollup_snapshot jsonb) so no recount is needed
    cur.execute(APPLY_DELTA_SQL, [ids])   # INSERT .. ON CONFLICT (cell) DO UPDATE SET total = total + EXCLUDED.total ...
```

Open design point: `with_contact_pct` is a percentage, not additive. Store `with_contact` as a count and derive the percentage on read (the b03c script stores counts; the percentage column becomes a view or generated value). This is a model change for `RollupCell`.

### Measured results

Script `taxonomy_06_rollup_incremental.py` and `b03c_rollup_delta.py` → `b03c_rollup_delta.txt` (M, 1,000,000 entries, 1,500 cells, one run, machine under load):

| Batch size | Median per batch | Per entry | Entries/s |
|---|---|---|---|
| 1 | 3.8 ms | 3.804 ms | 263 |
| 100 | 17.6 ms | 0.176 ms | 5,682 |
| 1,000 | 106.8 ms | 0.107 ms | 9,367 |
| 10,000 | 1,230 ms | 0.123 ms | 8,129 |

- Difference between delta table and exact recount after the single-consumer run: **0** cells.
- 4 parallel consumers (SKIP LOCKED), 19,898 entries: 0.98 s (20,307 entries/s), 0 errors, difference 0.
- Clock moved 40 days: sweeper found 33,226 entries; 1,087 ms without indexes, 292 ms with the two indexes (built in 1.0 s); applied in 3.1 s; difference 0.
- Roll-up table after 36,033 updates: 92 percent HOT, 2,781 dead tuples, 680 kB.

Compare: 0.107 ms per entry (batch 1,000) against 513 s for the real code: the batch path is the only way a bulk import can be rolled up.

### Caveats

- 1,500 cells only. At 100M entries the cell count is far higher (tens of millions); the hot-cell contention (one country root cell touched by every edit in the country) is NOT MEASURED beyond 4 consumers. Mitigation: batches coalesce per cell, and the apply sorts by cell key.
- `with_contact` and `by_level` counts in b03c are the ones the script models; verify they match the full `RollupCell` field set before building.
- Load on the machine inflates absolute times.

### Zero-downtime migration steps

1. Expand: add `with_contact` count column (nullable) and `rollup_dirty` table, fillfactor 70 on the roll-up table (no rewrite for new table; for the existing table, `ALTER TABLE ... SET (fillfactor=70)` only affects new pages).
2. Deploy code that writes to `rollup_dirty` on every entry change, with the consumer disabled by a flag. Old synchronous refresh keeps running.
3. Backfill `with_contact` from existing percentages is lossy; instead run the exact SQL recount once (7.1 s per 1M entries, I: about 12 minutes per 100M if linear) and fill the counts.
4. Enable the consumer; run the nightly exact recount in "report differences" mode for 7 days; require zero difference.
5. Switch readers to counts; remove the synchronous `refresh_for_entry` call (contract step, next release).

### Acceptance tests

- `test_rollup_delta_matches_exact_after_random_edits` (property test; edit, move, unpublish, merge, delete; difference must be 0).
- `test_rollup_delta_matches_exact_after_clock_move` (40 days).
- `test_rollup_parallel_consumers_no_lost_updates`.
- `test_refresh_path_makes_constant_queries_per_edit`.
- `test_nightly_recount_reports_zero_drift`.

### Risks

Drift if any code path changes an entry without queueing (mitigation: nightly diff alarm, and the mutation check script); hot-cell lock contention; the sweeper query on a table of 100M entries (292 ms at 1M is not linear-safe; NOT MEASURED).

## 3. Audit hash chain and the global advisory lock (C19)

### Problem and evidence

`backend/core/models.py` `audit()` takes `pg_advisory_xact_lock(727001)` for **every** audit write in the whole site, reads the last row, hashes `prev_hash + canonical row`, and inserts. The lock is held until the surrounding transaction commits, so any other work in that transaction (as in `bulk.publish`) is serialised across all writers.

Measured with the real `audit()` (`b01_audit_real.py` → `b01_audit_real.txt`, 12 s each, M):

| Hold time in the transaction | 1 writer | 8 writers (rate; p99) |
|---|---|---|
| 0 ms | 274/s | 246/s (p99 51 ms) |
| 5 ms | 97/s | 94/s (p99 189 ms) |
| 20 ms | 38/s | 30/s (p99 696 ms) |

Eight writers give no more throughput than one (it falls slightly), and p50 latency rises about 10x (3.4 ms to 31 ms at 0 ms hold; 26 ms to 221 ms at 20 ms hold).

Alternatives (`b02_audit_alternatives.py` → `b02b_repeat.txt`, median of 3 rounds, rows/s, 0 ms hold, M; `b02_full.txt` single-run figures are in line):

| Variant | 1 writer | 8 writers | 8-writer p99 |
|---|---|---|---|
| current (one chain) | 693 | 600 | 54.9 ms |
| chain16 (16 chains) | 778 | 1,365 | 20.0 ms |
| chain256 | 839 | 1,558 | 16.0 ms |
| chainC_skew (chain per country, skewed traffic) | 726 | 719 | 54.9 ms |
| unchained | 1,040 | 2,052 | 12.2 ms |
| batch500_chain (500 rows per transaction) | 28,833 | 27,417 | 295 ms |
| batch500_unchained | 29,750 | 65,667 | 137 ms |

With 5 ms of other work in the transaction: current 118 (both 1 and 8 writers), chain16 666 at 8 writers, unchained 905 at 8 writers.

Notes: the `b02_full` run (first, single round) had the one-chain "current" at 449 rows/s with 8 writers and unchained at 2,150; the repeat shows run-to-run spread of 10 to 40 percent (ranges in the file). Absolute rates in `b01` (real Django ORM) and `b02` (raw SQL) differ, as expected.

**One country chain is not a fix.** `chainC_skew` (a chain per country with realistic skew, one country with 25 percent of traffic) gave 719 rows/s, about the same as one chain. Use hash buckets, not countries.

### Chosen design

Two layers (decision for the founder in section 11):

1. **Sharded chains.** Chain id = `hash(object_uid) % 16` (start; 256 later). The advisory lock key becomes `hashtextextended('audit:' || chain_id, 0)`, so writers on different chains do not wait. A transaction that writes to more than one chain must lock in **sorted order**: the deadlock demo in `b02_seal_verify.txt` (M) shows opposite order gives a server-aborted deadlock after 1.02 s, sorted order succeeds.
2. **Periodic seal over the unchained rows (optional second step).** Writers insert rows with only a `row_hash` of their own content (no lock). A sealer every N seconds chains a block of rows into a seal (`seal_hash = sha256(prev_seal + merkle/concat of row hashes)`). Measured: 8 writers inserted at 3,878 rows/s with a 1 s sealer running (b02_full) and 1,942 rows/s in the later run (b02_seal_verify, machine under different load); sealed everything, 0 unsealed after final pass.
3. **External anchor.** Publish the latest seal hash to a write-once place (a signed message, a separate account's bucket with object lock, or a public ledger entry). This is what makes tamper detection real; see below.
4. **Bulk path.** `bulk.publish` writes audit rows in batches of 500 (28,800 rows/s with a chain, M) instead of one lock per row.

```python
# sketch, core/models.py (do not apply from this note; backend is read-only for research)
def audit(action, *, object_uid="", **kw):
    chain = int(hashlib.sha256(object_uid.encode()).hexdigest(), 16) % 16
    with connection.cursor() as cur:
        cur.execute("SELECT pg_advisory_xact_lock(hashtextextended(%s, 0))", [f"audit:{chain}"])
        prev = AuditLog.objects.filter(chain=chain).order_by("-id").values_list("hash", flat=True).first() or ""
        ...  # same canonical hash as today, plus chain in the row
```

### Tamper-detection results

`b02_seal_verify.txt` (M, 1,015,532 rows):

- Fill 1M rows by COPY: 40,424 rows/s including Python hashing. Seal 1,000,000 rows: 1.80 s (556,259 rows/s). `verify_seals` on 1,015,532 rows: 15.35 s (66,161 rows/s), intact.
- Tamper UPDATE one row: detected ("row content does not match its row_hash"). Tamper DELETE one row: detected (row count mismatch).
- **A strong attacker who rewrites the row, all hashes and all later seals is NOT detected by the database alone.** Only the external anchor mismatch caught it. Do not claim tamper-proof without the anchor.
- Per-row chain verification of one chain of 1,000,000 rows: 7.80 s; fill via batch500 chain 29.9 s (33,436 rows/s).

### Caveats

The numbers are from a 1 to 8 writer scratch test; production with web workers behind pgBouncer must use transaction-level locks (see section 7; `b08b` verified `verify_audit_chain()` stays intact through the pooler at 340 writes/s). Verification of 100M rows would take about 25 minutes at 66,000 rows/s (I). The anchor choice is not measured.

### Zero-downtime migration steps

1. Expand: add `chain smallint` (nullable, no default rewrite) and `row_hash`; create a new index `(chain, id)` concurrently.
2. Deploy writer that fills `chain`, with the old single chain frozen as chain `-1` (verify it ends cleanly).
3. Backfill old rows into `chain=-1` in keyset batches (section 5). The old chain stays valid because the stored hashes are unchanged.
4. Switch verification to "verify chain -1 once, then each chain, then seals".
5. Start anchor job and alert if the anchor does not match.

### Acceptance tests

`test_audit_chains_independent_locks`, `test_audit_multi_chain_tx_sorted_lock_order_no_deadlock`, `test_audit_tamper_update_detected`, `test_audit_tamper_delete_detected`, `test_audit_rewrite_detected_by_anchor`, `test_audit_bulk_batch_chain_valid`, `test_audit_survives_pgbouncer_transaction_mode`.

### Risks

Auditors and regulators may expect one global order (mitigation: seal gives a global order of blocks). Rows from different chains no longer have a single sequence (use `created_at` + `id`). Legal view of the anchor is for `08_trust_money_legal_solutions.md`.

## 4. Country partitioning under Django (C18)

### Problem and evidence

Django has no composite primary keys or composite foreign keys (as of the version in `.venv`; the b05 run needed raw SQL). `entries_entry` has 38 foreign keys pointing at it from other tables and 2 self-foreign keys (M, b05). PostgreSQL requires the partition key in every unique key on a partitioned table.

### Chosen design

`PARTITION BY LIST (country_code)` for `entries_entry` first; the big children follow (`entries_*`, contacts, roll-up). Primary key `(country_code, id)` and unique `(country_code, uid)`. Large countries get their own partition; the rest share small partitions; a DEFAULT partition catches new countries but **must be monitored** (attaching a new country partition scans the DEFAULT for conflicting rows). Hand-written SQL migration (`RunSQL` with state operations), not Django's autodetector. The ORM model keeps `id` as the Django `pk` for lookups, because the composite key cannot be expressed; code that gets by `uid` must also pass `country_code` where it is known so partition pruning applies.

Copy-and-swap, as tested in `b05_real_schema_partition.py`:

1. Create the partitioned table with `LIKE ... INCLUDING IDENTITY` (worked on the partitioned table) and partitions.
2. Mirror trigger on the old table for writes during the copy.
3. Copy in batches (keyset).
4. Verify row counts and a checksum.
5. In one transaction: lock the old table, drop the 38 foreign keys, rename, re-add composite FKs `NOT VALID` then `VALIDATE`.
6. For referencing tables with no `country_code` column: add the column and backfill, or use `db_constraint=False` plus an orphan check.

### Measured results

`b05_real_schema_partition.txt` (M, copy of the real `bench_django` schema, 1,000,000 entries + 2,321 live writes during the copy; one run; machine under load):

- Create partitioned table, 10 partitions + default, 15 indexes: 0.17 s.
- Copy: 34.2 s (29,241 rows/s) while a writer ran 7,863 statements; slowest statement 293 ms (mirror trigger included).
- Row count and checksum equal on both sides (1,002,321 rows).
- **Swap transaction held ACCESS EXCLUSIVE on `entries_entry` for 30 ms**, including dropping 38 foreign keys.
- Composite FKs re-added and validated on 13 tables that already carry `country_code`: 0.8 s (small tables).
- **25 tables referencing entries have no `country_code` column** (examples: `access_ad`, `access_placement`, `agents_draftentry`, `billing_order`, `entries_claim`, `entries_companysection`). This is the real work item.
- ORM create, filter, update, get by pk, delete, Contact create with composite FK: all worked. `makemigrations --check`: no changes detected.
- List query plan: index scan on the PK-country partition only (partition pruning works): `Index Cond country_code='PK' AND place_path='pk.p1.c1' AND primary_concept_id=1101 AND publish_state='published'`.

NOT MEASURED (no saved result): 5M-row load, 40 vs 250 partitions, planning time with many partitions, ATTACH with CHECK, DEFAULT-partition trap timing, `CREATE INDEX CONCURRENTLY` on the parent (`b04_partition_5m.py` exists, no result file), and pg_partman on a LIST table (`b10_partman.py`, no result file). Do not quote any partition-count number from this note.

### Caveats

- 30 ms lock is for 1M rows and an empty system; the lock is dominated by FK drops, not row count (H), but 100M rows with real traffic is NOT MEASURED.
- A copy at 29,241 rows/s means 100M rows take about 57 minutes (I, linear, ignoring index builds and contention). Index builds on the target add more.
- 38 FKs means each referencing table needs the country column; this is a schema change across 25 tables (see backfill in section 5).
- Run `pg_dump` / restore and detach tests (C18 asks for them) before cutover.

### Acceptance tests

`test_partition_swap_row_count_and_checksum_equal`, `test_partition_swap_lock_under_1s` (on a 1M-row copy), `test_partition_pruning_on_list_query` (EXPLAIN contains one partition), `test_orm_crud_on_partitioned_entry`, `test_no_orphans_after_fk_drop` (for the 25 tables without country_code), `test_makemigrations_check_clean`, `test_default_partition_stays_empty`, `test_restore_one_country_partition`.

### Risks

Django upgrades that add composite-pk support could conflict with hand SQL; queries by `uid` alone scan every partition; a country that grows past its partition size needs a second split (sub-partition by hash); the DEFAULT partition silently filling.

## 5. Batched, resumable backfills (C16)

### Problem and evidence

A single `UPDATE` over a large table holds locks and WAL, causes bloat and stalls other writers. `bulk.py` already stages in chunks and records `batch.staged_through`, so a resumable pattern exists for imports; migrations have none.

Measured (`b06_backfill.py` → `b06_backfill.txt`, 1,000,000 rows, with a foreground probe doing reads and writes throughout, M):

| Variant | Time | WAL | Table + index growth | Probe p99 | Probe max | Max replica lag |
|---|---|---|---|---|---|---|
| Single UPDATE | 11.4 s | 521 MB | 251 MB | 12.8 ms | **11,074 ms** | 25.8 MB / 0.38 s |
| Fixed 5,000-row batches, no pause | 10.5 s | 498 MB | 10 MB | 33.0 ms | 128 ms | 2.8 MB / 0.09 s |
| Throttled adaptive batches + lag guard | 19.7 s | 636 MB | 0 MB | 10.1 ms | 134 ms | 6.3 MB / 0.09 s |

After the throttled run: 0 rows still NULL, 0 rows with a wrong value.

The single UPDATE is fastest to write but stalls the probe for 11 s and bloats the table by 251 MB; batches finish in about the same time with a 128 ms worst case. The adaptive variant took about twice the time (a deliberate pause), kept p99 lowest and did not grow the table.

**Partial:** the "resume after kill" test and "OFFSET vs keyset" test in the script are not in the result file (the file ends after the header "== resume after kill =="). Resume correctness and OFFSET cost are NOT MEASURED. Keyset is used on the strength of general knowledge (H) and the script, not on a saved number.

### Chosen design

A `backfill_job` table (name, last_id, done, status, batch_size, updated_at). Each batch: `UPDATE ... WHERE id > last_id AND id <= (SELECT max(id) FROM (SELECT id FROM t WHERE id > last_id ORDER BY id LIMIT :batch))` plus `AND col IS NULL` for idempotence; update the checkpoint in the same transaction. Between batches: sleep proportional to the batch time; stop if replica lag exceeds a limit (bytes or seconds) or the foreground p95 rises. Run from a management command or background job; one runner per job (advisory lock on the job name).

```python
def run(job, batch=5000, max_lag_bytes=64_000_000):
    while True:
        if replica_lag_bytes() > max_lag_bytes: sleep(2); continue
        t0 = monotonic()
        n, last = step(job, batch)          # single transaction: update rows + move checkpoint
        if n == 0: mark_done(job); return
        sleep((monotonic() - t0) * 0.5)     # duty cycle
```

Dry run on a copy first (the C16 requirement). Estimate: 5,000-row batches ran at about 95,000 rows/s unthrottled and about 51,000 rows/s throttled (I, from 1M rows in 10.5 s and 19.7 s), so 100M rows takes about 33 minutes to 1 hour on this machine (I; real hardware with indexes and replicas will be slower).

### Zero-downtime steps

1. Expand: add the nullable column (catalog-only change).
2. Deploy code that writes the new column on every write path.
3. Run the backfill job to completion; verify zero NULL and zero wrong values (the b06 check).
4. Add constraint `NOT VALID`, then `VALIDATE CONSTRAINT`; then `SET NOT NULL` (using a validated CHECK first).
5. Contract in a later release.

### Acceptance tests

`test_backfill_batches_resume_from_checkpoint`, `test_backfill_idempotent_rerun_changes_nothing`, `test_backfill_pauses_on_replica_lag`, `test_backfill_foreground_write_latency_bounded`, `test_backfill_verifies_zero_null_zero_wrong`, `test_backfill_one_runner_per_job`.

### Risks

Row update rate hides index maintenance costs on wide tables; the lag guard needs a real replica (the lag figures here come from the scratch replica set-up in the script; its configuration is not recorded in the result); autovacuum falling behind after a very large backfill.

## 6. Migration linting in CI (C17)

### Problem and evidence

The CI workflow (`.github/workflows/python-package.yml`) checks that migrations exist, not that they are safe. Running squawk 'on `sqlmigrate` output of the project migrations (`lint_real_migrations.py`, config `squawk.toml`) gave 13 warnings across 5 migrations (`squawk_real_migrations.txt`, M):

| Rule | Where |
|---|---|
| `adding-foreign-key-constraint` | billing 0004 (twice), ledger 0004, outreach 0002 |
| `require-concurrent-index-creation` | billing 0004 (3x), ledger 0004, volunteers 0003 (2x) |
| `constraint-missing-not-valid` | billing 0004 |
| `changing-column-type` | intake 0004 (bulk pipeline) |
| `adding-required-field` | outreach 0002 |

These are on new tables or small tables today (low real risk), but the same shapes would be dangerous on a large table. The file has no total and no list of clean migrations, so "13 warnings" is my count of the lines in the file, and the number of migrations scanned is not recorded (gap).

### Chosen design

1. `squawk` in CI, run on the SQL from `python manage.py sqlmigrate` for each new migration in the pull request (script: `lint_real_migrations.py`), with `.squawk.toml` (saved at `benchmarks/squawk.toml`; pg_version 16, `assume_in_transaction=false`; excluded: prefer-text-field, ban-drop-default, transaction-nesting, prefer-robust-stmts, prefer-bigint-*, require-lock-timeout, require-statement-timeout).
2. A rule for tables: the linter fails the build on `require-concurrent-index-creation`, `adding-foreign-key-constraint`, `constraint-missing-not-valid`, `changing-column-type`, `adding-required-field` when the table is on a "large tables" list; on small/new tables a comment `-- squawk-ignore` with a reason is allowed.
3. `lock_timeout` and `statement_timeout` set centrally (role or database default, plus a Django check or `RunSQL('SET LOCAL lock_timeout...')`), not per statement; that is why those two rules are excluded. Note b08 (e): `ALTER DATABASE ... SET lock_timeout` only applies to new server connections, and the startup option `-c lock_timeout` is **rejected by pgBouncer**, so migrations should connect directly to PostgreSQL and use `SET lock_timeout` in the session.
4. Two-release rule for renames and drops (expand, then contract).

### Measured results

Only the warnings above. NOT MEASURED (`b07_migration_locks.py` has no result file): the stall that a waiting `ALTER TABLE` causes behind an old transaction, cost of `CREATE INDEX` vs `CONCURRENTLY` on 5M rows, `NOT VALID`/`VALIDATE` vs direct constraint, `int` to `bigint` rewrite vs expand and contract. The script's cases are listed in its docstring (A to F). Do not cite timings.

### Zero-downtime steps (for adopting the linter)

1. Add squawk to CI in report-only mode; record the 13 findings as the baseline.
2. Mark existing migrations as accepted (baseline file); fix new ones.
3. Switch to blocking mode after one release.

### Acceptance tests

`test_ci_lint_flags_create_index_without_concurrently` (using `benchmarks/lint_samples/`), `test_ci_lint_flags_fk_without_not_valid`, `test_ci_lint_passes_expand_pattern`, `test_migration_connection_sets_lock_timeout`, `test_migrations_use_direct_database_url_not_pooler`.

### Risks

False positives on new tables train people to ignore it; squawk's parsing of `sqlmigrate` output depends on Django version; RunPython data migrations are invisible to a SQL linter (needs a human rule: backfills go through section 5).

## 7. pgBouncer settings (C23)

### Problem and evidence

Direct connections hit `max_connections` fast: the scratch server with `max_connections=40` refused the 41st client ("too many clients already") (M, b08 part 1). Django with `CONN_MAX_AGE=0` pays a connection per request.

### Chosen settings

```
pool_mode = transaction
max_client_conn = 2000              # as tested; raise with ulimit
default_pool_size = 20              # per database/user pair; size to ~ 2-3 x CPU cores of the database
max_prepared_statements = 100       # required with psycopg 3 (see below)
```

Django: `DISABLE_SERVER_SIDE_CURSORS = True` for pooled connections is the safe default (b08b shows `iterator()` also worked with it `False`, "lucky routing", so do not rely on that), `CONN_MAX_AGE` short, no session-level advisory locks, no session `SET` (use `SET LOCAL`), and run migrations, backfills and the audit sealer on a **direct** connection.

### Measured results

`b08_pgbouncer.py` → `b08_pgbouncer.txt`, `b08b_django_via_pgbouncer.py` → `b08b_django_via_pgbouncer.txt` (M, pgBouncer and server on localhost, trust auth, no TLS, 8 s pgbench runs):

- 300 client connections x 20 queries of 20 ms: all 300 ok in 6.2 s, peak server backends 20 (the pool size).
- Cost of a new connection: 3.66 ms direct vs 0.53 ms via pgBouncer.
- pgbench select-only: direct 8 clients 36,550 tps, 30 clients 45,036 tps, 200 clients **no result** (server refused). Via pgBouncer: 8 clients 20,174 tps, 30 clients 26,427 tps, 200 clients 23,936 tps (8.4 ms average), 1,000 clients 22,123 tps (45 ms average). pgBouncer costs about 40 percent of peak throughput at low client counts (single-threaded proxy, and the test runs on the same 4 cores, I) but keeps working at 1,000 clients.
- With a new connection per transaction (`-C`), 8 clients: direct 382 tps vs pgBouncer 4,805 tps (12.6x).

Semantics in transaction mode (M):

| Feature | Result | Rule |
|---|---|---|
| `pg_advisory_xact_lock` | Works; second client waited | Safe; this is what `audit()` uses |
| `pg_advisory_lock` (session) | Second client got the lock too | **Never use** through the pooler |
| Session `SET` | Leaks to the next client (`statement_timeout=1234ms` visible to client 2) | Use `SET LOCAL` |
| Startup option `-c lock_timeout=5000` | **Rejected** ("unsupported startup parameter") | Set per database/role or in session on direct connection |
| `ALTER DATABASE .. SET lock_timeout` | Seen only by server connections opened after it | Restart/reload pool after change |
| Named `WITH HOLD` cursor | Worked ("lucky routing") | Do not rely on |
| Prepared statements, psycopg `prepare_threshold=0` or default, `max_prepared_statements=0` | **Fail**: 1 of 8 clients finished, `DuplicatePreparedStatement` | Not allowed |
| `prepare_threshold=None` with `max_prepared_statements=0` | 8/8 ok | Works but no prepared statements |
| Any threshold with `max_prepared_statements=100` | 8/8 ok | Chosen |

Real Django (`b08b`): `audit()` through a pool of 4 server connections, 6 client processes, 8 s: 2,723 writes (340/s), `verify_audit_chain()` returned intact. `QuerySet.iterator()` over 60,000 rows worked with `DISABLE_SERVER_SIDE_CURSORS` both False and True.

### Caveats

Localhost, trust auth, no TLS: real network and TLS add latency; the throughput loss may differ on separate hosts. Only one pgBouncer version/config was tested (version not recorded in the result). `pgbench` on the same 4 cores competes with the pooler for CPU.

### Zero-downtime steps

1. Install pgBouncer next to the web tier (or one pair per app host) and point only a canary web worker at it.
2. Confirm the three checks: audit chain intact, no prepared-statement errors, no leaked `SET`.
3. Move the rest of the web workers; keep the direct URL for migrations, backfills, sealer and `pg_dump`.
4. Alert on pgBouncer `cl_waiting` and `maxwait`.

### Acceptance tests

`test_audit_chain_intact_through_pooler`, `test_no_session_advisory_lock_in_codebase` (grep test for `pg_advisory_lock(`), `test_no_session_set_in_codebase`, `test_psycopg_prepared_statements_ok_with_pooler`, `test_server_side_cursor_setting_documented`, `test_migrations_use_direct_connection`.

### Risks

A single pooler is a single point of failure (run two); a long transaction in transaction mode pins a server connection; `max_prepared_statements` costs memory per client.

## 8. Precomputed sitemap files (3.8 in note 02)

### Problem and evidence

The sitemap code calls `indexable_list_cells` on request, which walks the roll-up cells with one or more queries each. Measured with the real code for PK with 160,000 roll-up cells → 106,667 indexable cells (M, `b09_sitemap.py`):

- `indexable_list_cells('PK')`: **154.9 s with 9,000 queries** in `b09_sitemap.txt` and **164.3 s with 160,002 queries** in `b09_sitemap_part2.txt`. The two runs disagree on the query count (9,000 is the Django log cap, which prints "Limit for query logging exceeded, only the last 9000 queries will be returned"; 160,002 is the count from the re-run, so the true count is about one query per cell). Time is consistent.
- One shard request (`pk-1`, 4.5 MB): 167.7 s. The index request: 164.8 s. A crawler fetching the index plus 3 shards triggers about four full scans, 659 s of database time (I from the printed figure).

### Chosen design

A table `sitemap_url (id identity, loc, lastmod, country_code, changefreq?)` filled by one SQL statement from the roll-up cells, and gzip shard files of 50,000 URLs written to object storage / the CDN origin by a job. Stable shard = `(id - 1) / 50000`, so new URLs rewrite only the last shard. The index file is written by the same job. Requests only serve files (CDN cacheable, no database).

```sql
INSERT INTO sitemap_url(loc, lastmod, country_code)
SELECT '/' || place_path || '/' || concept_slug || '/', updated_at, country_code
FROM rollup_cell WHERE published >= :threshold AND indexable;   -- indexable rule from the SEO policy
```

### Measured results

`b09_sitemap_part2.txt` (M):

- One SQL statement builds `sitemap_url` for the 106,667 URLs: **1.8 s** (part 1) / **2.5 s** (part 2). Same count as the real code (`True`).
- Writing 3 gzip shard files for 106,667 URLs: 0.4 s, total 0.5 MB.
- 5,000,000 URLs: table fill 36 s; full rebuild of 100 shard files in 12 s (428,175 URLs/s, 24 MB gzip, single process); one shard built entirely in SQL with `string_agg`: 34 ms (4.6 MB raw).
- 2,000 new URLs appended rewrite 1 shard file instead of 100.

Compared with the on-request code: 164.8 s per request versus 1.8 to 2.5 s once, then zero database time per crawler request.

### Caveats

`b09_sitemap.txt` and `_part1` are interrupted at the 5M step (script bug fixed in the re-run). The 5M table is synthetic. The measurement used 160,000 cells for one country; global scale (many countries, 50,000 URL files limit, and the 50 MB uncompressed limit of the sitemap protocol; 4.6 MB per 50,000 URLs is well within it) is inference. Machine under load.

### Zero-downtime steps

1. Create the table and job; write files to a new path.
2. Compare URL sets with the live code on a staging copy (same count test).
3. Point `/sitemap.xml` and shard URLs at the files (CDN rule or a view that streams the file).
4. Remove the on-request code later.

### Acceptance tests

`test_sitemap_files_match_indexable_cells`, `test_sitemap_shard_stable_after_append` (only last shard changes), `test_sitemap_request_makes_zero_db_queries`, `test_sitemap_shard_under_50k_urls_and_50mb`, `test_sitemap_excludes_noindex_cells`, `test_sitemap_lastmod_only_changes_when_content_changes`.

### Risks

Stale files if the job fails (alert on file age); `lastmod` lies hurt crawl trust; deleted entries leave URLs that return 404 until the next full rebuild.

## 9. Order of work

| Step | Why first |
|---|---|
| 1 Migration lint in CI (section 6) | Cheap, prevents new damage |
| 2 pgBouncer (section 7) | Needed before more web workers; audit must stay transaction-lock based |
| 3 Roll-up delta (section 2) and sitemap files (section 8) | Current code is unusable beyond about 20k entries per cell |
| 4 Audit sharding (section 3) | Before bulk import goes to production volume |
| 5 Backfill runner (section 5) | Needed by step 6 and by the `country_code` columns |
| 6 Partitioning (section 4) | Largest change; do after the others exist |

## 10. Gaps and conflicts

- No result for: b04 (5M partition layouts), b07 (lock stalls), b10 (pg_partman), b06 resume and OFFSET sections, `b02_audit_alternatives.txt` (empty), squawk summary. These are not guessed here. To fill them, the benchmark scripts need to be re-run when the founder lifts the pause on heavy work.
- Timings from 2026-10-06 and 2026-10-07 runs were taken on different loads; `b01` / `b02` / `b02b` figures for the same variant differ by 10 to 40 percent (see ranges in `b02b`).
- b09 part 1 and part 2 disagree on the query count (9,000 vs 160,002); explained above.
- Single scratch machine, localhost clients, no replica set-up detail recorded for lag numbers.
- All figures are small scale (1M to 5M rows). Extrapolations to 100M are marked I and are linear estimates only.

## 11. Open decisions for the founder, with suggested defaults

1. Audit: 16 hash-bucket chains plus periodic seals plus an external anchor? Default: yes; start with 16 chains and the anchor job, add sealing only if bulk import volume needs it.
2. Where to anchor the seal hash (write-once object store, signed email, public ledger)? Default: a write-once bucket in a separate account.
3. Partitioning: when to start? Default: design now (add `country_code` to the 25 tables), cut over at about 20M entries, not before.
4. pgBouncer: one pooler per app host or a shared pair? Default: shared pair with failover.
5. Roll-up: accept storing `with_contact` as a count and deriving the percentage? Default: yes.
6. Linter: blocking from which release? Default: report-only for one release, then block.
7. Re-run the missing benchmarks (b04, b07, b10, b06 resume) after the pause? Default: yes, one at a time, with nothing else running.
