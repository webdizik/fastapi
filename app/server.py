from fastapi import FastAPI

import datetime

from constants import SUCCESS_RESPONSE
from schema import (CreatePostRequest, UpdatePostRequest, CreatePostResponse,
                    UpdatePostResponse, GetPostResponse, SearchPostResponse,
                    DeletePostResponse)
from lifespan import lifespan
from dependancy import SessionDependency
from models import Post
from crud import add_item, get_item_by_id, delete_item_by_id

from sqlalchemy import select


app = FastAPI(
    title='Bay and sell',
    description='Site for buying/selling ads',
    lifespan=lifespan,
)

@app.post("/api/v1/advertisement", response_model=CreatePostResponse,
          tags=["Advertisement"])
async def create_post(post: CreatePostRequest, session: SessionDependency):

    post_dict = post.model_dump(exclude_unset=True)

    post_orm_obj = Post(**post_dict)

    await add_item(session, post_orm_obj)

    return post_orm_obj._id


@app.get("/api/v1/advertisement/{advertisement_id}", response_model=GetPostResponse,
         tags=["Advertisement"])
async def get_post(advertisement_id: int, session: SessionDependency):

    post_orm_obj = await get_item_by_id(session, Post, advertisement_id)

    return post_orm_obj.desc


@app.get("/api/v1/advertisement?{query_string}", response_model=SearchPostResponse,
         tags=["Advertisement"])
async def search_post(session: SessionDependency,
                      title: str = None,
                      description: str = None,
                      price: int = None,
                      creation_time: datetime.datetime = None
                      ):

    query = (
        select(Post)
        .where(
            Post.title == title,
            Post.description == description,
            Post.price == price,
            Post.creation_time == creation_time
            )
        .limit(10000)
        )

    found_posts = await session.scalars(query)

    return {"results": [post.desc for post in found_posts]}


@app.patch("/api/v1/advertisement/{advertisement_id}",
           response_model=UpdatePostResponse, tags=["Advertisement"])
async def update_post(session: SessionDependency,
                      advertisement_id: int, post_data: UpdatePostRequest):

    post_dict = post_data.model_dump(exclude_unset=True)

    post_orm_obj = await get_item_by_id(session, Post, advertisement_id)

    for field, value in post_dict.items():
        setattr(post_orm_obj, field, value)

    return SUCCESS_RESPONSE


@app.delete("/api/v1/advertisement/{advertisement_id}",
            response_model=DeletePostResponse, tags=["Advertisement"])
async def delete_post(session: SessionDependency, advertisement_id: int):

    post_orm_obj = await get_item_by_id(session, Post, advertisement_id)

    await delete_item_by_id(session, post_orm_obj)

    return SUCCESS_RESPONSE
