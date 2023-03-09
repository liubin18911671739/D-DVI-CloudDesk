

import json
import logging as log
import traceback

from flask import request

from api import app

from .._common.api_exceptions import Error
from ..libv2.api_storage_physical import (
    phy_storage_delete,
    phy_storage_list,
    phy_storage_reset_domains,
    phy_storage_reset_media,
    phy_storage_update,
    phy_storage_upgrade_to_storage,
    phy_toolbox_host,
)
from ..libv2.helpers import get_user_data
from .decorators import is_admin, ownsStorageId


@app.route("/api/v3/admin/storage/physical/<table>", methods=["GET"])
@is_admin
def api_v3_admin_get_storage_physical(payload, table):
    if table not in ["domains", "media"]:
        raise Error("bad_request", "Table should be domains or media")
    return (
        json.dumps(phy_storage_list(table)),
        200,
        {"Content-Type": "application/json"},
    )


@app.route("/api/v3/admin/storage/physical/<table>", methods=["PUT"])
@is_admin
def api_v3_admin_put_storage_physical(payload, table):
    data = request.get_json()
    # validate item
    phy_storage_update(table, [data])
    return (
        json.dumps({}),
        200,
        {"Content-Type": "application/json"},
    )


@app.route("/api/v3/admin/storage/physical/init/<table>", methods=["PUT"])
@is_admin
def api_v3_admin_init_storage_physical(payload, table):
    data = request.get_json()
    # validate item
    if table == "domains":
        phy_storage_reset_domains(data)
    if table == "media":
        phy_storage_reset_media(data)
    return (
        json.dumps({}),
        200,
        {"Content-Type": "application/json"},
    )


@app.route("/api/v3/admin/storage/physical/<table>/<path_id>", methods=["DELETE"])
@is_admin
def api_v3_admin_delete_storage_physical(payload, table, path_id):
    phy_storage_delete(table, path_id)
    return (
        json.dumps({}),
        200,
        {"Content-Type": "application/json"},
    )


@app.route(
    "/api/v3/admin/storage/physical/multiple_actions/<action_id>", methods=["POST"]
)
@is_admin
def api_v3_admin_storage_physical_multiple_actions(payload, action_id):
    data = request.get_json()

    if action_id == "upgrade_to_storage":
        result = phy_storage_upgrade_to_storage(data, payload["user_id"])
    else:
        raise Error("bad_request", "Action does not exist.")
    return (
        json.dumps(result),
        200,
        {"Content-Type": "application/json"},
    )


@app.route("/api/v3/admin/storage/physical/toolbox_host", methods=["GET"])
@is_admin
def api_v3_admin_storage_physical_host(payload):
    return (
        json.dumps(phy_toolbox_host()),
        200,
        {"Content-Type": "application/json"},
    )
