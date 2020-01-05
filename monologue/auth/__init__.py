from flask import Blueprint

bp = Blueprint('auth', __name__)

from monologue.auth import routes