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

    return app