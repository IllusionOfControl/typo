from flask import Blueprint

bp = Blueprint('main', __name__)

from monologue.main import routes