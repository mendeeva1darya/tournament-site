from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tournament",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=120, verbose_name="Название")),
                ("slug", models.SlugField(max_length=140, unique=True, verbose_name="URL")),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
                ("city", models.CharField(max_length=80, verbose_name="Город")),
                ("format", models.CharField(choices=[("5x5", "5 на 5"), ("8x8", "8 на 8"), ("11x11", "11 на 11")], default="5x5", max_length=5, verbose_name="Формат")),
                ("start_date", models.DateField(verbose_name="Старт")),
                ("registration_deadline", models.DateField(verbose_name="Приём заявок до")),
                ("max_teams", models.PositiveSmallIntegerField(default=12, verbose_name="Макс. команд")),
                ("prize_fund", models.CharField(blank=True, max_length=80, verbose_name="Призовой фонд")),
                ("cover", models.ImageField(blank=True, null=True, upload_to="covers/", verbose_name="Обложка")),
                ("is_active", models.BooleanField(default=True, verbose_name="Активен")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["start_date"],
                "verbose_name": "Турнир",
                "verbose_name_plural": "Турниры",
            },
        ),
        migrations.CreateModel(
            name="Team",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="Команда")),
                ("captain", models.CharField(blank=True, max_length=100, verbose_name="Капитан")),
                ("points", models.PositiveSmallIntegerField(default=0, verbose_name="Очки")),
                ("wins", models.PositiveSmallIntegerField(default=0, verbose_name="Победы")),
                ("draws", models.PositiveSmallIntegerField(default=0, verbose_name="Ничьи")),
                ("losses", models.PositiveSmallIntegerField(default=0, verbose_name="Поражения")),
                ("goals_for", models.PositiveSmallIntegerField(default=0, verbose_name="Забито")),
                ("goals_against", models.PositiveSmallIntegerField(default=0, verbose_name="Пропущено")),
                ("tournament", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="teams", to="main.tournament", verbose_name="Турнир")),
            ],
            options={
                "ordering": ["-points", "-goals_for"],
                "verbose_name": "Команда",
                "verbose_name_plural": "Команды",
                "unique_together": {("tournament", "name")},
            },
        ),
        migrations.CreateModel(
            name="Application",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("team_name", models.CharField(max_length=100, verbose_name="Название команды")),
                ("captain", models.CharField(max_length=100, verbose_name="Капитан")),
                ("phone", models.CharField(max_length=20, verbose_name="Телефон капитана")),
                ("players_count", models.PositiveSmallIntegerField(default=8, verbose_name="Игроков в заявке")),
                ("status", models.CharField(choices=[("new", "На модерации"), ("accepted", "Принята"), ("rejected", "Отклонена")], default="new", max_length=10, verbose_name="Статус")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Подана")),
                ("tournament", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="applications", to="main.tournament", verbose_name="Турнир")),
            ],
            options={
                "ordering": ["-created_at"],
                "verbose_name": "Заявка",
                "verbose_name_plural": "Заявки",
            },
        ),
    ]
