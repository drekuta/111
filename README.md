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
