from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, Session


DATABASE_URL = "postgresql+psycopg://postgres:admin@127.0.0.1:15432/postgres"
engine = create_engine(DATABASE_URL)
Sessionlocal = sessionmaker(bind=engine)



class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))

class TaskORM(Base):
    __tablename__ = "tasks"

    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    print("Запуск приложения")
    yield
    print("Завершение приложения")


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
)



class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool

class TaskCreateSchema(BaseModel):
    title: str

class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None



class CategorySchema(BaseModel):
    id: str
    name: str

class CategoryCreateSchema(BaseModel):
    name: str

class CategoryUpdateSchema(BaseModel):
    name: str | None = None

tasks: list[TaskSchema] = []
categories: list[CategorySchema] = []

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

def task_orm_to_schema(task_orm: TaskORM) -> TaskSchema:
    return TaskSchema(id=task_orm.id, title=task_orm.title, completed=task_orm.completed)

@app.get("/tasks")
def read_tasks(db: Session = Depends(get_db)) -> list[TaskSchema]:
   tasks_from_db = db.scalars(select(TaskORM)).all()
   return [task_orm_to_schema(task_orm) for task_orm in tasks_from_db]

@app.post("/tasks")
def create_task(payload: TaskCreateSchema, status_code=status.HTTP_201_CREATED, db: Session = Depends(get_db)) -> TaskSchema:
    new_task = TaskSchema(id=str(uuid4()), title=payload.title, completed=False)
    tasks.append(new_task)

    return new_task

@app.patch("/tasks/{task_id}")
def update_task(task_id: str, payload: TaskUpdateSchema, db: Session = Depends(get_db)):
    for task in tasks:
        if task.id == task_id:
            if payload.title: 
                task.title = payload.title
            if payload.completed is not None: 
                task.completed = payload.completed

            return task
        
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id, db: Session = Depends(get_db)):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)

@app.get("/categories")
def read_categories(db: Session = Depends(get_db)):
    return categories

@app.post("/categories")
def create_category(payload: CategoryCreateSchema, status_code=status.HTTP_201_CREATED, db: Session = Depends(get_db)) -> CategorySchema:
    new_category = CategorySchema(id=str(uuid4()), name=payload.name)
    categories.append(new_category)

    return new_category

@app.patch("/categories/{category_id}")
def update_category(category_id: str, payload: CategoryCreateSchema, db: Session = Depends(get_db)):
    for category in categories:
        if category.id == category_id:
            if payload.name:
                category.name = payload.name
            return category

@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id, db: Session = Depends(get_db)):
    for category in categories:
        if category.id == category_id:
            categories.remove(category)
