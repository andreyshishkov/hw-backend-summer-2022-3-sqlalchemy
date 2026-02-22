from aiohttp.web import json_response as aiohttp_json_response
from aiohttp.web_response import Response
import hashlib


def json_response(data: dict | None = None, status: str = "ok") -> Response:
    return aiohttp_json_response(
        data={
            "status": status,
            "data": data or {},
        }
    )


def error_json_response(
    http_status: int,
    status: str = "error",
    message: str | None = None,
    data: dict | None = None,
):
    return aiohttp_json_response(
        status=http_status,
        data={
            "status": status,
            "message": str(message),
            "data": data or {},
        },
    )


def hash_password(password: str) -> str:
    """Хеширует пароль с использованием SHA-256."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()