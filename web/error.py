# pylint: disable=unused-argument
from flask import Flask

from . import response


def init_app(app: Flask):
    @app.errorhandler(400)
    def _error_400(e):
        return response(400)

    @app.errorhandler(500)
    def _error_500(e):
        return response(500)

    @app.errorhandler(404)
    def _error_404(e):
        return response(404)

    @app.errorhandler(405)
    def _error_404(e):
        return response(405)
