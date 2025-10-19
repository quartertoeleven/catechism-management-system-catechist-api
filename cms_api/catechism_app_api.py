import os

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from .models.base import db
from .blueprints import register_blueprints
from .helpers.auth_helpers import login_manager


def create_app(test_config=None):
    load_dotenv()

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI"),
        SESSION_COOKIE_DOMAIN=os.getenv("SESSION_COOKIE_DOMAIN"),
        SESSION_COOKIE_SAME_SITE="Lax",
        SECRET_KEY=os.getenv("SECRET_KEY"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    CORS(app, supports_credentials=True, origins=(os.getenv("CORS_ORIGINS") if os.getenv("CORS_ORIGINS") else "").split(","))

    db.init_app(app)

    login_manager.init_app(app)

    register_blueprints(app, "/api")

    return app
