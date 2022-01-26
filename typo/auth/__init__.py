from flask import Blueprint

bp = Blueprint('auth', __name__)

from typo.auth import routes