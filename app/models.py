from app import db
from datetime import datetime

post_categories = db.Table('post_categories',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'))
)


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    description = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    body = db.Column(db.String)
    categories = db.relationship('Category', secondary=post_categories,
                            primaryjoin=(post_categories.c.post_id == id),
                            secondaryjoin=(post_categories.c.category_id == Category.id),
                            lazy='dynamic')
    
    def __repr__(self):
        return '<Post {}>'.format(self.body)

