from typing import TYPE_CHECKING, Any

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker, create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.engine.url import URL

from app.store.database import BaseModel

if TYPE_CHECKING:
    from app.web.app import Application


class Database:
    def __init__(self, app: "Application") -> None:
        self.app = app

        self.engine: AsyncEngine | None = None
        self._db: type[DeclarativeBase] = BaseModel
        self.session: async_sessionmaker[AsyncSession] | None = None

    async def connect(self, *args: Any, **kwargs: Any) -> None:
        self.engine = create_async_engine(
            URL.create(
                'postgresql+asyncpg',
                self.app.config.database.user,
                self.app.config.database.password,
                self.app.config.database.host,
                self.app.config.database.port,
                self.app.config.database.database
            ),
            echo=True,
            future=True,
            pool_pre_ping=True,
        )
        self.session = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            class_=AsyncSession,
            autoflush=False,
            autocommit=False,
        )

        async with self.engine.begin() as conn:
            await conn.run_sync(self._db.metadata.create_all)

    async def disconnect(self, *args: Any, **kwargs: Any) -> None:
        if self.engine:
            await self.engine.dispose()
