# DailyDose Backend

API для управления приёмом лекарств.

## Стек технологий:
- Python 3.12
- Django 5.2
- Django REST Framework
- SimpleJWT
- SQLite (для разработки)

## Установка:
открываем в проводнике папку, в которую хотим склонить гит, вводим cmd. В пути не должно быть русских символов.

в открывшемся терминале вводим команду
```bash
git clone https://github.com/KlyushovaPolina/DailyDose_backend.git
```
появившуюся папку DailyDose_backend открываем в вашей IDE 

Далее работаем в терминале в проекте:

Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Для Linux/MacOS
venv\Scripts\activate     # Для Windows
   ```

Установите зависимости:
```bash
pip install -r requirements.txt
   ```

Примените миграции: (после этого создается база данных)
```bash
python manage.py migrate
   ```

Запустите сервер:
```bash
python manage.py runserver
   ```