from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask_login import LoginManager
from flask_mail import Mail
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
moment = Moment()
mail = Mail()


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    
    db.init_app(app)
    migrate.init_app(app,db)
    moment.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    mail.init_app(app)

    with app.app_context():
        db.create_all()

    from typo.main import bp as bp_main
    from typo.auth import bp as bp_auth
    app.register_blueprint(bp_main)
    app.register_blueprint(bp_auth)

    from typo.errors import (
        forbidden,
        page_not_found,
        general_error,
        not_implemented
    )
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, general_error)
    app.register_error_handler(501, not_implemented)
    return app