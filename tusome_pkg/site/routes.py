from flask import render_template
from tusome_pkg.site import bp 

@bp.route('/home')
def home_page():
    return render_template('site/home.html')