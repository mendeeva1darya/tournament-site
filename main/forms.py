import datetime as dt

from django import forms

from .models import Application

# Сколько игроков допустимо в каждом формате
FORMAT_LIMITS = {
    "5x5": (8, 12),
    "8x8": (10, 16),
    "11x11": (14, 20),
}


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["tournament", "team_name", "captain", "phone", "players_count"]

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        digits = phone.replace("+", "").replace("-", "").replace(" ", "")
        digits = digits.replace("(", "").replace(")", "")
        if len(digits) != 11 or not digits.startswith(("7", "8")):
            raise forms.ValidationError(
                "Введите телефон в формате +7 (___) ___-__-__"
            )
        return phone

    def clean(self):
        cleaned = super().clean()
        tournament = cleaned.get("tournament")
        players = cleaned.get("players_count")

        if tournament and players:
            if tournament.registration_deadline < dt.date.today():
                self.add_error(
                    "tournament",
                    "Приём заявок на этот турнир уже закончился.",
                )
            if tournament.free_slots == 0:
                self.add_error(
                    "tournament",
                    "В этом турнире не осталось свободных мест.",
                )
            low, high = FORMAT_LIMITS[tournament.format]
            if not low <= players <= high:
                self.add_error(
                    "players_count",
                    f"Для формата «{tournament.get_format_display()}» "
                    f"нужно от {low} до {high} игроков.",
                )
        return cleaned
