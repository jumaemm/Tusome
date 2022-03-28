#TODO: Index(Best Sellers), LogIn, Register, My Reviews, Book, 
from statistics import mode
from passlib.hash import sha256_crypt
from flask import flash, render_template, session, redirect, url_for, get_flashed_messages
from tusome_pkg.auth import bp 
from tusome_pkg.forms import RegisterForm, LoginForm
from tusome_pkg.models import User, db

@bp.route('/login', methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        hashed_password=sha256_crypt.encrypt(form.password.data)

    return render_template('auth/login_modal.html')

@bp.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        #TODO: Use bcrypt instead of passlib
        hashed_password = sha256_crypt.encrypt(form.password1.data) #Not sure how secure this is. Read up on it
        user_to_create= User(username=form.username.data,
                             email=form.email_address.data,
                             password_hash=hashed_password)
        db.session.add(user_to_create)
        db.session.commit()
        print("something")
        return redirect(url_for('site.home_page'))
    if form.errors != {}: #If errors is not empty
        for err_msg in form.errors.values():
            flash(f'Error creating user: {err_msg}', category="danger")
    return render_template('auth/register_modal.html', form = form)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('site.home_page'))
