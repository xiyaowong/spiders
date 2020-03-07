from flask import Flask
from flask_cors import CORS

from . import config


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)
    CORS(app)

    from . import views
    views.init_app(app)

    from . import error
    error.init_app(app)

    return app


app = create_app()
if __name__ == "__main__":
    app.run()
    print(app.url_map)