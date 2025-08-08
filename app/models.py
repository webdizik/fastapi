import datetime

import config

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


engine = create_async_engine(config.PG_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    @property
    def _id(self):
        return {"id": self.id}


class Author(Base):

    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String, unique=True)


class Post(Base):

    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String, nullable=False, index=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[int] = mapped_column(Integer, nullable=True)
    id_authors = mapped_column(Integer, ForeignKey("authors.id"), nullable=False)
    creation_time: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        server_default=func.now()
        )

    @property
    def desc(self):
        return {
            "id": self.id,
            "title": self.title,
            "id_authors": self.id_authors,
            "creation_time": self.creation_time.strftime('%d.%m.%Y в %H:%M:%S'),
            }


async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def clear_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def close_orm():
    await engine.dispose()


ORM_OBJ = Post | Author
ORM_CLS = type[Post]
