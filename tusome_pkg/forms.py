#TODO: Register, LogIn, Review, Preferences
from statistics import covariance
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, URLField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from tusome_pkg.models import User
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

bcrypt = Bcrypt()
login_manager = LoginManager()
class RegisterForm(FlaskForm):
    #Catch any errors due to similar username
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please enter a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email address already exists! Please login instead.')
    

    username = StringField(label='Username:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Register')

class LoginForm(FlaskForm):
    username = StringField(label='Username:', validators=[DataRequired()])
    password = PasswordField(label='Password: ', validators=[DataRequired()])
    submit = SubmitField(label='Login')

class ReviewForm(FlaskForm):
    user = StringField(label='Username', validators=[DataRequired()])
    review = TextAreaField(label='Review',validators=[Length(min = 10, max = 2000), DataRequired()])
    book_isbn = StringField(label='Book', validators=[Length(min=13)])
    submit = SubmitField(label='Submit')

class BookForm(FlaskForm):
    isbn = StringField(label='ISBN13:', validators=[Length(min=13), DataRequired()])
    book_title = StringField(label='Title', validators=[Length(min=1,  max= 200), DataRequired()])
    author= StringField(label='Author', validators=[Length(min=1,  max= 200), DataRequired()])
    description = TextAreaField(label='Description', validators=[Length(min=1,  max= 200), DataRequired()])
    cover = URLField(label='Cover URL: ')
    submit = SubmitField(label='Submit')
