@echo off
setlocal

echo [1/4] Настройка переменных подключения к БД...
set "DB_HOST=192.168.1.65"
set "DB_PORT=5432"
set "DB_NAME=my_new_db"
set "DB_USER=admin"
set "DB_PASSWORD=<558955>"

echo [2/4] Проверка PyInstaller...
python -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo PyInstaller не найден. Устанавливаю...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo Ошибка установки PyInstaller.
        exit /b 1
    )
)

echo [3/4] Сборка EXE...
python -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --name volopas_app ^
  --onefile ^
  --collect-all docxtpl ^
  manage.py

if errorlevel 1 (
    echo Сборка завершилась с ошибкой.
    exit /b 1
)

echo [4/4] Готово. Файл EXE: dist\volopas_app.exe
endlocal
