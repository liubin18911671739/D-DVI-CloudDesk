

import csv
import io
import pathlib
import traceback
from pathlib import Path

from api import app

from .._common.api_exceptions import Error
from ..libv2.storage.isard_qcow import IsardStorageQcow


class StorageFile:
    def __init__(self, file_uuid):
        path = list(Path("/isard").rglob(file_uuid))
        import logging as log

        log.info(file_uuid)
        log.info(path)
        if not len(path):
            raise Error("not_found", "File not found", traceback.format_exc())
        self.file_path = str(path[0])
        # self.format = "qcow" if self.file_path.endswith(".qcow2") else "unknown"
        # self.format = "iso" if self.file_path.endswith(".iso") else "unknown"
        self.storage = IsardStorageQcow()
        # self.storage = IsardStorageIso() if self.format == "iso"
        # Init populate storage thread

    def size(self):
        return self.storage.get_file_size(self.file_path)

    def chain(self):
        return self.storage.get_file_chain(self.file_path)

    def disks(self):
        return self.storage.get_file_disks(self.file_path)
