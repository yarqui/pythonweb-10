import datetime
from typing import List


from sqlalchemy import select, extract, or_, tuple_
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact
from src.schemas import ContactBase, ContactUpdate


class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def create_contact(
        self,
        body: ContactBase,
    ) -> Contact:
        contact = Contact(**body.model_dump())
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def search_contacts(
        self,
        skip: int,
        limit: int,
        first_name: str | None,
        last_name: str | None,
        email: str | None,
    ) -> List[Contact]:

        stmt = select(Contact)
        filters = []
        if first_name:
            filters.append(Contact.first_name.ilike(f"%{first_name}%"))
        if last_name:
            filters.append(Contact.last_name.ilike(f"%{last_name}%"))
        if email:
            filters.append(Contact.email.ilike(f"%{email}%"))

        if filters:
            stmt = stmt.where(or_(*filters))

        stmt = stmt.offset(skip).limit(limit)
        result = await self.db.execute(stmt)

        return result.scalars().all()

    async def get_contact_by_id(self, contact_id: int) -> Contact | None:
        stmt = select(Contact).where(Contact.id == contact_id)
        contact = await self.db.execute(stmt)
        return contact.scalar_one_or_none()

    async def update_contact(
        self, contact_id: int, body: ContactUpdate
    ) -> Contact | None:

        contact = await self.get_contact_by_id(contact_id)
        if contact:
            update_data = body.model_dump(exclude_unset=True)

            for key, value in update_data.items():
                setattr(contact, key, value)

            await self.db.commit()
            await self.db.refresh(contact)

        return contact

    async def delete_contact(self, contact_id: int) -> Contact | None:
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def get_upcoming_birthdays(self) -> List[Contact]:
        today = datetime.date.today()

        target_dates = [today + datetime.timedelta(days=i) for i in range(7)]
        birthday_tuples = [(d.month, d.day) for d in target_dates]

        stmt = select(Contact).where(
            tuple_(
                extract("month", Contact.birthday), extract("day", Contact.birthday)
            ).in_(birthday_tuples)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
