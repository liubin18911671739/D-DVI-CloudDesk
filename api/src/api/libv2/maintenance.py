

import logging
import os

from rethinkdb import RethinkDB

from api import app

from .flask_rethink import RDB

_MAINTENANCE_FILE_PATH = "/usr/local/etc/isardvdi/maintenance"


class _MaintenanceMetaClass:
    def __init__(self, *arg, **kwargs):
        self._enabled = False
        self._rethinkdb = RethinkDB()
        self._db = RDB(app)
        self._db.init_app(app)

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        with app.app_context():
            self._rethinkdb.table("config").get(1).update({"maintenance": enabled}).run(
                self._db.conn
            )
        self._enabled = enabled
        logging.info("Maintenance mode changed to %r.", enabled)

    def initialization(self):
        """Initialize maintenance mode. Check if maintenance file exists.
        If exists remove it and setting maintenance to true.
        If not exists get maintenance status form database"""
        if os.path.exists(_MAINTENANCE_FILE_PATH):
            logging.info(
                "Activating maintenance mode because the file %s is present.",
                _MAINTENANCE_FILE_PATH,
            )
            os.remove(_MAINTENANCE_FILE_PATH)
            self.enabled = True
        else:
            with app.app_context():
                self.enabled = (
                    self._rethinkdb.table("config")
                    .get(1)
                    .pluck("maintenance")
                    .run(self._db.conn)
                    .get("maintenance", False)
                )
            logging.info("Imported maintenance mode %r from database", self.enabled)


class Maintenance(metaclass=_MaintenanceMetaClass):
    """Control maintenance mode status"""
