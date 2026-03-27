@echo off
setlocal EnableExtensions

:: build_exe.bat
:: - Показывает подробные ошибки в консоли
:: - Сохраняет лог сборки в build_exe.log
:: - Не закрывает окно после выполнения (pause)

set "LOG_FILE=build_exe.log"
if exist "%LOG_FILE%" del "%LOG_FILE%"

echo [1/5] Настройка переменных подключения к БД...
echo [1/5] Настройка переменных подключения к БД...>>"%LOG_FILE%"
set "DB_HOST=192.168.1.65"
set "DB_PORT=5432"
set "DB_NAME=my_new_db"
set "DB_USER=admin"
set "DB_PASSWORD=<558955>"

echo [2/5] Проверка Python...
echo [2/5] Проверка Python...>>"%LOG_FILE%"
python --version >>"%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Python не найден в PATH.
    echo [ОШИБКА] Python не найден в PATH.>>"%LOG_FILE%"
    goto :error
)

echo [3/5] Проверка PyInstaller...
echo [3/5] Проверка PyInstaller...>>"%LOG_FILE%"
python -m PyInstaller --version >>"%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo PyInstaller не найден. Устанавливаю...
    echo PyInstaller не найден. Устанавливаю...>>"%LOG_FILE%"
    python -m pip install pyinstaller >>"%LOG_FILE%" 2>&1
    if errorlevel 1 (
        echo [ОШИБКА] Ошибка установки PyInstaller.
        echo [ОШИБКА] Ошибка установки PyInstaller.>>"%LOG_FILE%"
        goto :error
    )
)

echo [4/5] Сборка EXE (подробный вывод в %LOG_FILE%)...
echo [4/5] Сборка EXE...>>"%LOG_FILE%"
python -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --name volopas_app ^
  --onefile ^
  --collect-all docxtpl ^
  manage.py

if errorlevel 1 (
    echo [ОШИБКА] Сборка завершилась с ошибкой. Смотрите %LOG_FILE%.
    echo [ОШИБКА] Сборка завершилась с ошибкой.>>"%LOG_FILE%"
    goto :error
)

echo [5/5] Проверка результата...
echo [5/5] Проверка результата...>>"%LOG_FILE%"
if not exist "dist\volopas_app.exe" (
    echo [ОШИБКА] Сборка завершилась без exe-файла: dist\volopas_app.exe
    echo [ОШИБКА] EXE не найден в dist.>>"%LOG_FILE%"
    goto :error
)

echo [УСПЕХ] Готово. Файл EXE: dist\volopas_app.exe
echo [УСПЕХ] Готово. Файл EXE: dist\volopas_app.exe>>"%LOG_FILE%"
echo Лог сохранен в %LOG_FILE%

goto :finish

:error
echo.
echo Лог сохранен в %LOG_FILE%
echo Откройте лог и проверьте последние ошибки.

:finish
echo.
pause
endlocal
