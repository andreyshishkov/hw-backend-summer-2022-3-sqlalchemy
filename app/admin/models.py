from app.store.database.sqlalchemy_base import BaseModel
from app.web.utils import hash_password

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer


class AdminModel(BaseModel):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(120), index=True, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(256), nullable=False)

    def is_password_valid(self, password: str) -> bool:
        return self.password == hash_password(password)
