import os
from datetime import datetime
from app import db
from app import app
from app import login
from app.models import User, Post
from app.forms import LoginForm, SearchForm, RegistrationForm
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename

user = None
ALLOWED_EXTENSIONS = set(['html'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        d = datetime.now().strftime('%Y.%m.%d-%H.%M.%S')
        filename = filename.replace('.html', '') + '{}.html'.format(d)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        text = request.json
        print(request.form)
        print(request.args)
        print(text)
        post = Post(file=filename, title=request.form.get('title', 'Notebook'), author=current_user)
        db.session.add(post)
        db.session.commit()

        return redirect('/posts/{}'.format(post.id))  #get_post_by_id(post.id)

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
        #flash('Welcome! Please log in!')
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

@app.route('/deletepost/<id>/<hide>')
@login_required
def deletepost(id, hide=1):
    print('hide',hide)
    p = Post.query.filter_by(id=id).filter_by(author=current_user).first()
    print('p1', p.deleted)
    if p is not None:
        if hide == '1':
            p.deleted = True
        elif hide == '2':
            p.deleted = False
        db.session.merge(p)
        db.session.commit()

        print('p2', Post.query.filter_by(id=id).first().deleted)
    return redirect('/feed')

@app.route('/posts/<id>')
def get_post_by_id(id):
    post = Post.query.filter_by(id=id).first()
    if post is None or post.deleted:
        return redirect('/feed')
 
    if post.file is None:
        return render_template('post_by_id.html', post=post)
    else:
        return render_template('render_nb.html', nb=post.file)

@app.route('/feed')
def feed():
    posts = Post.query.filter(Post.deleted==False).all()
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
