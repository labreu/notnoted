from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    search_string = StringField('Search', validators=[DataRequired('wtf..you want to search without typing anything?')])
    submit = SubmitField('Go')

class LoginForm(FlaskForm):
    username = StringField('User', validators=[DataRequired('really?')])
    pw = PasswordField('PW', validators=[DataRequired('password pls')])
    submit = SubmitField('Enter')

