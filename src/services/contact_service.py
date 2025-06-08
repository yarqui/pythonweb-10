from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository import ContactRepository
from src.schemas import ContactBase, ContactUpdate
from src.database.models import Contact


class ContactService:
    def __init__(self, db: AsyncSession):
        self._contact_repository = ContactRepository(db)

    async def create_contact(self, body: ContactBase) -> Contact:
        new_contact = await self._contact_repository.create_contact(body)
        return new_contact

    async def search_contacts(
        self,
        skip: int,
        limit: int,
        first_name: str | None,
        last_name: str | None,
        email: str | None,
    ) -> List[Contact]:
        contacts = await self._contact_repository.search_contacts(
            skip, limit, first_name, last_name, email
        )
        return contacts

    async def get_contact_by_id(self, contact_id: int) -> Contact | None:
        contact = await self._contact_repository.get_contact_by_id(contact_id)
        return contact

    async def update_contact(
        self, contact_id: int, body: ContactUpdate
    ) -> Contact | None:
        updated_contact = await self._contact_repository.update_contact(
            contact_id, body
        )
        return updated_contact

    async def delete_contact(self, contact_id: int) -> Contact | None:
        deleted_contact = await self._contact_repository.delete_contact(contact_id)
        return deleted_contact

    async def get_upcoming_birthdays(self) -> List[Contact]:
        contacts = await self._contact_repository.get_upcoming_birthdays()
        return contacts
