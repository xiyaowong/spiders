from flask import Flask, request

import funcs
from web import response


def home():
    data = ":)"
    return response(data=data)


def extract():
    if "url" not in request.values:
        return response(400, msg="Missing parameter.")
    url = request.values["url"]
    return funcs.extract(url)


def init_app(app: Flask):
    app.add_url_rule("/", "home", home)
    app.add_url_rule("/extract/", "extract", extract)
