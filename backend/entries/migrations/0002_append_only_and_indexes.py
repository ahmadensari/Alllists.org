from django.db import migrations

from core.pg import append_only, only_postgres, trigram_index


class Migration(migrations.Migration):
    dependencies = [("entries", "0001_initial"), ("core", "0002_append_only")]
    operations = [
        trigram_index("entries_entry", "name_fold", "entry_name_fold_trgm"),
        trigram_index("entries_namevariant", "text_fold", "namevariant_fold_trgm"),
        append_only("entries_verificationevent"),
        append_only("entries_consentrecord"),
        # a published entry needs a place and a name; plain checks the application also enforces
        only_postgres(
            "ALTER TABLE entries_entry ADD CONSTRAINT entry_name_not_blank CHECK (length(trim(name)) > 0);",
            "ALTER TABLE entries_entry DROP CONSTRAINT IF EXISTS entry_name_not_blank;",
        ),
    ]
