from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationUserDB
from app.services.investment import investing_from_donation

router = APIRouter()


@router.post(
    '/',
    response_model=DonationUserDB,
    response_model_exclude_none=True,
)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    donation = await donation_crud.create(
        donation, session, user
    )
    await investing_from_donation(donation, session)
    return donation


@router.get(
    '/',
    response_model=List[DonationDB],
    dependencies=[Depends(current_superuser)]
)
async def get_all_donation(
        session: AsyncSession = Depends(get_async_session)
):
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=List[DonationUserDB],
)
async def get_user_donation(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_donation_by_user(user, session)
