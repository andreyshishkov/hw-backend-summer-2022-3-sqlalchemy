from app.store.database.sqlalchemy_base import BaseModel

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Boolean
from typing import List


class ThemeModel(BaseModel):
    __tablename__ = "themes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    questions: Mapped[List["QuestionModel"]] = relationship(
        back_populates="theme", cascade="all, delete-orphan"
    )


class QuestionModel(BaseModel):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    theme_id: Mapped[int] = mapped_column(ForeignKey("themes.id", ondelete="CASCADE"), nullable=False)
    theme: Mapped["ThemeModel"] = relationship(back_populates="questions")
    answers: Mapped[List["AnswerModel"]] = relationship(
        back_populates="question", cascade="all, delete-orphan"
    )


class AnswerModel(BaseModel):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)

    question: Mapped["QuestionModel"] = relationship(back_populates="answers")
