from fastapi import HTTPException

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import ORM_CLS, ORM_OBJ


async def add_item(session: AsyncSession, item: ORM_OBJ):

    session.add(item)

    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(409, f"{ORM_OBJ.__name__} already exists")


async def get_item_by_id(session: AsyncSession, orm_cls: ORM_CLS, item_id: int):

    orm_obj = await session.get(orm_cls, item_id)

    if orm_obj is None:
        raise HTTPException(
            404,
            f"{orm_cls.__name__} with id {item_id} not found"
        )

    return orm_obj


async def delete_item_by_id(session: AsyncSession, orm_cls: ORM_CLS, item_id: int):

    orm_obj = await session.delete(orm_cls, item_id)

    if orm_obj is None:
        raise HTTPException(
            404,
            f"{orm_cls.__name__} with id {item_id} not found"
        )
    else:
        await session.commit()
