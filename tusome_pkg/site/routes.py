from flask import render_template, session
from tusome_pkg.site import bp 
from models import Book

@bp.route('/home')
def home_page():
    return render_template('site/home.html', session = session)

@bp.route('/reviews')
def review_page():
    return render_template('site/reviews.html')

@bp.route('/details')
def book_details():
    return render_template('site/book_detail.html')