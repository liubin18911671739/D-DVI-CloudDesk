

import traceback
from functools import wraps

from ..auth.tokens import Error, get_header_jwt_payload
from ..lib.exceptions import Error


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
            traceback.format_stack(),
        )

    return decorated
