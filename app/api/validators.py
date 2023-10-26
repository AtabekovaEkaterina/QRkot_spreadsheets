from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        charity_project_id, session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект не найден!'
        )
    return charity_project


async def check_name_unique(
        charity_project_name: str,
        session: AsyncSession
) -> None:
    charity_project = await charity_project_crud.get_charity_project_id_by_name(
        charity_project_name,
        session
    )
    if charity_project is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )


async def check_invested_amount_before_update_project(
        charity_project_id: int,
        session: AsyncSession,
        full_amount_to_update: int
) -> None:
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!',
        )
    if charity_project.invested_amount > full_amount_to_update:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Сумма проекта не может быть меньше внесённой!'
        )


def check_invested_amount_before_deleting_project(
        charity_project: CharityProject
) -> None:
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
