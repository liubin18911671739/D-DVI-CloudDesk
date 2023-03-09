

from rethinkdb import r

from .db import rethink


@rethink
def get_storage_pool(connection, storage_pool_id):
    return r.table("storage_pool").get(storage_pool_id).run(connection)
