from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from config import Config


db = SQLAlchemy()
migrate = Migrate()
moment = Moment()

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app,db)
    moment.init_app(app)

    from app.main import bp as bp_main
    app.register_blueprint(bp_main)

    from app.errors import (
        forbidden,
        page_not_found,
        general_error,
    )
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(502, general_error)
    return app