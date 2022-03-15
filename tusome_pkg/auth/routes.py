#TODO: Index(Best Sellers), LogIn, Register, My Reviews, Book, 
from flask import render_template
from tusome_pkg.auth import bp 
@bp.route('/login', methods=['GET','POST'])
def login():
    return render_template('login_modal.html')