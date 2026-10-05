from django.db import migrations

from core.pg import trigram_index


class Migration(migrations.Migration):
    dependencies = [("taxonomy", "0001_initial"), ("core", "0002_append_only")]
    operations = [trigram_index("taxonomy_conceptlabel", "text_fold", "conceptlabel_fold_trgm")]
