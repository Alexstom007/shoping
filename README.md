Тестовое задание отдел бэкенд Сарафан

1.	print_sequence.py - программа на 1 задание .

2.	Django проект магазина продуктов:

## Технологии
Python, Django, DRF, sqllite

## Запуск проекта локально:
Клонировать репозиторий:
```
git clone git@github.com:Alexstom007/shoping.git
```
В директории shoping создать и активировать виртуальное окружение:
```
python -m venv venv
Linux/macOS: source env/bin/activate
windows: source venv/Scripts/activate
```
Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
```
В директории shoping создать и заполнить файл .env:
```
touch .env

SECRET_KEY='Секретный ключ'
```
Выполнить миграции:
```
cd backend && python manage.py migrate
```
Создать суперпользователя:
```
python manage.py createsuperuser
```
Запустить проект:
```
python manage.py runserver
```

## Выполнил
[Александр Вотинов](https://github.com/Alexstom007)
