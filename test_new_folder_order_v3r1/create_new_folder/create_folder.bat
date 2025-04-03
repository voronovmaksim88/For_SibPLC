@echo off
chcp 65001 > nul

:: Попытка 1 - стандартный путь для Python 3.13
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe" (
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe" new_folder_order_v2.py
    goto :end
)

:: Попытка 2 - стандартный путь для Python 3.12
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" (
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" new_folder_order_v2.py
    goto :end
)

:: Попытка 3 - стандартный путь для Python 3.11
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe" (
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe" new_folder_order_v2.py
    goto :end
)

:: Попытка 4 - путь для Python, установленного для всех пользователей
if exist "C:\Program Files\Python313\python.exe" (
    "C:\Program Files\Python313\python.exe" new_folder_order_v2.py
    goto :end
)

if exist "C:\Program Files\Python312\python.exe" (
    "C:\Program Files\Python312\python.exe" new_folder_order_v2.py
    goto :end
)

echo Python не найден в стандартных местах установки!
echo Пожалуйста, укажите правильный путь к Python в bat-файле.

:end
pause