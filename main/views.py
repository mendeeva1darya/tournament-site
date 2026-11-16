"""Представления занятия 7: главная страница и заглушки будущих разделов."""
from django.shortcuts import render


def home(request):
    """Главная страница по макету desktop 1440 / mobile 375 (рисунок 6.1 отчёта 6)."""
    return render(request, "main/index.html")


# Заглушки разделов: сверстаются на занятии 8 по wireframes из отчёта 6
def tournaments(request):
    return render(request, "main/stub.html", {"title": "Турниры"})


def standings(request):
    return render(request, "main/stub.html", {"title": "Турнирная таблица"})


def teams(request):
    return render(request, "main/stub.html", {"title": "Команды"})


def news(request):
    return render(request, "main/stub.html", {"title": "Новости"})


def about(request):
    return render(request, "main/stub.html", {"title": "О проекте"})


def login_view(request):
    return render(request, "main/stub.html", {"title": "Вход"})


def register(request):
    return render(request, "main/stub.html", {"title": "Регистрация"})
