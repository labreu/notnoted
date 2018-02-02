from app import db
from app import app
from app import login
from app.models import User, Post
from app.forms import LoginForm, SearchForm, RegistrationForm
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

user = None

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    #search_form = SearchForm()
    #return render_template('index.html', search=search_form, user=user)
    return redirect('feed')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.pw.data):
            flash('Please login.')
            return redirect(url_for('login'))
        flash('Welcome!')
        login_user(user)
        return redirect(url_for('index'))
    else:
        return render_template('login.html', title='Sign In', login=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Welcome! Please log in!')
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', register=form)

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
    post = Post(body=text['text'], title=text['title'], author=current_user)
    db.session.add(post)
    db.session.commit()

    return ''

@app.route('/posts/<id>')
def get_post_by_id(id):
    post = Post.query.filter_by(id=id).first()
    return render_template('post_by_id.html', post=post)

@app.route('/feed')
def feed():
    posts = Post.query.all()
    return render_template('feed.html', posts=posts)

@app.route('/manageposts')
@login_required
def manageposts():
    posts = Post.query.filter_by(author=current_user).all()
    return render_template('manageposts.html', posts=posts)

@app.route('/manageaccount')
@login_required
def manageaccount():
    return "Em construcao account"
