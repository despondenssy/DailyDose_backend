# DailyDose Backend

API для управления приёмом лекарств.  

## Возможности:
- Регистрация и аутентификация пользователей
- Управление лекарствами (добавление, изменение, удаление)
- Управление курсами приёма лекарств
- JWT авторизация
- Защита API и привязка данных к конкретному пользователю

## Стек технологий:
- Python 3.12
- Django 5.2
- Django REST Framework
- SimpleJWT
- SQLite (для разработки)

## Установка:
1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/despondenssy/DailyDose_backend.git
    cd DailyDose_backend  # Переход в папку проекта
    ```

2. Создайте и активируйте виртуальное окружение:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Linux/MacOS
    venv\Scripts\activate     # Для Windows
    ```

3. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```


Теперь проект доступен по адресу: `http://127.0.0.1:8000/`.