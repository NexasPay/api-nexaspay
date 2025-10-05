from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine
from app import database_url
from sqlalchemy.orm import sessionmaker
from typing import Annotated

# connect_args = {"check_same_thread": False}
engine = create_engine(database_url, echo=False)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine)

SessionDep = Annotated[Session, Depends(get_session)]