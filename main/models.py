
from django.conf import settings
from django.db import models


class Tournament(models.Model):
    class Format(models.TextChoices):
        FIVE = "5x5", "5 на 5"
        EIGHT = "8x8", "8 на 8"
        ELEVEN = "11x11", "11 на 11"

    title = models.CharField("Название", max_length=120)
    slug = models.SlugField("URL", max_length=140, unique=True)
    description = models.TextField("Описание", blank=True)
    city = models.CharField("Город", max_length=80)
    format = models.CharField(
        "Формат",
        max_length=5,
        choices=Format.choices,
        default=Format.FIVE,
    )
    start_date = models.DateField("Старт")
    registration_deadline = models.DateField("Приём заявок до")
    max_teams = models.PositiveSmallIntegerField(
        "Макс. команд",
        default=12,
    )
    prize_fund = models.CharField(
        "Призовой фонд",
        max_length=80,
        blank=True,
    )
    cover = models.ImageField(
        "Обложка",
        upload_to="covers/",
        blank=True,
        null=True,
    )
    is_active = models.BooleanField("Активен", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start_date"]
        verbose_name = "Турнир"
        verbose_name_plural = "Турниры"

    def __str__(self):
        return self.title

    @property
    def teams_count(self):
        return self.teams.count()

    @property
    def free_slots(self):
        return max(self.max_teams - self.teams_count, 0)


class Team(models.Model):
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name="teams",
        verbose_name="Турнир",
    )
    name = models.CharField("Команда", max_length=100)
    captain = models.CharField(
        "Капитан",
        max_length=100,
        blank=True,
    )
    points = models.PositiveSmallIntegerField("Очки", default=0)
    wins = models.PositiveSmallIntegerField("Победы", default=0)
    draws = models.PositiveSmallIntegerField("Ничьи", default=0)
    losses = models.PositiveSmallIntegerField("Поражения", default=0)
    goals_for = models.PositiveSmallIntegerField("Забито", default=0)
    goals_against = models.PositiveSmallIntegerField(
        "Пропущено",
        default=0,
    )

    class Meta:
        ordering = ["-points", "-goals_for"]
        verbose_name = "Команда"
        verbose_name_plural = "Команды"
        unique_together = ["tournament", "name"]

    def __str__(self):
        return self.name

    @property
    def games(self):
        return self.wins + self.draws + self.losses

    @property
    def goals_diff(self):
        diff = self.goals_for - self.goals_against
        return f"+{diff}" if diff > 0 else str(diff)


class Application(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="applications",
        verbose_name="Пользователь",
    )

    class Status(models.TextChoices):
        NEW = "new", "На модерации"
        ACCEPTED = "accepted", "Принята"
        REJECTED = "rejected", "Отклонена"

    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name="applications",
        verbose_name="Турнир",
    )
    team_name = models.CharField(
        "Название команды",
        max_length=100,
    )
    captain = models.CharField(
        "Капитан",
        max_length=100,
    )
    phone = models.CharField(
        "Телефон капитана",
        max_length=20,
    )
    players_count = models.PositiveSmallIntegerField(
        "Игроков в заявке",
        default=8,
    )
    status = models.CharField(
        "Статус",
        max_length=10,
        choices=Status.choices,
        default=Status.NEW,
    )
    created_at = models.DateTimeField(
        "Подана",
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return f"{self.team_name} → {self.tournament.title}"
