from dotenv import load_dotenv
import os
from pathlib import Path

# pip install python-dotenv

# Цветовые коды ANSI
GREEN = '\033[92m'  # Зеленый цвет
RED = '\033[91m'  # Красный цвет
RESET = '\033[0m'  # Сброс цвета


def load_config():
    # Получаем абсолютный путь к директории скрипта
    base_dir = Path(__file__).parent
    env_path = base_dir / '.env'

    # Проверяем существование файла .env
    print(f"1. Проверка наличия файла .env:")
    print(f"   Путь к файлу: {env_path}")
    print(f"   Файл существует: {env_path.exists()}")

    if env_path.exists():
        print(f"\n2. Содержимое файла .env:")
        with open(env_path, 'r') as f:
            print("   " + "\n   ".join(f.readlines()))

    # Загружаем переменные и проверяем результат
    print(f"\n3. Загрузка переменных окружения:")
    success = load_dotenv(env_path)
    print(f"   load_dotenv вернул: {success}")

    # Получаем значения переменных
    config = {
        'password': os.getenv('PASSWORD'),
        'host': os.getenv('HOST'),
        'database': os.getenv('NAME'),
        'port': os.getenv('PORT')
    }

    # Проверяем значения переменных
    print(f"\n4. Проверка значений переменных:")
    variables = ['PASSWORD', 'HOST', 'NAME', 'PORT']
    for var in variables:
        value = os.getenv(var)
        if value is None:
            print(f"   {var}: {RED}Не задана{RESET}")
        masked_value = '*' * len(value) if value and var == 'PASSWORD' else value
        print(f"   {var}: {masked_value}")

    return config


# Пример использования
if __name__ == "__main__":
    try:
        db_config = load_config()
        print(f"{GREEN}Конфигурация БД успешно загружена{RESET}")
    except Exception as e:
        print(f"{RED}Ошибка при загрузке конфигурации БД: {e}{RESET}")
