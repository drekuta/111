#!/usr/bin/env python
import os
import sys
import threading
import time
import webbrowser


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    from django.core.management import execute_from_command_line

    host = os.getenv("APP_HOST", "127.0.0.1")
    port = os.getenv("APP_PORT", "8000")
    default_address = f"{host}:{port}"

    def _open_browser_later(url: str):
        time.sleep(1.2)
        webbrowser.open(url, new=2)

    # Dual mode:
    #   1) Server mode  : volopas_app.exe            | volopas_app.exe server
    #   2) Manage mode  : volopas_app.exe manage ...
    #                     (compat: volopas_app.exe migrate / shell / etc.)
    if len(sys.argv) == 1 or sys.argv[1] == "server":
        if len(sys.argv) >= 3 and sys.argv[1] == "server":
            default_address = sys.argv[2]
        url = f"http://{default_address}"
        threading.Thread(target=_open_browser_later, args=(url,), daemon=True).start()
        print(f"Запуск сервера Django: {url}")
        argv = [sys.argv[0], "runserver", default_address, "--noreload"]
    elif sys.argv[1] == "manage":
        argv = [sys.argv[0]] + sys.argv[2:]
    else:
        argv = sys.argv

    execute_from_command_line(argv)


if __name__ == "__main__":
    main()
