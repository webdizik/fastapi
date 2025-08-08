from pydantic import BaseModel
from typing import Literal

import datetime


class SuccessResponse(BaseModel):

    status: Literal["success"]

# Models requests
class CreatePostRequest(BaseModel):
    title: str
    description: str | None
    id_authors: int
    price: int
    creation_time: datetime.datetime


class UpdatePostRequest(BaseModel):
    title: str | None
    description: str | None
    price: int | None

# Models responses
class CreatePostResponse(SuccessResponse):
    pass


class UpdatePostResponse(SuccessResponse):
    pass


class GetPostResponse(BaseModel):
    id: int
    title: str
    description: str
    id_authors: int
    price: int
    creation_time: datetime.datetime


class SearchPostResponse(BaseModel):
    results: list[GetPostResponse]


class DeletePostResponse(SuccessResponse):
    pass
