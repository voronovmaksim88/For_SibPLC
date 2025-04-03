@echo off
chcp 65001 > nul
setlocal

echo === Запуск скрипта create-new-folder ===

rem Определение пути к проекту
set PROJECT_DIR=%~dp0

rem Проверка существования виртуального окружения
if not exist "%PROJECT_DIR%.venv\" (
    echo Виртуальное окружение не найдено, создаем...
    call uv venv .venv
    call "%PROJECT_DIR%.venv\Scripts\activate.bat"
    call uv pip install -e .
) else (
    call "%PROJECT_DIR%.venv\Scripts\activate.bat"
)

rem Запуск скрипта
python "%PROJECT_DIR%\main.py"

rem Вывод результата и ожидание
echo.
echo === Скрипт завершил работу ===
pause

endlocal