from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine
from app import database_url

engine = create_engine(database_url, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine)

SessionDep = Depends(get_session)