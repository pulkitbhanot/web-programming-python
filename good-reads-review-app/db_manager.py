import sqlalchemy
from error_codes import ErrorCodes


# Class to hand all the Databased interactions via SQL queries

class DBManager:
    def __init__(self, db_session):
        self.db_session = db_session

    # api to find the book details based on a given isbn. there is an optional parameter mini_details which controls if only less information has to be returned as part of the response
    def find_book_by_isbn(self, isbn, mini_details=True):
        if not isbn:
            return None
        else:
            book = self.db_session.execute(
                "SELECT books.id, title, author, year, reviews_count,average_rating  FROM books full outer join books_extended on books.id = books_extended.id WHERE books.id = :id",
                {"id": isbn}).fetchone()
            if not book:
                return None
            else:
                resp = {"title": book.title, "author": book.author, "year": book.year, "isbn": book.id}
                if book.reviews_count:
                    resp["review_count"] = book.reviews_count
                if not mini_details and book.average_rating:
                    resp['average_rating'] = book.average_rating
                return resp

    # api to save a user to the DB, if the user already exists it return an ErrorCode with value Duplicate otherwise return ErrorCodes.NoError
    def save_user(self, user):
        try:
            self.db_session.execute(
                "INSERT INTO users (username, password, firstname, lastname, created_at) VALUES (:username, :password, :firstname,:lastname,:created_at)",
                {"username": user.email, "password": user.password, "firstname": user.firstname,
                 "lastname": user.lastname, "created_at": user.created_at})
            self.db_session.commit()
            return ErrorCodes.NoError
            return "User account successfully created, Please login"
        except sqlalchemy.exc.IntegrityError:
            self.db_session.rollback()
            return ErrorCodes.Duplicate
            return "User with same Email already exists, Please login"

    # api to retrieve a user from DB, this returns a user object only if the passed in email and password are an exact match for the user.
    def find_user(self, email, password):
        user = self.db_session.execute(
            "SELECT id, username, firstname, lastname  FROM users WHERE username = :email and password = :password",
            {"email": email, "password": password}).fetchone()
        if not user:
            return None
        else:
            return {"id": user.id, "email": user.username, "firstname": user.firstname, "lastname": user.lastname}

    # api to search books across ISBN, author and title of the book, it uses the like sql option to lookup across the 3 columns in a single query
    def search_books_by_isbn_title_author(self, search_str):
        search_str_like = '%' + search_str + "%"
        books = self.db_session.execute(
            "SELECT id, title, author, year  FROM books WHERE id like :id or title like :title or author like :author order by id",
            {"id": search_str_like, "title": search_str_like, "author": search_str_like}).fetchall()
        if not books or len(books) == 0:
            return None
        else:
            return books

    # api to save the review for a book. If a user already has a review for a book, it will return ErrorCodes.Duplicate otherwise it will return ErrorCodes.NoError
    def save_review(self, user_id, isbn, review, created_at):
        try:
            self.db_session.execute(
                "INSERT INTO reviews (book_id, user_id, review, created_at) VALUES (:book_id, :user_id, :review,:created_at)",
                {"book_id": isbn, "user_id": user_id, "review": review, "created_at": created_at})
            self.db_session.commit()
            return ErrorCodes.NoError
        except sqlalchemy.exc.IntegrityError:
            self.db_session.rollback()
            return ErrorCodes.Duplicate

    # api to lookup reviews based on the isbn for a book
    def find_reviews_by_isbn(self, isbn):
        reviews = self.db_session.execute(
            "SELECT book_id, user_id, username, review, reviews.created_at FROM reviews join users on reviews.user_id=users.id and book_id=:id order by reviews.created_at desc",
            {"id": isbn}).fetchall()
        if not reviews or len(reviews) == 0:
            return None
        else:
            return reviews
