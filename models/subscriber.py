from sqlalchemy import Column, Integer, String, DateTime, func
from database import Base

class Subscriber(Base):
    __tablename__ = "website_subscribers"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
