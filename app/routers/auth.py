from fastapi import APIRouter
from app.dependencies import getDbData
from pydantic import BaseModel
import datetime
from app.db.session import AsyncSessionDep
from jose import jwt
from app import secret_key
from app.models.user_model import User


router = APIRouter()

# Only for test
@router.get("/auth/{user_id}")
async def authUser(user_id: int, session: AsyncSessionDep):
    return "Confirmed!"

# class UserCreate(BaseModel):
#     email: str
#     sub: str

# def create_access_token(data: dict, expires_minutes=30):
#     to_encode = data.copy()
#     expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_minutes)
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, secret_key, algorithm="HS256")

# @router.post("/register")
# async def register(user: UserCreate):
#     db = await getDbData()
#     new_user = User(email=user.email, sub=user.sub)
#     db.add(new_user)
#     await db.commit()
#     await db.refresh(new_user)
#     token = create_access_token({"sub": new_user.sub})
#     return {"user_id": new_user.id, "token": token}
