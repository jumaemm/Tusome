#TODO: User, Book, Review, Preferences
from encodings import utf_8
from enum import unique
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, current_user
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
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['TUSOME_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf_8')

    def check_password_correction(self, password_attempt):
        return bcrypt.check_password_hash(self.password_hash, password_attempt)
            
    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

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

    def __repr__(self) -> str:
        return f'Book: {self.book_title}'

    def __str__(self) -> str:
        return f'Book: {self.book_title}'
#TODO: OWNERS

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, unique=True)
    book_review = db.Column(db.String(2028))
    created = db.Column(db.DateTime, default=datetime.now())
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
            roles = {
                'User': (Permission.FOLLOW |
                        Permission.COMMENT |
                        Permission.REVIEW, True),
                'Moderator': (Permission.FOLLOW |
                            Permission.COMMENT |
                            Permission.REVIEW |
                            Permission.MODERATE_COMMENTS, False),
                'Administrator': (0xff, False)
            }
            for r in roles:
                role = Role.query.filter_by(name=r).first()
                if role is None:
                    role = Role(name=r)
                role.permissions = roles[r][0]
                role.default = roles[r][1]
                db.session.add(role)
            db.session.commit()

class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    REVIEW = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80