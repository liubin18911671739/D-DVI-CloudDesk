

import json

from api import app

from .. import socketio


def notify_user(user_id, type, msg_code, params={}):
    data = {
        "type": type,
        "msg_code": msg_code,
        "params": params,
    }
    socketio.emit(
        "msg",
        json.dumps(data),
        namespace="/userspace",
        room=user_id,
    )


def notify_desktop(desktop_id, type, msg_code, params={}):
    data = {
        "type": type,
        "msg_code": msg_code,
        "params": params,
    }
    socketio.emit(
        "msg",
        json.dumps(data),
        namespace="/userspace",
        room=desktop_id,
    )
