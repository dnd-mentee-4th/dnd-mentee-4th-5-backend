from enum import Enum
from typing import ClassVar

from pydantic import BaseModel, Field


class ReviewRating(BaseModel):
    MIN_VALUE: ClassVar[int] = 0
    MAX_VALUE: ClassVar[int] = 5
    __root__: int = Field(alias="value", ge=MIN_VALUE, le=MAX_VALUE)

    def __int__(self):
        return self.__root__


class OrderType(Enum):
    LIKE_DESC = "like_desc"
    LIKE_ASC = "like_asc"
    NEWEST = "newest"


class UserId(BaseModel):
    __root__: str = Field(alias="value", min_length=1, max_length=30)

    def __str__(self):
        return self.__root__
