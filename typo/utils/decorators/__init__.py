from flask import request, redirect, url_for, abort
from flask_login import current_user
from functools import wraps
from typo.models import Post


def author_only(f):
    @wraps(f)
    def _author_only(*args, **kwargs):
        post_id = kwargs['post_id']
        post = Post.query.filter_by(id=post_id).first()
        return f if post.author.id == current_user.id else abort(403)
        
    return _author_only


def admin_only(f):
    pass


def anonymous_only(f):
    @wraps(f)
    def _anonymous_only(*args, **kwargs):
        return f if current_user.is_anonymous() else redirect(url_for('main.index'))

    return _anonimous_only


def route_not_implemented(f):
    @wraps(f)
    def _route_not_implemented(*args, **kwargs):
        abort(501)

    return _route_not_implemented