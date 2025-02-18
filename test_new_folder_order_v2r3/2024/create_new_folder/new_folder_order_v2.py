from pathlib import Path
from db_config import load_config
import mysql.connector
# pip install mysql-connector-python
# poetry add mysql-connector-python
import shutil
from colorama import init, Fore, Style
import sys

# Инициализация colorama для работы с цветами в разных терминалах
init()

# Определяем цвета используя colorama
GREEN = Fore.GREEN
RED = Fore.RED
YELLOW = Fore.YELLOW
RESET = Style.RESET_ALL

# Загружаем конфигурацию
config = load_config()

# Используем значения
password = config['password']
host = config['host']
database = config['database']
port = config['port']


def get_current_year_from_parent_folder():
    """Получает год из имени родительской папки"""
    try:
        # Получаем путь к родительской папке (на уровень выше скрипта)
        parent_dir = Path(__file__).parent.parent

        # Получаем имя папки
        folder_name = parent_dir.name

        # Ищем в имени папки 4 цифры подряд (год)
        for i in range(len(folder_name) - 3):
            possible_year = folder_name[i:i + 4]
            if possible_year.isdigit() and 2000 <= int(possible_year) <= 2100:  # Разумный диапазон лет
                return possible_year

        # Если год не найден, возвращаем текущий год
        from datetime import datetime
        return str(datetime.now().year)

    except Exception as e:
        print(f"{RED}Ошибка при определении года: {e}{RESET}")
        from datetime import datetime
        return str(datetime.now().year)


def get_order_numbers_in_folder():
    try:
        # Получаем текущую директорию
        if getattr(sys, 'frozen', False):
            # Если запущено как exe
            current_dir = Path(sys.executable).parent.parent
        else:
            # Если запущено как скрипт
            current_dir = Path(__file__).parent.parent

        # Создаем множество для хранения номеров заказов
        order_numbers = set()

        # Перебираем все элементы в текущей директории
        for item in current_dir.iterdir():
            # Проверяем, что это директория
            if item.is_dir():
                # Получаем имя директории
                dir_name = item.name

                # Проверяем, начинается ли имя с 3 цифр и извлекаем номер заказа
                if len(dir_name) >= 11 and dir_name[:3].isdigit():
                    # Берем только номер заказа (первые 11 символов)
                    order_numbers.add(dir_name[:11])

        return order_numbers

    except Exception as e:
        print(f"{RED}Ошибка при поиске номеров заказов: {e}{RESET}")
        return set()


def create_maria_db_order_dict():  # создаём словарь заказов из MariaDB
    connection_mysql = None
    cursor_mysql = None
    try:
        connection_mysql = mysql.connector.connect(**config)
        cursor_mysql = connection_mysql.cursor()
        cursor_mysql.execute("Select serial, client FROM task")
        all_orders = cursor_mysql.fetchall()
        order_dict = {}  # Изменяем на словарь
        year = get_current_year_from_parent_folder()
        for order in all_orders:
            if order[0][7:11] == year:
                order_dict[order[0]] = order[1]  # номер заказа : id клиента
        return order_dict

    except mysql.connector.Error as err:
        print(f"{RED}Ошибка: {err}{RESET}")
        return None

    finally:
        if cursor_mysql is not None:
            cursor_mysql.close()
        if connection_mysql is not None and connection_mysql.is_connected():
            connection_mysql.close()
            print("Соединение с базой данных MariaDB закрыто")


def create_maria_db_client_dict():  # создаём словарь клиентов из MariaDB
    connection_mysql = None
    cursor_mysql = None
    try:
        connection_mysql = mysql.connector.connect(**config)
        cursor_mysql = connection_mysql.cursor()
        cursor_mysql.execute("SELECT id, name FROM client")
        all_clients = cursor_mysql.fetchall()
        client_dict = {}
        for client in all_clients:
            client_dict[client[0]] = client[1]
        return client_dict

    except mysql.connector.Error as err:
        print(f"{RED}Ошибка: {err}{RESET}")
        return None

    finally:
        if cursor_mysql is not None:
            cursor_mysql.close()
        if connection_mysql is not None and connection_mysql.is_connected():
            connection_mysql.close()
            print("Соединение с базой данных MariaDB закрыто")


def create_order_folder(folder_name):
    """Создает папку для заказа и необходимые подпапки"""
    try:
        # Получаем директорию с exe файлом или скриптом
        if getattr(sys, 'frozen', False):
            # Если это exe файл
            project_dir = Path(sys.executable).parent
        else:
            # Если это обычный Python скрипт
            project_dir = Path(__file__).parent

        parent_dir = project_dir.parent

        # Создаем основную папку заказа
        order_dir = parent_dir / folder_name
        order_dir.mkdir(exist_ok=True)

        # Создаем стандартные подпапки
        subfolders = ['Чеклисты', 'Фото и видео', 'ТЗ', 'Счета входящие', 'Схема',
                      'ПО', 'Паспорт', 'КП', 'Документы']
        for subfolder in subfolders:
            subfolder_path = order_dir / subfolder
            subfolder_path.mkdir(exist_ok=True)

        # Копируем шаблон ТЗ
        template_path = project_dir / 'ТЗ.odt'
        if template_path.exists():
            destination_path = order_dir / 'ТЗ' / f'{folder_name}_ТЗ_в1р1.odt'
            shutil.copy(template_path, destination_path)
            print(f"{GREEN}Шаблон ТЗ скопирован для заказа {folder_name}{RESET}")
        else:
            print(f"{YELLOW}Внимание: Файл шаблона ТЗ не найден по пути: {template_path}{RESET}")

        # Копируем шаблон КП
        template_path = project_dir / 'КП.xls'
        if template_path.exists():
            destination_path = order_dir / 'КП' / f'{folder_name}_КП_в1р1.xls'
            shutil.copy(template_path, destination_path)
            print(f"{GREEN}Шаблон КП скопирован для заказа {folder_name}{RESET}")
        else:
            print(f"{YELLOW}Внимание: Файл шаблона КП не найден по пути: {template_path}{RESET}")

        return True

    except Exception as e:
        print(f"{RED}Ошибка при создании папки {folder_name}: {e}{RESET}")
        return False


if __name__ == "__main__":
    try:
        order_numbers_in_folder = get_order_numbers_in_folder()
        if order_numbers_in_folder:
            print(f"Найдены следующие номера заказов в папках: {sorted(order_numbers_in_folder)}")
        else:
            print(f"{RED}В текущей директории не найдены папки с номерами заказов.{RESET}")

        maria_db_order_dict = create_maria_db_order_dict()  # Теперь это словарь
        print('')
        print("словарь заказов в maria_db:")
        print(maria_db_order_dict)

        maria_db_client_dict = create_maria_db_client_dict()
        print('')
        print("словарь клиентов в maria_db:")
        print(maria_db_client_dict)

        if maria_db_order_dict is None or maria_db_client_dict is None:
            print(f"{RED}Ошибка получения данных из базы данных. Создание папок невозможно.{RESET}")
            exit(1)

        # Создаем множество существующих номеров заказов
        existing_orders = set(order_numbers_in_folder)

        # Создаем новые папки только для отсутствующих заказов
        new_orders = []
        for order_number, client_id in maria_db_order_dict.items():
            if order_number not in existing_orders:
                client_name = maria_db_client_dict.get(client_id, "Unknown")
                # Заменяем недопустимые символы в имени клиента
                client_name = "".join(c if c.isalnum() or c in " -_" else "_" for c in client_name)
                new_orders.append((order_number, client_name))

        if not new_orders:
            print(f"{GREEN}Все необходимые папки уже существуют.{RESET}")
            answer = input("для выхода нажмите enter ")
            exit(0)


        print('')
        print("новые папки будут созданы с именами:")
        for order_number, client_name in new_orders:
            print(f"{order_number}_{client_name}")

        # Счетчики для статистики
        created_count = 0
        failed_count = 0

        print(f"\nНачинаем создание папок...")
        for order_number, client_name in new_orders:
            folder_name = f"{order_number}_{client_name}"
            if create_order_folder(folder_name):
                created_count += 1
                print(f"{GREEN}Создана папка для заказа: {folder_name}{RESET}")
            else:
                failed_count += 1

        # Выводим итоговую статистику
        print(f"\nСоздание папок завершено:")
        print(f"Успешно создано: {GREEN}{created_count}{RESET}")
        if failed_count > 0:
            print(f"Не удалось создать: {RED}{failed_count}{RESET}")

        answer = input("для выхода нажмите enter ")

    except Exception as e:
        print(f"\n{RED}Произошла ошибка: {e}{RESET}")
    finally:
        input("\nНажмите Enter для завершения программы...")