
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ApplicationForm
from .models import Application, Team, Tournament


def index(request):
    context = {
        "tournaments": Tournament.objects.filter(
            is_active=True
        )[:6],
        "top_teams": Team.objects.select_related(
            "tournament"
        ).order_by("-points", "-goals_for")[:4],
    }

    return render(request, "main/index.html", context)


def tournament_catalog(request):
    tournaments = Tournament.objects.filter(is_active=True)

    selected_city = request.GET.get("city", "")
    selected_format = request.GET.get("format", "")

    if selected_city:
        tournaments = tournaments.filter(city=selected_city)

    if selected_format:
        tournaments = tournaments.filter(format=selected_format)

    cities = (
        Tournament.objects
        .order_by("city")
        .values_list("city", flat=True)
        .distinct()
    )

    paginator = Paginator(tournaments, 20)
    page = paginator.get_page(request.GET.get("page"))

    context = {
        "page_obj": page,
        "cities": cities,
        "selected_city": selected_city,
        "selected_format": selected_format,
    }

    return render(request, "main/catalog.html", context)


def tournament_detail(request, slug):
    tournament = get_object_or_404(
        Tournament,
        slug=slug,
        is_active=True,
    )

    teams = tournament.teams.all()

    return render(
        request,
        "main/tournament_detail.html",
        {
            "tournament": tournament,
            "teams": teams,
        },
    )


@login_required(login_url="main:login")
def application_form(request):
    if request.method == "POST":
        form = ApplicationForm(request.POST)

        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user

            # BUG-02: проверка повторной заявки
            duplicate_exists = Application.objects.filter(
                user=request.user,
                tournament=application.tournament,
                team_name__iexact=application.team_name.strip(),
            ).exists()

            if duplicate_exists:
                form.add_error(
                    None,
                    "Вы уже подали заявку от этой команды "
                    "на данный турнир."
                )
            else:
                application.save()
                request.session["application_success"] = True

                return redirect("main:application_success")

    else:
        form = ApplicationForm()

    return render(
        request,
        "main/application.html",
        {"form": form},
    )


def application_success(request):
    # BUG-07: страница доступна только после отправки заявки
    if not request.user.is_authenticated:
        return redirect("main:login")

    if not request.session.pop("application_success", False):
        return redirect("main:application_form")

    return render(
        request,
        "main/application_success.html",
    )


@login_required(login_url="main:login")
def profile(request):
    applications = (
        Application.objects
        .filter(user=request.user)
        .select_related("tournament")
        .order_by("-created_at")[:10]
    )

    return render(
        request,
        "main/profile.html",
        {"applications": applications},
    )


def about(request):
    return render(request, "main/about.html")


def search(request):
    query = request.GET.get("q", "").strip()

    results = []

    if query:
        # BUG-04: поиск без учёта регистра русских букв
        normalized_query = query.casefold()

        # BUG-08: показываем только активные турниры
        tournaments = Tournament.objects.filter(is_active=True)

        results = [
            tournament
            for tournament in tournaments
            if (
                normalized_query in tournament.title.casefold()
                or normalized_query in tournament.city.casefold()
                or normalized_query
                in (tournament.description or "").casefold()
            )
        ]

    return render(
        request,
        "main/search.html",
        {
            "query": query,
            "results": results,
        },
    )


def register(request):
    if request.user.is_authenticated:
        return redirect("main:profile")

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect("main:profile")

    else:
        form = UserCreationForm()

    return render(
        request,
        "main/register.html",
        {"form": form},
    )
