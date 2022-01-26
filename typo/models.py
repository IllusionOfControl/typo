from flask_login import UserMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from typo import login_manager, db
from typo.utils.crypto import hash_password
from datetime import datetime


post_tags_association_table = db.Table('post_tags_association_table',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)

likes_association_table = db.Table('likes_association_table',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))

    def __repr__(self):
        return '<Tag {}>'.format(self.name)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    body = db.Column(db.String)
    tags = db.relationship("Tag", secondary=post_tags_association_table)
    who_liked = db.relationship("User", secondary=likes_association_table)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))    
    
    def __repr__(self):
        return '<Post {}>'.format(self.title)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    email = db.Column(db.String(128), unique = True)
    password = db.Column(db.String(128))
    created = db.Column(db.DateTime, default=datetime.utcnow)

    avatar = db.Column(db.String(128))
    about_me = db.Column(db.String(256))
    website = db.Column(db.String(128))
    banned = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    posts = db.relationship('Post', backref='author', lazy='dynamic')

    @validates("password")
    def validate_password(self, key, plaintext):
        return hash_password(str(plaintext))

    def __repr__(self):
        return '<User {}>'.format(self.username)


from typo import login_manager

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))
