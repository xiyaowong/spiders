import time

from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def response(status_code=200, data=None, message=None):
    if data == None and status_code == 200:
        status_code = 204

    pay_load = {
        "code": status_code,
        "message": message or HTTP_STATUS_CODES.get(status_code, "unknown code"),
        "data": data,
        "timestamp": int(time.time())
    }
    _response = jsonify(pay_load)
    _response.status_code = status_code
    return _response