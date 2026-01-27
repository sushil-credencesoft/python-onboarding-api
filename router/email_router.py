from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from database import get_db
from models.subscriber import Subscriber

email_router = APIRouter(prefix="/subscribe", tags=["Subscribe"])

class SubscribeRequest(BaseModel):
    email: EmailStr

@email_router.post("/")
def save_email(data: SubscribeRequest, db: Session = Depends(get_db)):
    existing = db.query(Subscriber).filter(Subscriber.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already subscribed")

    sub = Subscriber(email=data.email)
    db.add(sub)
    db.commit()

    return {"message": "Email saved successfully"}
