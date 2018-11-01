from flask import Flask, g, render_template, request, redirect, url_for, make_response, flash, abort

from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

import forms
import models

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'This is a secret key, you shouldnt know about'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request"""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close database connection after each request"""
    g.db.close()
    return response



@app.route('/new', methods=('GET', 'POST'))
def new():
    form = forms.PostForm()
    if form.validate_on_submit():
        models.User.create(
            title=form.title.data,
            date=form.date.data,
            time_spent=form.time_spent.data,
            what_i_learned=form.what_i_learned.data,
            resources_to_remember=form.resources_to_remember.data
            )
        flash("Message posted! Thanks!", "success")
        return redirect(url_for('index'))
    return render_template('new.html', form=form, legend='New Post')

@app.route('/')
def index():
    stream = models.User.select().limit(100)
    return render_template('index.html', stream=stream)


@app.route('/detail/<int:post_id>')
def detail(post_id):
    post = models.User.get_by_id(post_id)
    return render_template('detail.html', post=post)

@app.route('/detail/<int:post_id>/edit', methods=('GET', 'POST'))
def edit_post(post_id):
    post = models.User.get_by_id(post_id)
    form = forms.PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.date = form.date.data
        post.time_spent = form.time_spent.data
        post.what_i_learned = form.what_i_learned.data
        post.resources_to_remember = form.resources_to_remember
        post.save()

        flash('You post has been updated', "success")
        return redirect(url_for('detail', post_id=post.id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.date.data = post.date
        form.time_spent.data = post.time_spent
        form.what_i_learned.data = post.what_i_learned
        form.resources_to_remember.data = post.resources_to_remember

    return render_template('new.html', form=form, legend='Edit Post')



@app.route('/detail/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = models.User.get_by_id(post_id)
    post.delete_instance()
    flash('You post has been deleted', "success")
    return redirect(url_for('index'))


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)