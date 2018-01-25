from app import app
from flask import render_template, redirect, request
from app.forms import LoginForm, SearchForm
from app.models import User, Post
from app import db

user = None

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    login_form = LoginForm(prefix='l')
    search_form = SearchForm(prefix='s')
    if user:
        print('hasuser', user)
        return render_template('index.html', search=search_form, login=login_form, user=user)
    else:
        print('nouser', user)    
        return render_template('index.html', search=search_form, login=login_form)

@app.route('/login', methods=['POST'])
def login():
    print(request.form)
    global user
    login_form = LoginForm(prefix='l')
    if login_form.validate_on_submit():
        user = {'username': request.form.get('l-username'),
                'password': request.form.get('l-pw')}

        u = User.query.filter_by(username=user.get('username', 'Nenhum')).first()
        if u:
            if u.password_hash != user.get('password', "Nenhuma"):
                user = None
        else:
            user = None
    else:
        user = None
    return redirect('index')

@app.route('/logout')
def logout():
    global user
    user = None
    return redirect('index')

@app.route('/post')
def post():
    global user
    if user is not None:
        return render_template('post.html', user=user)
    else:
        return redirect('index')

@app.route('/posttext', methods=['POST', 'GET'])
def posttext():
    text = request.json
    print("TEXTO:", text, type(text))

    return ""


@app.route('/manageposts')
def manageposts():
    return "Em construcao posts"

@app.route('/manageaccount')
def manageaccount():
    return "Em construcao account"