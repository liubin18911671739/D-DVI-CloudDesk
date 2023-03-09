

import json
from time import time

from cachetools import TTLCache, cached
from rethinkdb import r

from api import app

from .. import socketio
from .flask_rethink import RDB


class StorageNode:
    """
    Manage Storage Node.

    Use constructor with keyboard arguments to create new Storage Node or
    update an existing one using id keyboard. Use constructor with id as
    first argument to create an object representing an existing Storage
    Node.
    """

    _rdb = RDB(app)

    def __init__(self, *args, **kwargs):
        if args:
            kwargs["id"] = args[0]
        self.__dict__["id"] = kwargs["id"]
        with app.app_context():
            r.table("storage_node").insert(kwargs, conflict="update").run(
                self._rdb.conn
            )
        socketio.emit(
            "storage_nodes",
            json.dumps(kwargs),
            namespace="/administrators",
            room="admins",
        )

    @cached(TTLCache(maxsize=10, ttl=5))
    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        with app.app_context():
            return (
                r.table("storage_node")
                .get(self.id)
                .pluck(name)
                .run(self._rdb.conn)
                .get(name)
            )

    def __setattr__(self, name, value):
        if name == "id":
            raise AttributeError
        else:
            updated_data = {name: value}
            if name == "status":
                updated_data["status_time"] = time()
            with app.app_context():
                r.table("storage_node").get(self.id).update(updated_data).run(
                    self._rdb.conn
                )
            updated_data["id"] = self.id
            socketio.emit(
                "storage_nodes",
                json.dumps(updated_data),
                namespace="/administrators",
                room="admins",
            )
