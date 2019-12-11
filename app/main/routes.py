from flask import render_template, redirect, url_for
from app import db
from app.models import Post
from app.main import bp
from app.main.forms import EditPostForm


@bp.route('/post/<int:post_id>/edit', methods=['GET','POST'])
def post_edit(post_id):
    form = EditPostForm()
    if form.validate_on_submit():
        post = Post.query.filter_by(id=post_id).first_or_404()
        post.title = form.title.data
        post.description = form.description.data
        post.body = form.body.data
        db.session.commit()
        return redirect(url_for('post', post_id=post_id))
    post = Post.query.filter_by(id=post_id).first_or_404()
    
    form.title.data = post.title
    form.description.data = post.description
    form.body.data = post.body
    return render_template('post_edit.html', form=form, edit=True)

@bp.route('/')
@bp.route('/index')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@bp.route('/post/<post_id>')
def post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    return render_template('post.html', post=post)

from app.main.forms import EditPostForm


@bp.route('/post/add', methods=['GET', 'POST'])
def post_add():
    form = EditPostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    description=form.description.data,
                    body=form.body.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('post', post_id=post.id))
    return render_template('post_create.html', form=form)


@bp.route('/base')
def base():
    return render_template('base.html')