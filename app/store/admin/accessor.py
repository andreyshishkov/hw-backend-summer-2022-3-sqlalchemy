from typing import TYPE_CHECKING
from sqlalchemy import select
from app.admin.models import AdminModel
from app.base.base_accessor import BaseAccessor
from app.web.utils import hash_password

if TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application") -> None:
        admin = await self.get_by_email(app.config.admin.email)
        if admin is None:
            await self.create_admin(
                email=app.config.admin.email,
                password=app.config.admin.password
            )

    async def get_by_email(self, email: str) -> AdminModel | None:
        query = select(AdminModel).where(AdminModel.email == email)

        async with self.app.database.session() as session:
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def create_admin(self, email: str, password: str) -> AdminModel:
        new_admin = AdminModel(
            email=email,
            password=hash_password(password)
        )

        async with self.app.database.session() as session:
            session.add(new_admin)
            await session.commit()
            await session.refresh(new_admin)

        return new_admin
