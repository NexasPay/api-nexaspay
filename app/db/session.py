from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine
from app import database_url
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import Annotated

engine = create_async_engine(database_url, echo=True)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def _get_async_session():
    async with async_session() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

AsyncSessionDep = Annotated[AsyncSession, Depends(_get_async_session)]