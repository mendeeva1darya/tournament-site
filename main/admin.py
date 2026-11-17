from django.contrib import admin

from .models import Tournament, Team


class TeamInline(admin.TabularInline):
    model = Team
    extra = 1


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ("title", "city", "format", "start_date", "registration_deadline", "is_active")
    list_filter = ("format", "is_active")
    search_fields = ("title", "city", "description")
    inlines = [TeamInline]
