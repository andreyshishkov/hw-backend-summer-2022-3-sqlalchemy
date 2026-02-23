from aiohttp_apispec import request_schema, response_schema
from aiohttp.web_exceptions import HTTPForbidden, HTTPUnauthorized
from aiohttp_session import new_session, get_session

from app.admin.schemes import AdminSchema
from app.web.app import View
from app.web.utils import json_response


class AdminLoginView(View):
    @request_schema(AdminSchema)
    @response_schema(AdminSchema, 200)
    async def post(self):
        data = self.data
        email = data["email"]
        password = data["password"]

        admin = await self.store.admins.get_by_email(email)
        if not admin or not admin.is_password_valid(password):
            raise HTTPForbidden(reason="Invalid email or password")

        admin_data = AdminSchema().dump(admin)
        session = await new_session(self.request)
        session["admin"] = admin_data
        return json_response(data=admin_data)


class AdminCurrentView(View):
    @response_schema(AdminSchema, 200)
    async def get(self):
        session = await get_session(self.request)
        admin_data = session.get("admin")

        if not admin_data:
            raise HTTPUnauthorized(reason="unauthorized")
        return json_response(data=admin_data)
