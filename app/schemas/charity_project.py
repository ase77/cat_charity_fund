from datetime import datetime
from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from pydantic import (BaseModel, Extra, Field, NonNegativeInt, PositiveInt,
                      validator)


class CharityProjectBase(BaseModel):
    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: NonNegativeInt
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectBase):

    @validator('name', 'description', 'full_amount')
    def fields_cannot_be_null(cls, value):
        if value == '' or value is None:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail='Обязательные поля не могут быть пустыми!',
            )
        return value
