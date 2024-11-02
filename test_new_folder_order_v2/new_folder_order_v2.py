from pathlib import Path
from db_config import load_config
import mysql.connector
# Цветовые коды ANSI
GREEN = '\033[92m'  # Зеленый цвет
RED = '\033[91m'  # Красный цвет
RESET = '\033[0m'  # Сброс цвета


# Загружаем конфигурацию
config = load_config()

# Используем значения
password = config['password']
host = config['host']
database = config['database']
port = config['port']


# def create_maria_db_company_dict():  # создаём множество компаний из MariaDB
#     # Устанавливаем соединение с БД MySQL
#     connection_mysql = None
#     cursor_mysql = None
#
#     try:
#         connection_mysql = mysql.connector.connect(**config)
#         # Создаем объект cursor, который позволяет нам выполнять SQL-запросы
#         cursor_mysql = connection_mysql.cursor()
#         # Выполняем SQL-запрос для получения названий всех таблиц
#         # cursor.execute("SHOW TABLES")
#         # Получаем результаты и выводим их
#         # print("Названия всех таблиц в базе данных:")
#         # tables = cursor.fetchall()
#         # for (table_name,) in tables:
#         #     print(table_name)
#
#         cursor_mysql.execute("Select id, name FROM client")
#         clients = cursor_mysql.fetchall()
#         for client in clients:
#             maria_db_company_dict[client[0]] = client[1]
#
#     except mysql.connector.Error as err:
#         print(f"Ошибка: {err}")
#
#     finally:
#         # Проверяем, был ли курсор инициализирован
#         if cursor_mysql is not None:
#             cursor_mysql.close()
#
#         # Проверяем, было ли соединение установлено и открыто
#         if connection_mysql is not None and connection_mysql.is_connected():
#             connection_mysql.close()
#             print("Соединение с базой данных MariaDB закрыто")

def get_order_numbers_in_folder():
    # Получаем текущую директорию, где находится скрипт
    current_dir = Path(__file__).parent

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
                order_numbers.add(int(dir_name[:3]))

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
    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")


# Пример использования
if __name__ == "__main__":
    order_numbers_in_folder = get_order_numbers_in_folder()
    if order_numbers_in_folder:
        print(f"Найдены следующие номера заказов в папках: {sorted(order_numbers_in_folder)}")
    else:
        print(f"{RED}В текущей директории не найдены папки с номерами заказов.{RESET}")
    create_maria_db_order_set()
