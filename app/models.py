from app import db
from datetime import datetime

post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    description = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    body = db.Column(db.String)
    tags = db.relationship('Tag', secondary=post_tags,
                            primaryjoin=(post_tags.c.post_id == id),
                            secondaryjoin=(post_tags.c.tag_id == Tag.id),
                            lazy='dynamic')
    
    def __repr__(self):
        return '<Post {}>'.format(self.body)

