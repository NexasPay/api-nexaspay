from datetime import datetime, timedelta, timezone
from jose import jwt
from jose.exceptions import JWTError
from fastapi import Form, Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlmodel import select, Session
from pydantic import BaseModel, EmailStr
from typing import Annotated
from app.db.session import get_session  
from app.models.user_model import Users
from app.internal.AuthUser import encryptPassword, checkPassword
from os import getenv
from pydantic import BaseModel, Field

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = getenv("SECRET_KEY", "dev-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Não foi possível validar as credenciais",
    headers={"WWW-Authenticate": "Bearer"},
)

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginData(BaseModel):
    email: Annotated[str, Form(alias="Email")]
    password: Annotated[
            str,
            Form(alias="Senha", json_schema_extra={"format": "password"})
        ]

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_user_by_email(email: str, session: Session):
    statement = select(Users).where(Users.email == email)
    return session.exec(statement).first()

def authenticate_user(email: str, password: str, session: Session) -> Users:
    user: Users = get_user_by_email(email, session)
    if not (user or checkPassword(password, user.password)): 
        raise HTTPException(status_code=401, detail=f"Acesso inválido. Usuário ou senha incorretos")
    return user

def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = session.exec(select(Users).where(Users.user_id == user_id)).first()
    if user is None:
        raise credentials_exception

    return user


class userLoginForm(BaseModel):
    email: str = Field(alias="Email")
    password: str = Field(alias='Senha')

@router.post("/token", response_model=Token, name="Verifique login do usuário")
async def login_for_access_token(
    form_data: Annotated[userLoginForm, Form()],
    session: Session = Depends(get_session)
):
    user = authenticate_user(form_data.email, form_data.password, session)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.user_id)}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/", name="Verique seu login atual")
async def read_users_me(current_user: Annotated[Users, Depends(get_current_user)]):
    return current_user