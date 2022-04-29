
from xml.dom.expatbuilder import parseString
from flask import flash, render_template, session, request
from tusome_pkg.forms import ReviewForm
from tusome_pkg.site import bp 
from tusome_pkg.models import Book, Review, User
import os, urllib.request, json
from flask_login import login_required

@bp.route('/home')
def home_page():
    

    return render_template('site/landing_page.html', session = session)

@bp.route('/reviews')
def review_page():
    return render_template('site/reviews.html')

@bp.route('/details/<isbn>')
def book_details(isbn):
    book = get_book_from_bestsellers(isbn)
    return render_template('site/book_details.html', book=book, session=session)

@bp.route('/bestsellers')
def bestseller_page():
    book_list = get_bestsellers_list()
    return render_template('site/bestsellers.html', session = session, books = book_list)

@bp.route("/my_reviews")
@login_required
def my_reviews():
    user = User.query.filter_by(username=session['username']).first()
    user_id = user.id
    user_reviews = Review.query.filter_by(user_id = user_id).all()

    return render_template('site/my_reviews.html', session = session, reviews = user_reviews)


@bp.route("/write_review", methods=['GET', 'POST'])
@login_required
def write_review(book):
    #TODO: Write unit test for a dummy review
    # Has to be a better way to do this than query the db three times
    review_author = User.query.filter_by(username=session['username']).first()
    user_id = User.query.filter_by(username=review_author).first().id
    book_id = Book.query.filter_by(book_title=book.book_title).first().id
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(title = book.book_title, book_review=form.review.data, user_id=user_id)
        flash("Review successfully posted", category='success')
    return render_template('site/write_review.html', session=session, writer=review_author)

#General book reviews
@bp.route("/book_reviews")
def book_reviews(book):
    
    return render_template('site/reviews.html')


#Make API calls to the NYTimes Books API
def get_bestsellers():
    url = "https://api.nytimes.com/svc/books/v3/lists/current/hardcover-fiction.json?api-key={}".format(os.environ.get("NYT_APIKEY"))
    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)
    return dict["results"]["books"]

#Put the bestsellers in list form for the webpage
def get_bestsellers_list():
    bestsellers_dict = get_bestsellers()
    book_list = []
    i = 0
    while i < 15:
        isbn13 = bestsellers_dict[i]["primary_isbn13"]
        author = bestsellers_dict[i]["author"]
        book_title = bestsellers_dict[i]["title"]
        description = bestsellers_dict[i]["description"]
        cover = bestsellers_dict[i]["book_image"]
        #append to empty list a dictionary with isbn13, title, description, author, book_image
        book_list.append({"isbn":isbn13, "book_title": book_title, "author":author, "description":description, "cover":cover})
        i+=1
    return book_list

def get_book_from_bestsellers(isbn):
    book_list = get_bestsellers_list()
    for book in book_list:
        if isbn == book["isbn"]:
            return book
    return 