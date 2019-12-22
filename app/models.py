from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property

from app import login_manager
from app.utils.crypto import hash_password
from datetime import datetime

db = SQLAlchemy()

class CRUDMixin(object):
    """ Mixin that adds methods for CRUD operations. """

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()


    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save()


    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()


    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self


class Model(CRUDMixin, db.Model):
    """ Abstract model class that includes CRUD methods"""
    __abstract__ = True


post_categories = db.Table('post_categories',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'))
)


class Category(Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))

    def __repr__(self):
        return '<Tag {}>'.format(self.name)


class Post(Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    description = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    body = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    categories = db.relationship('Category', secondary=post_categories,
                            primaryjoin=(post_categories.c.post_id == id),
                            secondaryjoin=(post_categories.c.category_id == Category.id),
                            lazy='dynamic')
    
    def __repr__(self):
        return '<Post {}>'.format(self.title)

class User(UserMixin, Model):
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
    verified = db.Column(db.Boolean, default=False)
    hidden = db.Column(db.Boolean, default=False)

    posts = db.relationship('Post', backref='author', lazy='dynamic')

    @validates("password")
    def validate_password(self, key, plaintext):
        return hash_password(str(plaintext))

    def __repr__(self):
        return '<User {}>'.format(self.username)