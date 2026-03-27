#!/usr/bin/env python
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    from django.core.management import execute_from_command_line

    if len(sys.argv) == 1:
        # Default executable behavior: run web app instead of printing help and exiting.
        argv = [sys.argv[0], "runserver", "127.0.0.1:8000", "--noreload"]
        print("Запуск сервера Django: http://127.0.0.1:8000")
    else:
        argv = sys.argv

    execute_from_command_line(argv)


if __name__ == "__main__":
    main()
