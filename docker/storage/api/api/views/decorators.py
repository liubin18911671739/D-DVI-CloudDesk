

import traceback
from functools import wraps

from flask import abort, request

from api import app

from .._common.api_exceptions import Error
from ..auth.tokens import Error, get_auto_register_jwt_payload, get_header_jwt_payload


def has_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        payload = get_header_jwt_payload()
        if payload.get("role_id") != "admin":
            maintenance()
        kwargs["payload"] = payload
        return f(*args, **kwargs)

    return decorated


def is_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        payload = get_header_jwt_payload()
        if payload["role_id"] == "admin":
            kwargs["payload"] = payload
            return f(*args, **kwargs)
        raise Error(
            "forbidden",
            "Not enough rights.",
            traceback.format_exc(),
            description_code="forbidden",
        )

    return decorated


def is_admin_or_manager(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        payload = get_header_jwt_payload()
        if payload.get("role_id") != "admin":
            maintenance()
        if payload["role_id"] == "admin" or payload["role_id"] == "manager":
            kwargs["payload"] = payload
            return f(*args, **kwargs)
        raise Error(
            "forbidden",
            "Not enough rights.",
            traceback.format_exc(),
        )

    return decorated
