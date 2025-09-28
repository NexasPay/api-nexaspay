from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models import User
from pydantic import BaseModel
import datetime
from jose import jwt
from app import secret_key
router = APIRouter()

class UserCreate(BaseModel):
    email: str
    sub: str

def create_access_token(data: dict, expires_minutes=30):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm="HS256")

@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = User(email=user.email, sub=user.sub)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    token = create_access_token({"sub": new_user.sub})
    return {"user_id": new_user.id, "token": token}
