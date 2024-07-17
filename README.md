# SimpleServerFastAPIAuth
# Простой сервер авторизации и аутентификации

## Описание тестового задания

### Разработка простого серверного приложения
1. Выбрать язык программирования (Python или JavaScript).
2. Реализовать базу данных (PostgreSQL или любую другую удобную систему).
3. Реализовать функции регистрации и аутентификации пользователей.
4. Реализовать обработку следующих типов запросов:
 - Получение списка пользователей.
 - Добавление нового пользователя.
 - Обновление информации о пользователе.
 - Удаление пользователя.
5. Обеспечить минимальную защиту приложения (например, защита от SQL-инъекций).

## Критерии оценки тестового задания:
- Чистота и качество кода.
- Правильность и логичность реализации функционала.
- Способность обеспечить базовую защиту данных.
- Документация кода и комментарии.

### Запуск на выполнение
Разрабатывалось в Python 3.12
Описание работ для PyCharm в Windows.

1. Создать и активировать виртуальное окружение.
python -m venv venv
.\venv\Scripts\activate

2. Установить зависимости проекта, указанные в файле requirements.txt
pip install -r requirements.txt 
или средствами PyCharm.

3. Проверить наличие установленного PostgreSQL и его настройки.
4. Создать файл .env на основе sample.env и прописать настройки.

5. Запустить можно стандартно, через скрипт или в PyCharm через "зеленую стрелку"
6. Работать с базой данных или просматривать документацию API можно:
localhost:8000/docs или
localhost:8000/redoc
