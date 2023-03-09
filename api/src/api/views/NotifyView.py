

import json

from flask import request

from api import app

from .._common.api_exceptions import Error
from ..libv2.api_notify import notify_desktop, notify_user
from .decorators import is_admin


@app.route("/api/v3/admin/notify/user/desktop", methods=["POST"])
@is_admin
def user_notify(payload):
    data = request.get_json()
    notify_user(
        data["user_id"],
        data["type"],
        data.get("msg_code"),
        data.get("params"),
    )
    return json.dumps({}), 200, {"Content-Type": "application/json"}


@app.route("/api/v3/admin/notify/desktop", methods=["POST"])
@is_admin
def desktop_notify(payload):
    data = request.get_json()
    notify_desktop(
        data["desktop_id"],
        data["type"],
        data.get("msg_code"),
        data.get("params"),
    )
    return json.dumps({}), 200, {"Content-Type": "application/json"}
