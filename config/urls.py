"""Маршруты проекта: подключаем приложение main (занятие 7, п. 3)."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
]
