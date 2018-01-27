from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class SearchForm(FlaskForm):
    search_string = StringField('Search', validators=[DataRequired('wtf..you want to search without typing anything?')])
    submit = SubmitField('Go')


class LoginForm(FlaskForm):
    username = StringField('User', validators=[DataRequired('really?')])
    pw = PasswordField('PW', validators=[DataRequired('password pls')])
    submit = SubmitField('Enter')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Username mandatory for registration')])
    email = StringField('Email', validators=[DataRequired('Email mandatory for registration'), Email('Use a valid email')])
    password = PasswordField('Password', validators=[DataRequired('Fill in the password field')])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired('Fill in the password field'), EqualTo('password', 'Non-matching passwords')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email already in database.')
