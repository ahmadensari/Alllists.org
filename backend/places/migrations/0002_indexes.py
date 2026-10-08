from django.db import migrations

from core.pg import trigram_index


class Migration(migrations.Migration):
    dependencies = [("places", "0001_initial"), ("core", "0002_append_only")]
    operations = [trigram_index("places_placename", "name_fold", "placename_fold_trgm")]
