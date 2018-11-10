from flask import Flask, g, render_template, request, redirect, url_for, flash, abort

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
    g.db.connect(reuse_if_open=True)
    g.user = current_user


@app.after_request
def after_request(response):
    """Close database connection after each request"""
    g.db.close()
    return response


@app.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = forms.PostForm()
    if form.validate_on_submit():
        models.Post.create(
            title=form.title.data,
            date=form.date.data,
            time_spent=form.time_spent.data,
            what_i_learned=form.what_i_learned.data,
            resources_to_remember=form.resources_to_remember.data
            )
        flash("Message posted! Thanks!", "success")
        return redirect(url_for('index'))
    return render_template('new_post.html', form=form, legend='New Post')


@app.route('/')
def index():
    stream = models.Post.select().limit(5)
    stream.order_by(models.Post.posted_at.asc())
    return render_template('index.html', stream=stream)


@app.route('/detail/<int:post_id>')
def detail(post_id):
    try:
        post = models.Post.get_by_id(post_id)
        return render_template('detail.html', post=post)
    except models.DoesNotExist:
        abort(404)


@app.route('/detail/<int:post_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_post(post_id):
    try:
        post = models.Post.get_by_id(post_id)
        form = forms.PostForm()
        if form.validate_on_submit():
            post.title = form.title.data
            post.date = form.date.data
            post.time_spent = form.time_spent.data
            post.what_i_learned = form.what_i_learned.data
            post.resources_to_remember = form.resources_to_remember.data
            post.save()

            flash('You post has been edited', "success")
            return redirect(url_for('detail', post_id=post.id))

        elif request.method == 'GET':
            form.title.data = post.title
            form.date.data = post.date
            form.time_spent.data = post.time_spent
            form.what_i_learned.data = post.what_i_learned
            form.resources_to_remember.data = post.resources_to_remember

        return render_template('new_post.html', form=form, legend='Edit Post')
    except models.DoesNotExist:
        abort(404)


@app.route('/detail/<int:post_id>/delete', methods=['POST', 'GET'])
@login_required
def delete_post(post_id):
    post = models.Post.get_by_id(post_id)
    post.delete_instance()
    flash('You post has been deleted', "success")
    return redirect(url_for('index'))


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.username == form.username.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in!", "success")
                return redirect(url_for('index'))
            else:
                flash("Your username or password doesn't match!", "error")
    return render_template('login.html', form=form)


@app.route('/entries')
def list():
    stream = models.Post.select().limit(100)
    return render_template('list.html', stream=stream)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out! Come back soon!", "success")


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username='Tester',
            password='Password',
            admin=True
        )
    except ValueError:
        pass

    app.run(debug=DEBUG, host=HOST, port=PORT)
