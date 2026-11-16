"""
Именованные маршруты приложения main (занятие 7, п. 3).
Ссылки в шаблонах только через {% url %}.
"""
from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("", views.home, name="home"),
    path("tournaments/", views.tournaments, name="tournaments"),
    path("standings/", views.standings, name="standings"),
    path("teams/", views.teams, name="teams"),
    path("news/", views.news, name="news"),
    path("about/", views.about, name="about"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register, name="register"),
]
