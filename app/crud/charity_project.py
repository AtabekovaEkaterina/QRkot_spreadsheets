from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_charity_project_id_by_name(
            self,
            charity_project_name: str,
            session: AsyncSession
    ) -> Optional[CharityProject]:
        charity_project = await session.execute(
            select(self.model).where(
                self.model.name == charity_project_name
            )
        )
        return charity_project.scalars().first()

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession
    ) -> list[CharityProject]:
        sort_closed_projects = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested
            ).order_by(
                func.strftime(
                    '%s', CharityProject.close_date
                ) - func.strftime(
                    '%s', CharityProject.create_date
                )
            )
        )
        return sort_closed_projects.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)
