import os
import colorama
import \
    shutil
from colorama import Fore

# Инициализация colorama для перехвата символов цвета в Windows
colorama.init(autoreset=True)
print(Fore.BLUE + "Список папок внутри заданной")


def print_all_folders(start_path_for_print):
    for root, dirs, files in os.walk(start_path_for_print):
        for dir_name in dirs:
            print(os.path.join(root, dir_name), end=" ")
            folder_path = os.path.join(root, dir_name)
            if is_folder_empty(folder_path):
                print(Fore.GREEN + "empty")
            else:
                print(Fore.RED + "no empty")


def del_empty_folders(start_path_for_del):
    count = 0
    for root, dirs, files in os.walk(start_path_for_del):
        for dir_name in dirs:
            print(os.path.join(root, dir_name), end=" ")
            folder_path = os.path.join(root, dir_name)
            if is_folder_empty(folder_path):
                print(Fore.GREEN + "empty")
                try:
                    shutil.rmtree(folder_path)
                    print(f"Папка '{folder_path}' была успешно удалена.")
                    count = count + 1
                except Exception as e:
                    print(f"Произошла ошибка при удалении папки: {e}")
            else:
                print(Fore.RED + "no empty")
    return count


def is_folder_empty(folder_path):
    # Возвращает 'True', если папка пуста, и 'False' в противном случае
    return not os.listdir(folder_path)


start_path = r'D:\YandexDisk\Труд\0_В работе\2022'
print_all_folders(start_path)
answer = ""
while answer != "y" or answer != "n":
    answer = input("delete empty folder ? y/n ")
    if answer == "y":
        print(del_empty_folders(start_path), " folders have been deleted")
        input("press any key for exit")
        break
    elif answer == "n":
        print("folder not delete")
        break
    else:
        continue
