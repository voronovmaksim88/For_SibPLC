# Модуль os предоставляет множество функций для работы с операционной системой.
# Нам тут он нужен для создания папок
import os
from pathlib import Path

# Модуль shutil - это модуль стандартной библиотеки Python,
# который предоставляет набор функций для манипулирования файлами и директориями.
import shutil

# Модуль для работы с датами и временем
import datetime

# указываем путь к родительской директории в которой хранятся заявки
parent_directory = "."
# parent_directory = "D:/YandexDisk/"

# Получаем путь к папке, в которой находится этот скрипт
script_dir = Path(__file__).resolve().parent

print("Путь к папке, где лежит файл с этой программой:", script_dir)

folders = []
for item in os.listdir(parent_directory):
    if os.path.isdir(os.path.join(parent_directory, item)):
        folders.append(item)
# print(folders)


new_folders = []
for folder in folders:
    try:
        new_folder = int(folder[0:3])
    except ValueError:
        new_folder = 0
    new_folders.append(new_folder)
    # print(new_folder)
folders = new_folders

max_folder = max(new_folders)

now = datetime.datetime.now()
year = str(now.year)
month_now = str(now.month)

num_str = input(f"Введите номер последней заявки (по умолчанию {max_folder}): ")
num = int(num_str) if num_str else max_folder


month_str = input(f"Введите номер текущего месяца (по умолчанию {month_now}): ")
month = int(month_str) if month_str else month_now


folderNum = int(input("введите количество папок которое надо создать "))

for i in range(folderNum):

    # задаем имя новой папки заявки в формате NNN-MM-YYYY,
    # NNN - номер порядковый в текущем году
    # MM - месяц
    # YYYY - год
    num = num + 1
    if len(str(num)) == 1:
        num_str = "00" + str(num)
    if len(str(num)) == 2:
        num_str = "0" + str(num)
    if len(str(num)) == 3:
        num_str = str(num)
    if len(str(month)) == 1:
        month_str = "0" + str(month)

    zayavka_folder_name = num_str + "-" + month_str + "-" + year + "_"

    # создаем новую директорию
    new_directory = os.path.join(parent_directory, zayavka_folder_name)
    os.mkdir(new_directory)

    folder_directory = parent_directory + "/" + zayavka_folder_name
    new_folder_name = "Чеклисты"
    new_directory = os.path.join(folder_directory, new_folder_name)
    os.mkdir(new_directory)

    new_folder_name = "Фото и видео"
    new_directory = os.path.join(folder_directory, new_folder_name)
    os.mkdir(new_directory)

    new_folder_name = "ТЗ"
    new_directory = os.path.join(folder_directory, new_folder_name)
    os.mkdir(new_directory)

    shutil.copy(parent_directory + "/ТЗ.odt",
                parent_directory + "/" + zayavka_folder_name + "/ТЗ/" + zayavka_folder_name + "ТЗ_в1р1.odt")

    new_folder_name = "Счета входящие"
    new_directory = os.path.join(folder_directory, new_folder_name)
    os.mkdir(new_directory)

    new_folder_name = "Схема"
    new_directory = os.path.join(folder_directory, new_folder_name)
    os.mkdir(new_directory)

    new_folder_name = "ПО"
    new_directory = os.path.join(folder_directory, new_folder_name)
    os.mkdir(new_directory)

    new_folder_name = "КП"
    new_directory = os.path.join(folder_directory, new_folder_name)
    os.mkdir(new_directory)
    shutil.copy(parent_directory + "/КП.xls",
                parent_directory + "/" + zayavka_folder_name + "/КП/" + zayavka_folder_name + "_КП_в1р1.xls")

    new_folder_name = "Паспорт"
    new_directory = os.path.join(folder_directory, new_folder_name)
    os.mkdir(new_directory)

    new_folder_name = "Документы"
    new_directory = os.path.join(folder_directory, new_folder_name)
    os.mkdir(new_directory)

input("Папки созданы, нажмите enter для выхода")
