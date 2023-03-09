

import json

from flask import request

from api import app

from ..libv2.maintenance import Maintenance
from .decorators import is_admin


@app.route("/api/v3/maintenance", methods=["GET"])
def _api_maintenance_get():
    return (
        json.dumps(Maintenance.enabled),
        200,
        {"Content-Type": "application/json"},
    )


@app.route("/api/v3/maintenance", methods=["PUT"])
@is_admin
def _api_maintenance_put(payload):
    Maintenance.enabled = request.get_json()
    return (
        json.dumps(Maintenance.enabled),
        200,
        {"Content-Type": "application/json"},
    )
