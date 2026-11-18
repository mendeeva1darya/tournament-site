from django.contrib import admin

from .models import Application, Tournament, Team


class TeamInline(admin.TabularInline):
    model = Team
    extra = 1


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ("title", "city", "format", "start_date", "registration_deadline", "is_active")
    list_filter = ("format", "is_active")
    search_fields = ("title", "city", "description")
    inlines = [TeamInline]


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("team_name", "tournament", "captain", "phone", "players_count", "status", "created_at")
    list_filter = ("status", "tournament")
    search_fields = ("team_name", "captain", "phone")
    list_editable = ("status",)
