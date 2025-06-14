from fastapi import APIRouter, Depends, Request

from src.schemas import UserResponse
from src.database.models import User

from src.services.auth_service import get_current_user
from src.services import limiter

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get(
    "/me", response_model=UserResponse, summary="Get Current User's Profile"
)
@limiter.limit("5/minute")
async def get_own_profile(
    request: Request, current_user: User = Depends(get_current_user)
):
    return current_user
