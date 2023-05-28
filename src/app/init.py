from flask import Flask

from routes import init_routes


def create_app(test_config=None):

    app = Flask(__name__)

    app.config["SECRET_KEY"] = "sw@rdfi$h"
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@pgsql:5432/db"

    init_routes(app)

    return app
