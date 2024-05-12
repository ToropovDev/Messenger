from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.dialects.postgresql import UUID

from backend.src.auth.config import auth_backend
from backend.src.auth.models import User
from backend.src.auth.schemas import UserRead, UserCreate, UserUpdate
from backend.src.auth.manager import get_user_manager

from backend.src.messages.router import router as messages_router

app = FastAPI(
    title="Мессенджер",
    version="0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # can alter with time
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(messages_router)
