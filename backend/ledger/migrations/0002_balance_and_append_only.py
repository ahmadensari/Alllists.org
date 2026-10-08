from django.db import migrations

from core.pg import append_only, only_postgres

BALANCE_FN = """
CREATE OR REPLACE FUNCTION ledger_check_balanced() RETURNS trigger AS $$
DECLARE bad integer;
BEGIN
  SELECT count(*) INTO bad FROM (
    SELECT currency FROM ledger_ledgerposting WHERE txn_id = NEW.txn_id GROUP BY currency HAVING sum(amount_minor) <> 0
  ) t;
  IF bad > 0 THEN
    RAISE EXCEPTION 'ledger transaction % does not balance', NEW.txn_id USING ERRCODE = 'integrity_constraint_violation';
  END IF;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;
"""


class Migration(migrations.Migration):
    dependencies = [("ledger", "0001_initial"), ("core", "0002_append_only")]
    operations = [
        only_postgres(BALANCE_FN, "DROP FUNCTION IF EXISTS ledger_check_balanced();"),
        only_postgres(
            "CREATE CONSTRAINT TRIGGER ledger_posting_balanced AFTER INSERT ON ledger_ledgerposting "
            "DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION ledger_check_balanced();",
            "DROP TRIGGER IF EXISTS ledger_posting_balanced ON ledger_ledgerposting;",
        ),
        append_only("ledger_ledgertxn"),
        append_only("ledger_ledgerposting"),
    ]
