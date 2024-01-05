from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Optional
from config import DB_HOST, DB_USER, DB_PORT, DB_NAME, DB_PASSWORD

db_con = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(db_con)

SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Base.metadata.create_all(bind=engine)

DATABASE_URL: Optional[str] = None
SECRET_KEY: Optional[str] = "cairocoders"


def sess_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()
