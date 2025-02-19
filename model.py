from sqlalchemy import Column, Integer, String, DateTime
from database import notice_Base

class Notice(notice_Base):
    __tablename__ = "notice"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    link = Column(String(500), nullable=False, unique=True)  
    pubDate = Column(DateTime, nullable=False, index=True)  
    author = Column(String(50), nullable=True, index=True)