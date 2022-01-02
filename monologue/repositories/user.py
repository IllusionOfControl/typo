from monologue.models import User
from monologue import db

class UserRepository():
    def check_username_is_taken(username):
        exist_query = User.query.filter_by(username=username).exists()
        if db.session.query(exist_query):
            return True
        return False

    def check_email_is_taken(email):
        exist_query = User.query.filter_by(email=email).exists()
        if db.session.query(exist_query):
            return True
        return False

    def create_user(username, email, password):
        return User(username=username,
                email=email,
                password=email)