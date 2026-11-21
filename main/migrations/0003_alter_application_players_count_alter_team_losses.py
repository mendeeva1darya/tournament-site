
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_application_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="application",
            name="players_count",
            field=models.PositiveSmallIntegerField(
                default=8,
                validators=[
                    django.core.validators.MinValueValidator(1)
                ],
                verbose_name="Игроков в заявке",
            ),
        ),
    ]
