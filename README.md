# Flask-ToDo-List
ToDo List сделанный на Flask, с использованием Flask Migrate (тот же Alembic), так же с Flask JWT и Docker compose.

Что реализовано:
1. Каждому конкретному пользователю доступны только его задачи.
2. Эндпонт /api/tasks с всеми его методами только после аутентификации. Выдаётся ошибка 401, если нет доступа.
3. Используется PostgreSQL.
4. Используется SQLAlchemy.
5. Миграции реализованы с помощью Flask Migrate - основан на Alembic.
6. PostgreSQL в докер контейнере. Данные находятся вне контейнера.
Не реализовано:
1. Механизм сидирования базы данных.