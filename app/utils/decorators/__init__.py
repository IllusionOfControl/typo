from flask import request, redirect, url_for, abort
from flask_login import current_user
from functools import wraps


def author_only(f):
    pass

def admin_only(f):
    pass

def anonimous_only(f):
    pass

def route_not_implemented(f):
    @wraps(f)
    def _route_not_implemented(*args, **kwargs):
        abort(501)
    
    return _route_not_implemented