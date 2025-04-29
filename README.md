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
```bash
git clone https://github.com/despondenssy/DailyDose_backend.git
cd DailyDose_backend  # Переход в папку проекта
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt