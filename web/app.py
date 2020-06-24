import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.getcwd())))

from flask import Flask
from flask_cors import CORS

from web import config, error, views, log



def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)
    CORS(app)

    views.init_app(app)
    error.init_app(app)
    log.init_app(app)

    if app.config["ENV"] == "development":
        print(app.url_map)

    return app


app = create_app()

if __name__ == "__main__":
    app.run()
