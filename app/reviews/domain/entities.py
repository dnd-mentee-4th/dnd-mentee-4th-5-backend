from typing import ClassVar

from pydantic import BaseModel, Field

from reviews.domain.value_objects import ReviewRating, UserId, ReviewId, DrinkId


class Review(BaseModel):
    MIN_COMMENT_LEN: ClassVar[int] = 0
    MAX_COMMENT_LEN: ClassVar[int] = 300
    id: ReviewId
    drink_id: DrinkId
    user_id: UserId
    rating: ReviewRating
    comment: str = Field(min_length=MIN_COMMENT_LEN, max_length=MAX_COMMENT_LEN)
    created_at: float
    updated_at: float
