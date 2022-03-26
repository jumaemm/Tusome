#TODO: Register, LogIn, Review, Preferences
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class RegisterForm(FlaskForm):
    username = StringField(label='Username:')
    email_address = StringField(label='Email:')
    password1 = PasswordField(label='Password:')
    password2 = PasswordField(label='Confirm Password:')
    submit = SubmitField(label='Register')

class LoginForm(FlaskForm):
    username = StringField(label='Username')
