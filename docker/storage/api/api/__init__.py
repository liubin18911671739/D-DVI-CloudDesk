

import os
from importlib.machinery import SourceFileLoader
from logging.config import dictConfig

from flask import Flask
from flask_cors import CORS

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "%(asctime)s.%(msecs)03d, %(levelname)s, %(message)s",
                "datefmt": "%Y-%m-%dT%H:%M:%S",
            },
        },
        "handlers": {
            "stdout": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            }
        },
        "root": {"handlers": ["stdout"], "level": os.getenv("LOG_LEVEL", "INFO")},
    }
)

app = Flask(__name__, static_url_path="")
CORS(app)
app.url_map.strict_slashes = False

# Max upload size
app.config["MAX_CONTENT_LENGTH"] = 1 * 1000 * 1000  # 1 MB

print("Starting toolbox api...")

app.ram = {
    "secrets": {
        "isardvdi": {
            "id": "isardvdi",
            "secret": os.environ["API_ISARDVDI_SECRET"],
            "description": "isardvdi",
            "domain": "localhost",
            "category_id": "default",
            "role_id": "admin",
        }
    }
}

from api._common.api_rest import ApiRest
from api.libv2.load_config import setup_app

ApiRest().wait_for()

if not setup_app(app):
    app.logger.error("Unable to initialize app config. Exitting.")
    exit(0)

from api.libv2.load_validator_schemas import load_validators

app.validators = load_validators()

"""'
Import all views
"""
from .views import StorageView, check
