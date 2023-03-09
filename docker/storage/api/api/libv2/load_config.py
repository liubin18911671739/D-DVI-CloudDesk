

import os
import time
import traceback

from api import app

from .._common.api_rest import ApiRest


def wait_for_api(app):
    api_rest = ApiRest("isard-api")
    app.logger.info("Check connection to api")
    api_conection = False
    while not api_conection:
        try:
            api_rest.get("")
            api_conection = True
        except:
            app.logger.debug(traceback.format_exc())
            time.sleep(1)


def setup_app(app):
    try:
        app.config.setdefault("LOG_LEVEL", os.environ.get("LOG_LEVEL", "INFO"))
        app.config.setdefault("LOG_FILE", "isard-toolbox.log")
        app.debug = True if os.environ["LOG_LEVEL"] == "DEBUG" else False

    except:
        app.logger.error(traceback.format_exc())
        app.logger.error("Missing parameters!")
        return False
    app.logger.info("Initial configuration loaded...")
    return True
