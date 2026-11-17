import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import datetime as dt
import random

from main.models import Tournament, Team

random.seed(2026)

cities = ["Ульяновск", "Димитровград", "Казань", "Самара", "Чебоксары"]
formats = ["5x5", "8x8", "11x11"]
names = ["Заря", "Волга-Д", "Строитель", "Ротор-Аматор", "СВЕША", "Флагман",
         "Локомотив-Д", "Спартан", "Феникс", "Марс", "Чайка", "Энергетик",
         "Текстильщик", "Купол", "Заслон", "Метеор", "Буревестник",
         "Торпедо-2", "Алмаз", "Салават"]

created_count = 0
for i, name in enumerate(names, start=1):
    fmt = formats[(i - 1) % 3]
    city = cities[(i - 1) % 5]
    start_date = dt.date(2026, 11, 21) + dt.timedelta(days=i * 3)
    tournament, created = Tournament.objects.get_or_create(
        slug=f"cup-2026-{i:02d}",
        defaults={
            "title": f"Кубок «{name}» — {fmt}",
            "description": (
                f"Открытый любительский турнир в формате {fmt}. "
                "Матчи проходят по выходным, судья — сертифицированный рефери, "
                "взнос делится между командами поровну."
            ),
            "city": city,
            "format": fmt,
            "start_date": start_date,
            "registration_deadline": start_date - dt.timedelta(days=7),
            "max_teams": random.choice([8, 10, 12, 16]),
            "prize_fund": f"{random.choice([30, 50, 80, 100])} тыс. руб.",
            "is_active": True,
        },
    )
    if not created:
        continue
    created_count += 1

    opponents = random.sample([n for n in names if n != name], 12)
    for j in range(random.randint(5, 12)):
        w = random.randint(1, 10)
        d = random.randint(0, 4)
        Team.objects.get_or_create(
            tournament=tournament,
            name=opponents[j],
            defaults={
                "captain": f"Капитан {j + 1}",
                "wins": w,
                "draws": d,
                "losses": random.randint(0, 4),
                "points": w * 3 + d,
                "goals_for": random.randint(5, 40),
                "goals_against": random.randint(2, 30),
            },
        )

print(f"Создано турниров: {created_count}")
print(f"Всего в базе: {Tournament.objects.count()} турниров, {Team.objects.count()} команд")
