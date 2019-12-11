import unittest
from app.models import Tag, Post
from app import db, create_app
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class PostModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def test_create_post(self):
        tag1 = Tag(name="tag1")
        tag2 = Tag(name="tag2")
        tag3 = Tag(name="tag3")      

        db.session.add_all([tag1, tag2, tag3])
        db.session.commit()
        post1 = Post(title='post1')
        post2 = Post(title='post2')
        post2.tags.append(tag1)
        post2.tags.append(tag2)
        post2.tags.append(tag3)
        db.session.add_all([post1, post2])
        db.session.commit()
        self.assertEqual(len(db.session.query(Post).all()), 2)
        self.assertEqual(len(post2.tags.all()), 3)

    def edit_post(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)
