from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):

    async def get_donation_by_user(
            self,
            user: User,
            session: AsyncSession,
    ) -> List[Donation]:
        db_donation = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        db_donation = db_donation.scalars().all()
        return db_donation


donation_crud = CRUDDonation(Donation)
