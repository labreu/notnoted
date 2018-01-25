from app import db
from app import app
from app import login
from app.models import User, Post
from app.forms import LoginForm, SearchForm
from flask import render_template, redirect, request, url_for
from flask_login import login_user, logout_user, login_required, current_user

user = None

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    search_form = SearchForm()
    return render_template('index.html', search=search_form, user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.pw.data):
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    else:
        return render_template('login.html', title='Sign In', login=form)

@app.route('/search', methods=['GET', 'POST'])
def search():
    return 'TBD'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/post')
@login_required
def post():
    return render_template('post.html', user=user)

@app.route('/posttext', methods=['POST', 'GET'])
@login_required
def posttext():
    text = request.json
    print("TEXTO:", text, type(text))
    return ""

@app.route('/manageposts')
@login_required
def manageposts():
    return "Em construcao posts"

@app.route('/manageaccount')
@login_required
def manageaccount():
    return "Em construcao account"