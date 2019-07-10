import os

from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from db_manager import DBManager
from user import User
from flask import jsonify, render_template, request
import flask
from datetime import datetime
from error_codes import ErrorCodes

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
dbmanager = DBManager(db)


# This is the python file that stores all the routing information

# default route for the application, every time this is accessed it explicitly clears of any active sessions for a user.
@app.route("/")
def index():
    del session['user_id']
    del session['user_email']
    return render_template("index.html")


# mapping for the search get request which is invoked from the navigation bar. If the user is not logged in currently it forces the user to login screen.
@app.route("/search", methods=["GET"])
def search_for_get():
    if 'user_id' in session and session['user_id']:
        return render_template("search.html", name=session['user_email'])
    else:
        return render_template("index.html")


# mapping for the search screen to be shown post a successful login with a valid username and password.
@app.route("/search", methods=["POST"])
def search():
    # check if there is an active usersession, in which case lookup the request search string.
    if 'user_id' in session and session['user_id']:
        search_str = request.form.get("search_str")
        if search_str:
            books = dbmanager.search_books_by_isbn_title_author(search_str);
            if not books:
                return render_template("search.html", name=session['user_email'],
                                       message="No books found matching the specified criteria")
        return render_template("search.html", name=session['user_email'], books=books)
    else:
        # if there is no active session, lookup the email and password and validate the user. Post a successful login set the userid and the username in the session
        email = request.form.get("email")
        password = request.form.get("password")
        user = User()
        db_stored_password = user.get_salted_password(password)
        resp = dbmanager.find_user(email, db_stored_password)
        if not resp:
            return render_template("index.html", reason="Login failed: Invalid username or password.")
        session['user_id'] = resp["id"]
        session['user_email'] = email
        return render_template("search.html", name=session['user_email'])


# route mapping when a user clicks register button on the login screen
@app.route("/register", methods=["GET"])
def register_for_get():
    return render_template("register.html")

# mapping to store the item details for the web page
@app.route("/book_details/<string:isbn>")
def book_details(isbn):
    if 'user_id' in session and session['user_id']:
        book = dbmanager.find_book_by_isbn(isbn, False)
        reviews = dbmanager.find_reviews_by_isbn(isbn)
        return render_template("book_details.html", book=book, reviews=reviews)
    else:
        return render_template("index.html")


# route for logging out a user, this also clears the session state
@app.route("/logout", methods=["GET"])
def logout():
    del session['user_id']
    del session['user_email']
    return render_template("index.html")


# route to invoke for creating a new user account, it does a salt based hashing for the user password and only stored the password in the DB.
@app.route("/register", methods=["POST"])
def register():
    user = User()
    user.create_from_form(request.form)

    user.created_at = datetime.now()
    resp = dbmanager.save_user(user)
    if ErrorCodes.Duplicate == resp:
        error_message = "User with same Email already exists, Please login"
        return render_template("register.html", error_message=error_message)
    elif ErrorCodes.NoError == resp:
        message = "User account successfully created, Please login"
    return render_template("index.html", message=message)


# default application level handler for all 404 type errors
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

# route mapping to expose the book details as a json object in the response
@app.route("/api/<string:isbn>")
def lookup_by_isbn(isbn):
    book = dbmanager.find_book_by_isbn(isbn)
    if not book:
        flask.abort(404)
    else:
        return jsonify(book)

# route mapping to submit a new review/feedback for a book. It
@app.route("/post_feedback", methods=["POST"])
def post_feedback():
    isbn = request.form.get("isbn")

    # check if there is a valid session for the user.
    if 'user_id' in session and session['user_id']:
        review = request.form.get("review")
        error_message = None
        resp = None
        # check the number of characters a user has provided for the review
        if len(review) < 10:
            error_message = "Review must have 10 Characters"

        # if the number of characters is greater attempt to save the review in the DB
        if not error_message:
            resp = dbmanager.save_review(session['user_id'], isbn, review, datetime.now())

        # Error handling based on the error code.
        if ErrorCodes.Duplicate == resp:
            error_message = "You have already submitted a review for this book earlier"
        elif ErrorCodes.NoError == resp:
            resp = "Review saved successfully"
        book = dbmanager.find_book_by_isbn(isbn, False)
        reviews = dbmanager.find_reviews_by_isbn(isbn)

        return render_template("book_details.html", book=book, error_message=error_message, message=resp,
                               reviews=reviews)
    else:
        # if the user is not logged in, take the user to the login screen.
        return render_template("index.html")
