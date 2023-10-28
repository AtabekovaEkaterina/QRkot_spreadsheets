from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.services.investment import investment_process
from app.schemas.donation import (
    DonationAllDB, DonationCreate, DonationDB
)

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationAllDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    return await donation_crud.get_multi(session)


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_new_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Для всех пользователей."""
    new_donation = await donation_crud.create(donation, session, user)
    await investment_process(session)
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    response_model_exclude={'user_id'},
)
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Получает список всех пожертвований текущего пользователя."""
    return await donation_crud.get_by_user(
        session=session, user=user
    )
