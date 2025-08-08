from typing import Annotated

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from models import Session


async def get_session():

    async with Session() as session:

        yield session


SessionDependency = Annotated[AsyncSession, Depends(get_session)]