from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import CharityProject, Donation


async def get_unallocated_donations_and_open_projects(
        session: AsyncSession,
):
    projects = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested is not True
        )
    )
    donations = await session.execute(
        select(Donation).where(
            Donation.fully_invested is not True
        )
    )
    return projects.scalars().all(), donations.scalars().all()


def distribution_of_donations_for_projects(
        projects: CharityProject,
        donations: Donation
):
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
                project.fully_invested = True
                project.close_date = datetime.now()
            if donation.invested_amount == donation.full_amount:
                donation.fully_invested = True
                donation.close_date = datetime.now()
                break


async def investment_process(
        session: AsyncSession,
):
    projects, donations = (
        await get_unallocated_donations_and_open_projects(
            session
        )
    )
    if projects and donations:
        distribution_of_donations_for_projects(
            projects, donations
        )
    await session.commit()
    return projects
