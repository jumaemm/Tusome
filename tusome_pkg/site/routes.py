
from xml.dom.expatbuilder import parseString
from flask import flash, redirect, render_template, session, request, url_for
from tusome_pkg.forms import ReviewForm, BookForm
from tusome_pkg.site import bp 
from tusome_pkg.models import Book, Review, User, db
import os, urllib.request, json
from flask_login import login_required
from tusome_pkg.decorators import admin_required

@bp.route('/home')
def home_page():
    

    return render_template('site/landing_page.html', session = session)

@bp.route('/upload', methods=['GET', 'POST'])
@login_required
@admin_required
def book_upload():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(isbn = form.isbn.data,
                    book_title = form.book_title.data,
                    author = form.author.data,
                    description = form.description.data,
                    cover = form.cover.data)
        db.session.add(book)
        db.session.commit()
        flash(f'Successfully uploaded {form.book_title.data}', category='SUCCESS')
        return redirect(url_for('site.landing_page'))
    return render_template('site/upload_book.html', form = form)
    

@bp.route('/details/<isbn>')
def book_details(isbn):
    book = get_book_from_bestsellers(isbn)
    session['current_book'] = book
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
def write_review():
    #TODO: Write unit test for a dummy review
    # Has to be a better way to do this than query the db three times
    book = session['current_book']
    print (book)
    review_author = User.query.filter_by(username=session['username']).first()
    print (review_author)
    user_id = User.query.filter_by(username=review_author.username).first().id
    book_id = Book.query.filter_by(isbn=book['isbn']).first().isbn
    print ("This is the book ID: " + str(book_id))
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(review_title = form.review_title.data, book_review=form.review.data, user_id=user_id, book_id = book_id)
        db.session.add(review)
        db.session.commit()
        flash("Review successfully posted", category='success')
        return redirect(url_for('site.home_page'))
    
    return render_template('site/write_review.html', session=session, writer=review_author, book = book, form = form)

#General book reviews
@bp.route("/book_reviews/<isbn>")
def book_reviews(isbn):
    book = get_book_from_bestsellers(isbn)
    print ("This is the book: \n" + str(book))
    review_list = Review.query.filter_by(book_id = book['isbn']).all()
    print ("This is the review list right here lads")
    print (review_list)
    return render_template('site/reviews.html', reviews = review_list, book = book)


#Make API calls to the NYTimes Books API
def get_bestsellers():
    url = "https://api.nytimes.com/svc/books/v3/lists/current/hardcover-fiction.json?api-key={}".format(os.environ.get("NYT_APIKEY"))
    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)
    return dict["results"]["books"]

def get_bestsellers_list():
    """
    Runs get_bestsellers() and returns a list of dictionaries with isbn13, title, description, author, book_image
    """
    bestsellers_dict = get_bestsellers()
    book_list = []
    i = 0
    while i < 15:
        isbn13 = bestsellers_dict[i]["primary_isbn13"]
        author = bestsellers_dict[i]["author"]
        book_title = bestsellers_dict[i]["title"]
        description = bestsellers_dict[i]["description"]
        cover = bestsellers_dict[i]["book_image"]
        book = Book(isbn = isbn13, book_title = book_title, author = author, description = description, cover = cover)
        if Book.query.filter_by(isbn = isbn13).first():
            pass
        else:
            db.session.add(book)
        #append to empty list a dictionary with isbn13, title, description, author, book_image
        book_list.append({"isbn":isbn13, "book_title": book_title, "author":author, "description":description, "cover":cover})
        i+=1
    db.session.commit()
    return book_list

def get_book_from_bestsellers(isbn):
    book_list = get_bestsellers_list()
    for book in book_list:
        if isbn == book["isbn"]:
            return book
    return 

    