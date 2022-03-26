#TODO: Index(Best Sellers), LogIn, Register, My Reviews, Book, 
from statistics import mode
from flask import render_template, session, redirect, url_for
from tusome_pkg.auth import bp 
from tusome_pkg.forms import RegisterForm
from tusome_pkg.models import User, db

@bp.route('/login', methods=['GET','POST'])
def login():
    return render_template('auth/login_modal.html')

@bp.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create= User(username=form.username.data,
                             email=form.email_address.data,
                             password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        print("something")
        return redirect(url_for('site.home_page'))
    return render_template('auth/register_modal.html', form = form)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('site.home_page'))
