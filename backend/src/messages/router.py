from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from backend.src.database import get_async_session
from backend.src.messages.models import message
from backend.src.messages.schemas import MessageCreate
from backend.src.auth.models import User
from backend.src.auth.config import current_verified_user


router = APIRouter(
    prefix="/msg",
    tags=["messages"],
)


@router.get("/{user_1_id}_{user_2_id}")
async def get_messages(
        user_1_id: int,
        user_2_id: int,
        user: User = Depends(current_verified_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    try:
        query = (select(message)
                 .where(
                    ((message.c.user_1 == user_1_id) & (message.c.user_2 == user_2_id)) |
                    ((message.c.user_1 == user_2_id) & (message.c.user_2 == user_1_id))
                )
                .where((message.c.user_1 == user.id) | (message.c.user_2 == user.id))
                )
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.mappings().all(),
            "details": None
        }
    except Exception as e:
        return {
            "status": "error",
            "data": None,
            "details": str(e)
        }


@router.post("/{user_1_id}_{user_2_id}")
async def create_message(
        user_1_id: int,
        user_2_id: int,
        text: str,
        user: User = Depends(current_verified_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    try:
        msg_create = MessageCreate(
            user_1=user_1_id,
            user_2=user_2_id,
            text=text,
            by=user.id,
            time=datetime.utcnow()
        )
        query = insert(message).values(msg_create.dict())
        await session.execute(query)
        await session.commit()
        return {
            "status": "success",
            "data": None,
            "details": None
        }
    except Exception as e:
        return {
            "status": "error",
            "data": None,
            "details": str(e)
        }


async def get_message_time(
        user_1_id: int,
        user_2_id: int,
        current_user_id: int,
        msg_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> datetime:
    query = (select(message.c.time)
             .where(
        ((message.c.user_1 == user_1_id) & (message.c.user_2 == user_2_id)) |
        ((message.c.user_1 == user_2_id) & (message.c.user_2 == user_1_id))
    )
             .where((message.c.user_1 == current_user_id) | (message.c.user_2 == current_user_id))
             .where(message.c.id == msg_id)
             )
    result = await session.execute(query)
    msg_time = result.scalar()
    return msg_time


@router.patch("/{user_1_id}_{user_2_id}")
async def update_message(
        user_1_id: int,
        user_2_id: int,
        msg_id: int,
        new_text: str,
        user: User = Depends(current_verified_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    try:
        msg_time = await get_message_time(user_1_id, user_2_id, user.id, msg_id, session)
        if datetime.utcnow() - timedelta(days=1) < msg_time:
            query = select(message).where(message.c.id == msg_id)
            result = await session.execute(query)
            message_data = dict(result.mappings().all()[0])
            message_data["text"] = new_text
            stmt = update(message).where(message.c.id == msg_id).values(message_data)
            await session.execute(stmt)
            await session.commit()
            return {
                "status": "success",
                "data": None,
                "details": None
            }
        else:
            return {
                "status": "error",
                "data": None,
                "details": "С момента отправки сообщения прошло больше суток"
            }

    except Exception as e:
        return {
            "status": "error",
            "data": None,
            "details": str(e)
        }


@router.delete("/{user_1_id}_{user_2_id}")
async def delete_message(
        user_1_id: int,
        user_2_id: int,
        msg_id: int,
        user: User = Depends(current_verified_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    try:
        msg_time = await get_message_time(user_1_id, user_2_id, user.id, msg_id, session)
        if datetime.utcnow() - timedelta(days=1) < msg_time:
            stmt = delete(message).where(message.c.id == msg_id)
            await session.execute(stmt)
            await session.commit()
            return {
                "status": "success",
                "data": None,
                "details": None
            }
        else:
            return {
                "status": "error",
                "data": None,
                "details": "С момента отправки сообщения прошло больше суток"
            }

    except Exception as e:
        return {
            "status": "error",
            "data": None,
            "details": str(e)
        }
