from app import app
from flask import render_template, redirect, request
from app.forms import LoginForm, SearchForm

user = None

@app.route('/')
@app.route('/index')
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

@app.route('/manageposts')
def manageposts():
    return redirect('index')

@app.route('/manageaccount')
def manageaccount():
    return redirect('index')