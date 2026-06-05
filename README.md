# Todo App Backend

Backend для todo-приложения на FastAPI.

Реализованы CRUD-роуты для:

- задач (`/tasks`)
- категорий (`/categories`)

## Стек

- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- PostgreSQL
- Docker Compose

## Запуск проекта

### 1. Активировать виртуальное окружение

```bash
source venv/bin/activate
```

### 2. Запустить PostgreSQL

```bash
docker compose up -d
```

PostgreSQL запускается на порту `15432`.

Данные сохраняются в Docker volume `postgres_data`, поэтому они не пропадут после остановки контейнера.

### 3. Запустить backend

```bash
uvicorn app.main:app --reload --port 8080
```

API будет доступен по адресу:

```text
http://127.0.0.1:8080
```

Swagger-документация:

```text
http://127.0.0.1:8080/docs
```

## Роуты

### Tasks

```text
GET    /tasks
POST   /tasks
PATCH  /tasks/{task_id}
DELETE /tasks/{task_id}
```

### Categories

```text
GET    /categories
POST   /categories
PATCH  /categories/{category_id}
DELETE /categories/{category_id}
```

## База данных

Строка подключения находится в `app/core/config.py`:

```text
postgresql+psycopg://postgres:admin@127.0.0.1:15432/postgres
```

Настройки Docker Compose:

- database: `postgres`
- user: `postgres`
- password: `admin`
- host: `127.0.0.1`
- port: `15432`

