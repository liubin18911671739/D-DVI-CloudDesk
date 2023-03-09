

from gevent import monkey

monkey.patch_all()

import os

from flask import Flask

from scheduler import app, socketio

debug = os.environ.get("USAGE", "production") == "devel"

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=debug, log_output=debug)
