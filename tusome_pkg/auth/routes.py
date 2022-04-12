#TODO: LogIn, Register, Logout Error handling
from statistics import mode
from passlib.hash import sha256_crypt
from flask import flash, render_template, session, redirect, url_for, get_flashed_messages
from tusome_pkg.auth import bp 
from tusome_pkg.forms import RegisterForm, LoginForm
from tusome_pkg.models import User, db, bcrypt
from flask_login import login_user
#TODO: Roll register and login modals to site view

@bp.route('/login', methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(password_attempt=form.password.data):
            login_user(attempted_user)
            flash(f'Successfully logged in as: {attempted_user.username}', category='success')
            session['logged_in'] = True
            return redirect(url_for('site.home_page'))
        else:
            flash('Username or password incorrect, please try again', category='danger')
    return render_template('auth/login_modal.html', form = form)

@bp.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create= User(username=form.username.data,
                             email=form.email_address.data,
                             password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        flash(f'Successfully registered as {form.username.data}', category='success')
        return redirect(url_for('auth.login'))
    if form.errors != {}: #If errors is not empty
        for err_msg in form.errors.values():
            flash(f'Error creating user: {err_msg}', category="danger")
    return render_template('auth/register_modal.html', form = form)

@bp.route('/logout')
def logout():
    session.clear()
    flash("Successfully logged out", category='info')
    return redirect(url_for('site.home_page'))
