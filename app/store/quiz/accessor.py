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
        query = select(ThemeModel).where(ThemeModel.id == id_)
        async with self.app.database.session() as session:
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def list_themes(self) -> Sequence[ThemeModel]:
        stmt = select(ThemeModel)
        async with self.app.database.session() as session:
            result =  await session.scalars(stmt)
            return result.all()

    async def create_question(
        self, title: str, theme_id: int, answers: Iterable[AnswerModel]
    ) -> QuestionModel:
        question = QuestionModel(
            title=title,
            theme_id=theme_id,
            answers=answers,
        )
        async with self.app.database.session() as session:
            session.add(question)
            await session.commit()
            await session.refresh(question, ['answers'])
            return question

    async def get_question_by_title(self, title: str) -> QuestionModel | None:
        stmt = select(QuestionModel).where(QuestionModel.title == title)
        async with self.app.database.session() as session:
            return await session.scalar(stmt)

    async def list_questions(
        self, theme_id: int | None = None
    ) -> Sequence[QuestionModel]:
        query = select(QuestionModel).options(
            joinedload(QuestionModel.answers)
        )
        if theme_id is not None:
            query = query.where(QuestionModel.theme_id == theme_id)

        async with self.app.database.session() as session:
            result = await session.scalars(query)
            return result.unique().all()
