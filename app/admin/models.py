from app.store.database.sqlalchemy_base import BaseModel
from app.web.utils import hash_password

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
import bcrypt


class AdminModel(BaseModel):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, index=True, unique=True, nullable=False)
    password: Mapped[str]

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.password.encode())

    def set_password(self, password: str) -> None:
        self.password = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt(),
        ).decode()
