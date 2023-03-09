

# from subprocess import check_output
import hashlib
import json
import os
from pathlib import Path

from api import app

from .._common.api_exceptions import Error
from .._common.api_rest import ApiRest
from ..libv2.storage.isard_qcow import IsardStorageQcow


def ff(path_id):
    # file_format = check_output(
    #     ("file", "-F", "','", path_id), text=True
    # ).strip().split(",")[1]
    # if "QCOW" in file_format:
    #     return "qcow2"
    return "qcow2"


class Storage:
    def __init__(self):
        app.logger.info("Instantiating storage")
        self.storage = {"qcow2": IsardStorageQcow()}
        self.init_api()

    def init_api(self):
        flavour = os.environ.get("FLAVOUR", False)
        if str(flavour) == "all-in-one" or not flavour:
            self.hostname = "isard-hypervisor"
        else:
            self.hostname = os.environ.get("DOMAIN")
        api_domain = os.environ.get("API_DOMAIN", False)
        if api_domain and api_domain != "isard-api":
            self.api_rest = ApiRest("isard-api")

        self.templates_path = "/isard/templates"
        self.desktops_path = "/isard/groups"
        self.media_path = "/isard/media"

    def get_file_info(self, path_id):
        try:
            return self.storage[ff(path_id)].get_file_info(path_id)
        except:
            raise Error("not_found", "File " + str(path_id) + " not found in system.")

    def update_disks(self, add_qemu_img_info=True):
        qcows = []
        total = list(Path("/isard").rglob("**/*.qcow2"))
        for p in total:
            if p.is_file():
                try:
                    disk_with_backing = self.storage[ff(str(p))].get_file_info(
                        str(p), backing_chain=True
                    )
                except:
                    qcows.append(
                        {
                            "id": hashlib.md5(str(p).encode("utf-8")).hexdigest(),
                            "path": str(p),
                            "parents": None,
                            "correct-chain": False,
                            "hyper": self.hostname,
                            "size": p.stat().st_size,
                            "qemu-img-info": self.storage[ff(str(p))].get_file_info(
                                str(p)
                            ),
                        }
                    )
                    continue
                qcows.append(
                    {
                        "id": hashlib.md5(str(p).encode("utf-8")).hexdigest(),
                        "path": str(p),
                        "parents": [
                            p["full-backing-filename"]
                            for p in disk_with_backing
                            if p.get("full-backing-filename")
                        ],
                        "correct-chain": True,
                        "hyper": self.hostname,
                        "size": p.stat().st_size,
                        "qemu-img-info": disk_with_backing[0],
                    }
                )
                app.logger.info(
                    "Reading info for disk " + str(len(qcows)) + "/" + str(len(total))
                )
        self.api_rest.put(
            "/admin/storage/physical/init/domains",
            qcows,
        )
        return len(qcows)

    def update_media(self):
        self.media_files = [
            {
                "id": hashlib.md5(str(p).encode("utf-8")).hexdigest(),
                "path": str(p),
                "hyper": self.hostname,
                "kind": "media",
                "size": p.stat().st_size,
            }
            for p in Path(self.media_path).rglob("*")
            if p.is_file()
        ]
        self.api_rest.put(
            "/admin/storage/physical/init/media",
            self.media_files,
        )
        app.logger.info("- updated media to api")
        return {
            "media": len(self.media_files),
        }
