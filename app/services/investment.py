from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import CharityProject, Donation


async def investment_process(
        session: AsyncSession,
):
    """Логика распределения инвестиций."""
    open_projects = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested == bool(False)
        )
    )
    projects = open_projects.scalars().all()

    undistributed_donations = await session.execute(
        select(Donation).where(
            Donation.fully_invested == bool(False)
        )
    )
    donations = undistributed_donations.scalars().all()

    if projects and donations:
        for donation in donations:
            for project in projects:

                investments_before_project_closure = (
                    project.full_amount - project.invested_amount
                )
                donation_balance_amount = (
                    donation.full_amount - donation.invested_amount
                )
                if donation_balance_amount < investments_before_project_closure:
                    project.invested_amount = (
                        project.invested_amount + donation_balance_amount
                    )
                    donation.invested_amount = (
                        donation.invested_amount + donation_balance_amount
                    )
                if donation_balance_amount >= investments_before_project_closure:
                    project.invested_amount = project.full_amount
                    donation.invested_amount = (
                        donation.invested_amount + investments_before_project_closure
                    )
                    project.fully_invested = bool(True)
                    project.close_date = datetime.now()
                if donation.invested_amount == donation.full_amount:
                    donation.fully_invested = bool(True)
                    donation.close_date = datetime.now()
                    break
    await session.commit()
    return projects
