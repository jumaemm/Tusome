from flask import render_template, session
from tusome_pkg.site import bp 
#from models import Book
import os, urllib.request, json

@bp.route('/home')
def home_page():
    #bestsellers_dict = get_bestsellers()
    book_list = []
    i = 0
    #while i < 15:
        #append to empty list a dictionary with isbn13, title, description, author, book_image
        #book_list.append([{bestsellers_dict.books[i].isbns.isbn13: bestsellers_dict.books[i].title, }])
    return render_template('site/landing_page.html', session = session)

@bp.route('/reviews')
def review_page():
    return render_template('site/reviews.html')

@bp.route('/details')
def book_details():
    return render_template('site/book_detail.html')

#Make API calls to the NYTimes Books API
def get_bestsellers():
    url = "https://api.nytimes.com/svc/books/v3/lists/current/hardcover-fiction.json?api-key={}".format(os.environ.get("NYT_APIKEY"))
    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)
    return dict.results