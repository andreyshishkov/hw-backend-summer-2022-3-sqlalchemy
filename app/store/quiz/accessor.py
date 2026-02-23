from collections.abc import Iterable, Sequence
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.base.base_accessor import BaseAccessor
from app.quiz.models import (
    AnswerModel,
    QuestionModel,
    ThemeModel,
)


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> ThemeModel:
        new_theme = ThemeModel(title=title)
        async with self.app.database.session() as session:
            session.add(new_theme)
            await session.commit()
            await session.refresh(new_theme)
        return new_theme

    async def get_theme_by_title(self, title: str) -> ThemeModel | None:
        query = select(ThemeModel).where(ThemeModel.title == title)
        async with self.app.database.session() as session:
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_theme_by_id(self, id_: int) -> ThemeModel | None:
        raise NotImplementedError

    async def list_themes(self) -> Sequence[ThemeModel]:
        raise NotImplementedError

    async def create_question(
        self, title: str, theme_id: int, answers: Iterable[AnswerModel]
    ) -> QuestionModel:
        raise NotImplementedError

    async def get_question_by_title(self, title: str) -> QuestionModel | None:
        raise NotImplementedError

    async def list_questions(
        self, theme_id: int | None = None
    ) -> Sequence[QuestionModel]:
        raise NotImplementedError
