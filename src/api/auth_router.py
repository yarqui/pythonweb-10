from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.schemas import UserCreate, UserResponse, TokenResponse
from src.services import get_user_service, UserService, AuthService
from src.services import get_auth_service

auth_router = APIRouter(prefix="/auth", tags=["authentication"])


@auth_router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
async def signup(
    body: UserCreate, user_service: UserService = Depends(get_user_service)
):
    """
    Handles user registration. The service layer contains all business logic,
    including checking for existing users. The router just calls the service.
    """
    new_user = await user_service.create_user(body)
    return new_user


@auth_router.post("/login", response_model=TokenResponse, summary="User Login")
async def login(
    body: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
    db: AsyncSession = Depends(get_db),
):
    return await auth_service.login_user(body, db)
