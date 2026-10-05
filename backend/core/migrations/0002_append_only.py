from django.contrib.postgres.operations import TrigramExtension, UnaccentExtension
from django.db import migrations

from core.pg import DROP_FORBID_FN, FORBID_FN, append_only, only_postgres


class Migration(migrations.Migration):
    dependencies = [("core", "0001_initial")]
    operations = [
        TrigramExtension(),
        UnaccentExtension(),
        only_postgres(FORBID_FN, DROP_FORBID_FN),
        append_only("core_auditlog"),
        append_only("core_changelog"),
    ]
