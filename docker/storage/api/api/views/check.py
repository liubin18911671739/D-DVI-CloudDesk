

import json

from api import app


@app.route("/toolbox/api/check", methods=["GET"])
def check():
    return (
        json.dumps({}),
        200,
        {"Content-Type": "application/json"},
    )
