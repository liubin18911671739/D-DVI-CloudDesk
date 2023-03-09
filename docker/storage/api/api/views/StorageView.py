

import json

from flask import request

from api import app

from .._common.api_exceptions import Error
from ..libv2.api_storage import Storage

# from ..libv2.api_storage_file import StorageFile
from .decorators import is_admin

api_storage = Storage()


@app.route("/toolbox/api/storage/disk/info", methods=["POST"])
@is_admin
def storage_disk_info(payload):
    data = request.get_json(force=True)
    return (
        json.dumps(api_storage.get_file_info(data["path_id"])),
        200,
        {"Content-Type": "application/json"},
    )


@app.route("/toolbox/api/storage/disks", methods=["PUT"])
@is_admin
def storage_disk_update(payload):
    return (
        json.dumps(api_storage.update_disks()),
        200,
        {"Content-Type": "application/json"},
    )


@app.route("/toolbox/api/storage/media", methods=["PUT"])
@is_admin
def storage_media_update(payload):
    return (
        json.dumps(api_storage.update_media()),
        200,
        {"Content-Type": "application/json"},
    )


# @app.route("/toolbox/api/storage/disks", methods=["GET"])
# @is_admin
# def storage_list(payload=None):
#     return (
#         json.dumps(api_storage.get_disks()),
#         200,
#         {"Content-Type": "application/json"},
# )


# @app.route("/toolbox/api/file/<item>/<uuid>", methods=["GET"])
# # @has_token
# def file_info(item, uuid):
#     if item == "size":
#         return (
#             json.dumps(StorageFile(uuid).size()),
#             200,
#             {"Content-Type": "application/json"},
#         )
#     if item == "chain":
#         return (
#             json.dumps(StorageFile(uuid).chain()),
#             200,
#             {"Content-Type": "application/json"},
#         )
#     if item == "disks":
#         return (
#             json.dumps(StorageFile(uuid).disks()),
#             200,
#             {"Content-Type": "application/json"},
#         )


# @app.route("/toolbox/api/file", methods=["POST"])
# @app.route("/toolbox/api/file/<from_backing>", methods=["POST"])
# @has_token
# def file_new(payload, from_backing=None):
#     data = request.get_json(force=True)
#     if from_backing == "from_backing":
#         data = _validate_item("new_file_from_backing", data)
#         uuid = StorageFile(uuid).create(
#             data.get("format", "qcow2"), data["backing_file"]
#         )
#     else:
#         data = _validate_item("new_file", data)
#         uuid = StorageFile(uuid).create(data.get("format", "qcow2"), data["size"])
#     return json.dumps(uuid), 200, {"Content-Type": "application/json"}
