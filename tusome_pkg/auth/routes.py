#TODO: Index(Best Sellers), LogIn, Register, My Reviews, Book, 
from flask import render_template
from tusome_pkg.auth import bp 
from tusome_pkg.forms import RegisterForm

@bp.route('/login', methods=['GET','POST'])
def login():
    return render_template('auth/login_modal.html')

@bp.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    return render_template('auth/register_modal.html', form = form)