from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from app.models import db, Post
from app.main import bp
from app.main.forms import EditPostForm


@bp.route('/')
@bp.route('/index')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@bp.route('/post/<int:post_id>/edit', methods=['GET','POST'])
def post_edit(post_id):
    form = EditPostForm()
    post = Post.query.filter_by(id=post_id).first_or_404()
    if form.validate and request.method=='POST':
        post.update(
            title = form.title.data,
            description = form.description.data,
            body = form.body.data)
        return redirect(url_for('main.post', post_id=post.id))
    post = Post.query.filter_by(id=post_id).first_or_404()
    
    form.title.data = post.title
    form.description.data = post.description
    form.body.data = post.body
    return render_template('post_edit.html', form=form, edit=True)


@bp.route('/post/<post_id>')
def post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    return render_template('post.html', post=post)


from app.main.forms import EditPostForm


@bp.route('/post/add', methods=['GET', 'POST'])
def post_add():
    form = EditPostForm()
    if form.validate_on_submit():
        post = Post.create(title=form.title.data,
                    description=form.description.data,
                    body=form.body.data,
                    author=current_user)
        return redirect(url_for('main.post', post_id=post.id))
    return render_template('post_create.html', form=form)


@bp.route('/post/<int:post_id>/delete')
def post_delete(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        flash('There is no post to delete')
        return redirect(url_for('main.index'))
    post.delete()
    flash('Post was deleted')
    return redirect(url_for('main.index'))


@bp.route('/users')
def users():
    raise NotImplementedError

@bp.route('/user/<int:user_id>')
def user(user_id):
    raise NotImplementedError

@bp.route('/about')
def about():
    raise NotImplementedError