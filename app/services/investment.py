from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def investment_process(model, objects_not_invest):
    balance = model.full_amount
    for i in objects_not_invest:
        need_invest = i.full_amount - i.invested_amount
        investing = min(balance, need_invest)
        i.invested_amount += investing
        model.invested_amount += investing
        balance -= investing
        if i.full_amount == i.invested_amount:
            i.fully_invested = True
            i.close_date = datetime.now()
        if balance == 0:
            model.fully_invested = True
            model.close_date = datetime.now()
            break


async def investing_in_project(
    model: CharityProject,
    session: AsyncSession
):
    donations_not_invest = await session.execute(
        select(Donation).where(
            Donation.fully_invested == False # noqa
        )
    )
    donations_not_invest = donations_not_invest.scalars().all()
    await investment_process(model, donations_not_invest)
    await session.commit()
    await session.refresh(model)
    return model


async def investing_from_donation(
    model: Donation,
    session: AsyncSession
):
    projects_not_invest = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested == False # noqa
        )
    )
    projects_not_invest = projects_not_invest.scalars().all()
    await investment_process(model, projects_not_invest)
    await session.commit()
    await session.refresh(model)
    return model
