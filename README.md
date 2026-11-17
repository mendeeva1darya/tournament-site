# Любительская футбольная лига (АФЛ)

Учебный проект: сайт любительской футбольной лиги на Django.

## Структура проекта

- `config/` — настройки проекта (`settings.py`, маршруты `urls.py`)
- `main/` — единственное приложение: модели (Tournament, Team), представления, маршруты
- `templates/main/` — шаблоны: базовый каркас, главная, каталог, карточка турнира, заявка, личный кабинет, «О проекте», поиск
- `static/` — статика: `css/styles.css` (UI-kit + адаптив), `js/main.js` (мобильное меню-бургер)
- `seed.py` — скрипт с тестовыми данными (20 турниров, команды с очками)
- `db.sqlite3` — база данных (в git не входит)

## Запуск

1. Создать и активировать виртуальное окружение:
   ```
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
2. Установить зависимости: `pip install -r requirements.txt`
3. Применить миграции:
   ```
   python manage.py makemigrations main
   python manage.py migrate
   ```
4. Наполнить базу тестовыми данными: `python seed.py`
5. Создать администратора: `python manage.py createsuperuser`
6. Запустить сервер: `python manage.py runserver`

Сайт: http://127.0.0.1:8000 · Админка: http://127.0.0.1:8000/admin/
