from flask_login import LoginManager
from app.models import User

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

