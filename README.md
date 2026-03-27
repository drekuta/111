# VOLPAS Lab Forms Platform (MVP)

Внутренняя система ведения форм 1–5 испытательной лаборатории (не LIMS).

## Что реализовано в этом этапе
- Архитектурная документация (`docs/architecture.md`).
- ER-модель (`docs/er-model.md`).
- Карта модулей (`docs/modules.md`).
- Модель подсистемы шаблонов и печати (`docs/template-model.md`).
- MVP реестра шаблонов.
- MVP Форма 1 (Персонал) с карточкой и вложениями.
- MVP генерации печатной формы из Word-шаблона (`.docx`) через `docxtpl`.
- Базовый современный UI на Django Templates + Bootstrap 5.

## Запуск (Docker)
```bash
docker compose up --build
```

Приложение: `http://localhost:8000`

## Технологии
- Python 3.12
- Django 5
- Django REST Framework
- PostgreSQL 16
- docxtpl

## Подключение к БД (по умолчанию)
В `config/settings.py` установлены значения по умолчанию:
- `DB_HOST=192.168.1.65`
- `DB_PORT=5432`
- `DB_NAME=my_new_db`
- `DB_USER=admin`
- `DB_PASSWORD=<558955>`

При необходимости их можно переопределить через переменные окружения.

## Сборка EXE (Windows)
Добавлен `build_exe.bat` в корне проекта.

Он:
1. Устанавливает переменные окружения для БД.
2. Проверяет наличие `PyInstaller` (и устанавливает, если его нет).
3. Собирает `dist\volopas_app.exe`.

Поведение `volopas_app.exe`:
 codex/fix-pyinstaller-typeerror-in-django-build-0l6ylc
- режим сервера (по умолчанию): `volopas_app.exe` или `volopas_app.exe server [host:port]`;
- режим команд Django: `volopas_app.exe manage <команда>` (например, `volopas_app.exe manage migrate`);
- для совместимости также поддержан прямой вызов команд без `manage` (например, `volopas_app.exe migrate`).
=======
- без аргументов: запускает сервер `http://127.0.0.1:8000`;
- с аргументами: работает как `manage.py` (например, `volopas_app.exe migrate`).
 main
