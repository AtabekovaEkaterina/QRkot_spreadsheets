from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_exists,
    check_invested_amount_before_deleting_project,
    check_invested_amount_before_update_project,
    check_name_unique,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.services.investment import investment_process
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charityprojects(
        session: AsyncSession = Depends(get_async_session),
):
    """Для всех пользователей."""
    all_charityprojects = await charity_project_crud.get_multi(session)
    return all_charityprojects


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charityproject(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    await check_name_unique(
        charity_project_name=charity_project.name,
        session=session
    )
    new_charity_project = await charity_project_crud.create(
        charity_project, session
    )
    await investment_process(session)
    await session.refresh(new_charity_project)
    return new_charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        project_id: int,
        object_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    if object_in.full_amount is not None:
        await check_invested_amount_before_update_project(
            project_id, session, object_in.full_amount
        )
    if object_in.name is not None:
        await check_name_unique(
            object_in.name, session
        )
    charity_project = await charity_project_crud.update(
        charity_project, object_in, session
    )
    await investment_process(session)
    await session.refresh(charity_project)
    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    check_invested_amount_before_deleting_project(charity_project)
    remote_charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return remote_charity_project
