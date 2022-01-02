from monologue.models import User
from monologue import db

class UserRepository():
    def check_username_is_taken(self, username) -> bool:
        exist_query = User.query.filter_by(username=username).exists()
        if db.session.query(exist_query).scalar():
            return True
        return False

    def check_email_is_taken(self, email) -> bool:
        exist_query = User.query.filter_by(email=email).exists()
        if db.session.query(exist_query).scalar():
            return True
        return False

    def create_user(self, username, email, password, with_commit=True) -> User:
        user = User(username=username,
                email=email,
                password=email)
        db.session.add(user)
        if with_commit:
            db.session.commit()
        return user

    def get_user_by_username(self, username) -> User:
        return User.query.filter_by(username=username).one()