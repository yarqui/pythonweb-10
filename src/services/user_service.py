from __future__ import annotations
import logging

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from asyncpg.exceptions import UniqueViolationError

from libgravatar import Gravatar

from src.repository import UserRepository
from src.services import AuthService
from src.schemas import UserCreate
from src.database.models import User

logger = logging.getLogger(__name__)

__all__ = ["UserService"]


class UserService:
    def __init__(self, db: AsyncSession):
        self._repository = UserRepository(db)
        self._auth_service = AuthService()

    async def create_user(self, body: UserCreate) -> User:
        existing_user = await self._repository.get_user_by_email(body.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists.",
            )
        hashed_password = self._auth_service.hash_password(body.password)

        avatar_url = None
        try:
            g = Gravatar(body.email)
            avatar_url = g.get_image()
        except Exception as e:
            logger.warning("Could not retrieve Gravatar for %s: %s", body.email, e)

        try:
            return await self._repository.create_user(body, hashed_password, avatar_url)
        except IntegrityError as e:
            # Needed for race condition
            if isinstance(e.orig, UniqueViolationError):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User with this email already exists (race condition).",
                ) from e
            raise

    async def get_user_by_id(self, user_id: int) -> User | None:
        user = await self._repository.get_user_by_id(user_id)
        return user

    async def get_user_by_username(self, username: str) -> User | None:
        user = await self._repository.get_user_by_username(username)
        return user

    async def get_user_by_email(self, email: str) -> User | None:
        user = await self._repository.get_user_by_email(email)
        return user
