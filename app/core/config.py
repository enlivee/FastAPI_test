from dataclasses import dataclass

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str
    cors_allowed_origins: list[str]

def get_settings():
    return Settings(
        DATABASE_URL="postgresql+psycopg://postgres:admin@127.0.0.1:15432/postgres",
        cors_allowed_origins = ["http://localhost:3000"]
    )


settings = get_settings()
engine = create_engine(settings.DATABASE_URL)
Sessionlocal = sessionmaker(bind=engine)


def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()
