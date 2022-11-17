from datetime import datetime
from typing import Optional

from pydantic import BaseModel, NonNegativeInt, PositiveInt


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]


class DonationCreate(DonationBase):
    pass


class DonationUserDB(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationBase):
    id: int
    create_date: datetime
    user_id: int
    invested_amount: NonNegativeInt
    fully_invested: bool

    class Config:
        orm_mode = True
