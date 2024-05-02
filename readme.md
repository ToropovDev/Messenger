## Start up
### 1. Create DB and role
#### 1.1 - install psql 

#### 1.2 - create DB
```sql
CREATE DATABASE {имя БД};
```
#### 1.3 - create role
```sql
CREATE USER {пользователь} WITH PASSWORD {пароль};
```
#### 1.4 - grant privileges
```sql
GRANT ALL PRIVILEGES ON DATABASE {имя БД} TO {пользователь};
```
#### 1.4 - add data to .env file. Template .env:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME={имя БД}
DB_USER={пользователь}
DB_PASS={пароль}
```
#### Не создавать таблицы через psql - для этого есть миграции alembic.
### 2. Python backend
#### 2.1 - После создания виртуального окружения установить зависимости
```
pip install -r requirements.txt
```
#### 2.2 - установить redis, запустить
#### 2.3 - добавить в .env поля:
``` 
JWT_SECRET={любой секретный токен}
USER_MANAGER_SECRET={любой секретный токен}

SMTP_HOST={например, smtp.yandex.ru}
SMTP_PORT={для яндекса 465}
SMTP_USER={почтовый адрес}
SMTP_PASS={пароль приложения}

CELERY_BROKER_URL={по умолчанию - redis://localhost:6379}
```
#### 2.4 - запустить celery
``` 
celery -A backend.src.auth.manager:celery_app worker --loglevel=INFO --pool=solo
```
#### 2.5 - запустить апу
``` 
uvicorn backend.src.app:app --reload 
```