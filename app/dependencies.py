# from https://fastapi.tiangolo.com/tutorial/bigger-applications/?h=file%20structure#path-operations-with-apirouter
# We see that we are going to need some dependencies used in several places of the application.
# So we put them in their own dependencies module (app/dependencies.py).
# We will now use a simple dependency to read a custom X-Token header:


from typing import Annotated
from fastapi import Header, HTTPException, Depends
from app import secret_key
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import init_db
    

async def getDbData() -> AsyncSession: 
    return await Depends(init_db) 