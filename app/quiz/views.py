from aiohttp_apispec import querystring_schema, request_schema, response_schema
from aiohttp.web_exceptions import HTTPConflict, HTTPBadRequest, HTTPNotFound

from app.quiz.schemes import (
    ListQuestionSchema,
    QuestionSchema,
    ThemeIdSchema,
    ThemeListSchema,
    ThemeSchema,
)
from app.quiz.models import AnswerModel
from app.web.app import View
from app.web.utils import json_response


class ThemeAddView(View):
    @request_schema(ThemeSchema)
    @response_schema(ThemeSchema)
    async def post(self):
        title = self.data["title"]
        existing_theme = await self.store.quizzes.get_theme_by_title(title)
        if existing_theme:
            raise HTTPConflict(reason="Theme with this title already exists")
        theme = await self.store.quizzes.create_theme(title=title)
        return json_response(data=ThemeSchema().dump(theme))

class ThemeListView(View):
    @response_schema(ThemeListSchema)
    async def get(self):
        themes = await self.store.quizzes.list_themes()
        return json_response(data=ThemeListSchema().dump({"themes": themes}))


class QuestionAddView(View):
    @request_schema(QuestionSchema)
    @response_schema(QuestionSchema)
    async def post(self):
        data = self.data
        title = data["title"]
        theme_id = data["theme_id"]
        answers_raw = data["answers"]

        theme = await self.store.quizzes.get_theme_by_id(theme_id)
        if not theme:
            raise HTTPNotFound(reason="Theme not found")

        existing_question = await self.store.quizzes.get_question_by_title(title)
        if existing_question:
            raise HTTPConflict(reason="Question with this title already exists")

        correct_count = sum(1 for a in answers_raw if a["is_correct"])
        if correct_count == 0:
            raise HTTPBadRequest(reason="Question must have at least one correct answer")
        if len(answers_raw) < 2:
            raise HTTPBadRequest(reason="Question must have at least two answers")
        if correct_count == len(answers_raw):
            raise HTTPBadRequest(reason="Question must have at least one incorrect answer")

        answers = [
            AnswerModel(title=a["title"], is_correct=a["is_correct"])
            for a in answers_raw
        ]
        question = await self.store.quizzes.create_question(
            title=title,
            theme_id=theme_id,
            answers=answers
        )

        return json_response(data=QuestionSchema().dump(question))

class QuestionListView(View):
    @querystring_schema(ThemeIdSchema)
    @response_schema(ListQuestionSchema)
    async def get(self):
        theme_id = self.data.get("theme_id")
        questions = await self.store.quizzes.list_questions(theme_id=theme_id)
        return json_response(data=ListQuestionSchema().dump({"questions": questions}))
