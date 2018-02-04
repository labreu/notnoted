import os
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

def init_db():
	try:
		os.system('export FLASK_APP=main.py; flask db init;flask db migrate;flask db upgrade')
	except Exception as e:
		print(e)

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
try:
	os.makedirs('app/static/notebooks/')
except:
	pass

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'youwillneverguess')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'app/static/notebooks/'

db = SQLAlchemy(app)
login = LoginManager(app)
migrate = Migrate(app, db)
login.login_view = 'login'

#init_db()

from app import routes, models
