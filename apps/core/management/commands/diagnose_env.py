import os
import socket
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


def _mask_secret(value: str) -> str:
    if not value:
        return "<empty>"
    if len(value) <= 2:
        return "*" * len(value)
    return f"{value[0]}{'*' * (len(value) - 2)}{value[-1]}"


class Command(BaseCommand):
    help = "Диагностика окружения Django: static files, переменные БД и проверка подключения."

    def add_arguments(self, parser):
        parser.add_argument(
            "--skip-db",
            action="store_true",
            help="Пропустить реальное подключение к БД (полезно для офлайн-проверки).",
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("=== Django environment diagnostics ==="))
        self._print_general()
        self._check_staticfiles_dirs()
        self._print_db_config()
        self._check_db_network()

        if not options["skip_db"]:
            self._check_db_connection()
        else:
            self.stdout.write(self.style.WARNING("[DB CONNECT] skipped (--skip-db)"))

        self.stdout.write(self.style.SUCCESS("=== Diagnostics finished ==="))

    def _print_general(self):
        self.stdout.write("\n[GENERAL]")
        self.stdout.write(f"BASE_DIR: {settings.BASE_DIR}")
        self.stdout.write(f"DEBUG: {settings.DEBUG}")
        self.stdout.write(f"DJANGO_SETTINGS_MODULE: {os.getenv('DJANGO_SETTINGS_MODULE', '<not set>')}")

    def _check_staticfiles_dirs(self):
        self.stdout.write("\n[STATICFILES_DIRS]")
        static_dirs = list(getattr(settings, "STATICFILES_DIRS", []))
        if not static_dirs:
            self.stdout.write(self.style.WARNING("STATICFILES_DIRS is empty."))
            return

        for item in static_dirs:
            path = Path(item)
            if path.exists():
                self.stdout.write(self.style.SUCCESS(f"OK: {path}"))
            else:
                self.stdout.write(self.style.WARNING(f"MISSING: {path}"))

    def _print_db_config(self):
        self.stdout.write("\n[DATABASE CONFIG]")
        db = settings.DATABASES.get("default", {})
        self.stdout.write(f"ENGINE: {db.get('ENGINE', '<missing>')}")
        self.stdout.write(f"NAME: {db.get('NAME', '<missing>')}")
        self.stdout.write(f"USER: {db.get('USER', '<missing>')}")
        self.stdout.write(f"PASSWORD: {_mask_secret(str(db.get('PASSWORD', '')))}")
        self.stdout.write(f"HOST: {db.get('HOST', '<missing>')}")
        self.stdout.write(f"PORT: {db.get('PORT', '<missing>')}")

    def _check_db_network(self):
        self.stdout.write("\n[DB NETWORK]")
        db = settings.DATABASES.get("default", {})
        host = db.get("HOST")
        port = db.get("PORT")

        if not host or not port:
            self.stdout.write(self.style.ERROR("HOST/PORT missing in DATABASES['default']."))
            return

        try:
            port = int(port)
        except (TypeError, ValueError):
            self.stdout.write(self.style.ERROR(f"PORT is not numeric: {port}"))
            return

        try:
            with socket.create_connection((host, port), timeout=3):
                self.stdout.write(self.style.SUCCESS(f"TCP OK: {host}:{port}"))
        except OSError as exc:
            self.stdout.write(self.style.ERROR(f"TCP FAIL: {host}:{port} -> {exc}"))

    def _check_db_connection(self):
        self.stdout.write("\n[DB CONNECT]")
        try:
            connection = connections["default"]
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                row = cursor.fetchone()
            self.stdout.write(self.style.SUCCESS(f"DB query OK: SELECT 1 -> {row}"))
        except OperationalError as exc:
            self.stdout.write(self.style.ERROR(f"DB OperationalError: {exc}"))
        except Exception as exc:
            self.stdout.write(self.style.ERROR(f"DB unexpected error: {type(exc).__name__}: {exc}"))
