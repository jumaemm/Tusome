#TODO: User, Book, Review, Preferences
from encodings import utf_8
from enum import unique
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin
from datetime import datetime

bcrypt = Bcrypt()
db = SQLAlchemy()

#intermediate table for books to users
books_users = db.Table('books_users', 
                        db.Column('user_id',db.Integer, db.ForeignKey('user.id'), primary_key=True), 
                        db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True)
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable= False)
    password_hash = db.Column(db.String(60), nullable=False)
    books = db.relationship('Book', secondary=books_users, backref='users' , lazy=True)
    reiews = db.relationship('Review', backref = 'user', lazy = True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf_8')

    def check_password_correction(self, password_attempt):
        return bcrypt.check_password_hash(self.password_hash, password_attempt)
            
    
    def __repr__(self) -> str:
        return f'User: {self.username}'

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.Integer, unique=True)
    book_title = db.Column(db.String(400), nullable=False)
    author = db.Column(db.String(120),nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    cover = db.Column(db.String(), nullable=False) 
    reviews = db.relationship('Review', backref='book', lazy=True)

#TODO: OWNERS

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, unique=True)
    book_review = db.Column(db.String(2028))
    created = db.Column(db.DateTime, default=datetime.now())
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

