from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from .contact_service import ContactService


def get_contact_service(db: AsyncSession = Depends(get_db)) -> ContactService:
    return ContactService(db)
