from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),
    path("tournaments/", views.tournament_catalog, name="catalog"),
    path("tournaments/<slug:slug>/", views.tournament_detail, name="tournament_detail"),
    path("application/", views.application_form, name="application_form"),
    path("application/success/", views.application_success, name="application_success"),
    path("profile/", views.profile, name="profile"),
    path("about/", views.about, name="about"),
    path("search/", views.search, name="search"),
]
