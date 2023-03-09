

import traceback

from api import app

from .._common.api_exceptions import Error


def _validate_item(item, data, normalize=True):
    if not app.validators[item].validate(data):
        raise Error(
            "bad_request",
            "Data validation for "
            + item
            + " failed: "
            + str(app.validators[item].errors),
            traceback.format_exc(),
        )
    if normalize:
        return app.validators[item].normalized(data)
    return data
