from typing import List
from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError

from src.schemas import ContactUpdate, ContactBase, ContactResponse
from src.services import ContactService, get_contact_service

contact_router = APIRouter(prefix="/contacts", tags=["contacts"])


@contact_router.get("/", response_model=List[ContactResponse])
async def search_contacts(
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
    skip: int = 0,
    limit: int = Query(default=10, ge=1, le=100),
    contact_service: ContactService = Depends(get_contact_service),
):
    contacts = await contact_service.search_contacts(
        first_name, last_name, email, skip, limit
    )
    return contacts


@contact_router.get(
    "/birthdays",
    response_model=List[ContactResponse],
    summary="Get upcoming birthdays",
)
async def get_upcoming_birthdays(
    contact_service: ContactService = Depends(get_contact_service),
):
    contacts = await contact_service.get_upcoming_birthdays()
    return contacts


@contact_router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact_by_id(
    contact_id: int, contact_service: ContactService = Depends(get_contact_service)
):
    contact = await contact_service.get_contact_by_id(contact_id)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@contact_router.post(
    "/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED
)
async def create_contact(
    body: ContactBase,
    contact_service: ContactService = Depends(get_contact_service),
):
    try:
        new_contact = await contact_service.create_contact(body)
        return new_contact

    # Unique constraint violation
    except IntegrityError as e:
        if isinstance(e.orig, UniqueViolationError):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Contact with email '{body.email}' already exists.",
            ) from e

        # Other unexpected database errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected database error occurred.",
        ) from e


@contact_router.patch("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: int,
    body: ContactUpdate,
    contact_service: ContactService = Depends(get_contact_service),
):
    contact = await contact_service.update_contact(contact_id, body)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@contact_router.delete("/{contact_id}", response_model=ContactResponse)
async def delete_contact(
    contact_id: int, contact_service: ContactService = Depends(get_contact_service)
):
    contact = await contact_service.delete_contact(contact_id)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact
