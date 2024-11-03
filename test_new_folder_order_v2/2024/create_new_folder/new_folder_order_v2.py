from pathlib import Path
from db_config import load_config
import mysql.connector

# Модуль shutil - это модуль стандартной библиотеки Python,
# который предоставляет набор функций для манипулирования файлами и директориями.
import shutil

# Цветовые коды ANSI
GREEN = '\033[92m'  # Зеленый цвет
RED = '\033[91m'  # Красный цвет
RESET = '\033[0m'  # Сброс цвета
YELLOW = '\033[93m'  # Желтый цвет

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
    # Получаем текущую директорию, где находится скрипт
    current_dir = Path(__file__).parent.parent  # Переход на уровень выше

    # Создаем множество для хранения номеров заказов
    order_numbers = set()

    # Перебираем все элементы в текущей директории
    for item in current_dir.iterdir():
        # Проверяем, что это директория
        if item.is_dir():
            # Получаем имя директории
            dir_name = item.name

            # Проверяем, начинается ли имя с 3 цифр
            if len(dir_name) >= 3 and dir_name[:3].isdigit():
                order_numbers.add(dir_name[:11])

    return order_numbers


def create_maria_db_order_set():  # создаём множество заказов из MariaDB
    # Устанавливаем соединение с БД MySQL
    connection_mysql = None
    cursor_mysql = None
    try:
        connection_mysql = mysql.connector.connect(**config)
        # Создаем объект cursor, который позволяет нам выполнять SQL-запросы
        cursor_mysql = connection_mysql.cursor()
        # Выполняем SQL-запрос для получения названий всех таблиц
        cursor_mysql.execute("SHOW TABLES")
        # Получаем результаты и выводим их
        print("Названия всех таблиц в базе данных:")
        tables = cursor_mysql.fetchall()
        for (table_name,) in tables:
            print(table_name)
        cursor_mysql.execute("Select serial FROM task")
        all_orders = cursor_mysql.fetchall()
        order_set = set()
        year = get_current_year_from_parent_folder()
        for order in all_orders:
            if order[0][7:11] == year:
                order_set.add(order[0])
        return order_set

    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")
        return None

    finally:
        # Проверяем, был ли курсор инициализирован
        if cursor_mysql is not None:
            cursor_mysql.close()
        # Проверяем, было ли соединение установлено и открыто
        if connection_mysql is not None and connection_mysql.is_connected():
            connection_mysql.close()
            print("Соединение с базой данных MariaDB закрыто")


def create_order_folder(folder_name):
    """Создает папку для заказа и необходимые подпапки"""
    try:
        # Получаем директорию на уровень выше
        project_dir = Path(__file__).parent
        parent_dir = project_dir.parent

        # Создаем основную папку заказа
        order_dir = parent_dir / folder_name
        order_dir.mkdir(exist_ok=True)

        # Создаем стандартные подпапки (можете изменить список под ваши нужды)
        subfolders = ['Чеклисты', 'Фото и видео', 'ТЗ', 'Счета входящие', 'Схема', 'ПО', 'Паспорт', 'КП', 'Документы']
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


# Пример использования
if __name__ == "__main__":
    order_numbers_in_folder = get_order_numbers_in_folder()
    if order_numbers_in_folder:
        print(f"Найдены следующие номера заказов в папках: {sorted(order_numbers_in_folder)}")
    else:
        print(f"{RED}В текущей директории не найдены папки с номерами заказов.{RESET}")
    maria_db_order_set = create_maria_db_order_set()
    print('')
    print("множество заказов в maria_db:")
    print(maria_db_order_set)

    if maria_db_order_set is None:
        print(f"{RED}Ошибка получения данных из базы данных. Создание папок невозможно.{RESET}")
        exit(1)

    new_folder_names = maria_db_order_set - set(order_numbers_in_folder)
    if not new_folder_names:
        print(f"{GREEN}Все необходимые папки уже существуют.{RESET}")
        exit(0)
    print('')
    print("новые папки будут созданы с именами:")
    print(new_folder_names)

    # Счетчики для статистики
    created_count = 0
    failed_count = 0

    print(f"\nНачинаем создание папок...")
    for new_folder in new_folder_names:
        if create_order_folder(new_folder):
            created_count += 1
            print(f"{GREEN}Создана папка для заказа: {new_folder}{RESET}")
        else:
            failed_count += 1

    # Выводим итоговую статистику
    print(f"\nСоздание папок завершено:")
    print(f"Успешно создано: {GREEN}{created_count}{RESET}")
    if failed_count > 0:
        print(f"Не удалось создать: {RED}{failed_count}{RESET}")
    # print(get_current_year_from_parent_folder())
