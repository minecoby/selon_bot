from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from variable import *


SQLALCHEMY_DATABASE_URL_USER = f"mysql+mysqlconnector://root:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{NOTICE_DB_NAME}?charset=utf8mb4&collation=utf8mb4_unicode_ci"

notice_engine = create_engine(SQLALCHEMY_DATABASE_URL_USER)

notice_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=notice_engine)

notice_Base = declarative_base()

def get_noticedb():
    db = notice_SessionLocal()
    try:
        yield db
    finally:
        db.close()