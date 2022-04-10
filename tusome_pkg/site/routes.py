from xml.dom.expatbuilder import parseString
from flask import render_template, session
from tusome_pkg.site import bp 
#from models import Book
import os, urllib.request, json

@bp.route('/home')
def home_page():
    

    return render_template('site/landing_page.html', session = session)

@bp.route('/reviews')
def review_page():
    return render_template('site/reviews.html')

@bp.route('/details')
def book_details():
    return render_template('site/book_detail.html')

@bp.route('/bestsellers')
def bestseller_page():
    bestsellers_dict = get_bestsellers()
    book_list = []
    i = 0
    while i < 15:
        isbn13 = bestsellers_dict[i]["primary_isbn13"]
        author = bestsellers_dict[i]["author"]
        title = bestsellers_dict[i]["title"]
        description = bestsellers_dict[i]["description"]
        cover = bestsellers_dict[i]["book_image"]
        #append to empty list a dictionary with isbn13, title, description, author, book_image
        book_list.append({"isbn":isbn13, "title": title, "author":author, "description":description, "cover":cover})
        i+=1
        print("This is the list: \n" )
        print(book_list)
    return render_template('site/bestsellers.html', session = session, books = book_list)

#Make API calls to the NYTimes Books API
def get_bestsellers():
    url = "https://api.nytimes.com/svc/books/v3/lists/current/hardcover-fiction.json?api-key={}".format(os.environ.get("NYT_APIKEY"))
    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)
    print (dict["results"]["books"])
    return dict["results"]["books"]