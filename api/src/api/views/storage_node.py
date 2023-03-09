

import json
import traceback

import requests
from flask import request

from api import app

from .._common.api_exceptions import Error
from ..libv2.storage_node import StorageNode
from .decorators import is_hyper


@app.route("/api/v3/storage_node", methods=["POST", "PUT", "DELETE"])
@is_hyper
def manage_storage_node():
    """
    Manage Storage Node.

    Input data must be JSON.
    """
    if not request.is_json:
        raise Error(description="JSON expected")
    storage_node = StorageNode(**request.json)
    if request.method == "DELETE":
        storage_node.status = "deleted"
        return (
            json.dumps(storage_node.id),
            200,
            {"Content-Type": "application/json"},
        )
    else:
        try:
            requests.get(
                storage_node.id, verify=storage_node.verify_cert
            ).status_code == 200
            storage_node.status = "online"
            return (
                json.dumps(storage_node.id),
                200,
                {"Content-Type": "application/json"},
            )
        except:
            storage_node.status = "error"
            raise Error(
                "bad_request",
                "Unable to connect to storage node at " + str(storage_node.id),
                traceback.format_exc(),
            )
