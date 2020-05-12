import csv
import os
import requests
import sys
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime

'''
class to import a list of books into the database. For each of the book specified in the csv file a get request is made to the goodreads api to get some extra attributes for the book.
if the goodreads api doesnot return a response the book record is still processed. In UI and in the api response those attributes are not displayed/returned.

Additionally the records are committed in batches of size 100.
'''

# get the database url from the environment variable
database_url = os.getenv("DATABASE_URL")

if not database_url:
    print >> sys.stderr, "Environment variable DATABASE_URL is not set."
    sys.exit(1)

# get the GOODREADS_API_KEY from the environment variable
goodreads_api_key = os.getenv("GOODREADS_API_KEY")
if not goodreads_api_key:
    print >> sys.stderr, "Environment variable GOODREADS_API_KEY is not set."
    sys.exit(1)

engine = create_engine(database_url)
db = scoped_session(sessionmaker(bind=engine))


# api to retrieve data from goodreads api, it returns None of the api returned a not ok status
def get_goodreads_data(key, isbn):
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": key, "isbns": isbn})

    if res.status_code == requests.codes.ok:
        return res
    else:
        print(f" Data couldnot been retrieved from Goodreads for {isbn} will return None")
    return None


# main function to read a csv file with the different book attributes that makes a call to goodreads api to pulling in additional attributes for the book
def main():
    f = open("books.csv")
    reader = csv.reader(f)
    created_at = datetime.now()
    next(reader)  # skip the header line
    batch_size = 100  # set the batch size to 100, i.e commit after every 100 records from the CSV
    counter = 0;
    for isbn, title, author, year in reader:
        print(f"processing book isbn {isbn} title {title} author {author} year {year}.")
        db.execute(
            "INSERT INTO books (id, title, author, year, created_at) VALUES (:id, :title, :author, :year, :created_at)",
            {"id": isbn, "title": title, "author": author, "year": year, "created_at": created_at})
        counter += 1
        res = get_goodreads_data(goodreads_api_key, isbn)
        if res:
            try:
                api_resp_obj = res.json()['books'][0]
                db.execute(
                    "INSERT INTO books_extended (id ,isbn13,goodreads_id,ratings_count,reviews_count,text_reviews_count,work_ratings_count,work_reviews_count,work_text_reviews_count,average_rating,created_at) VALUES (:id ,:isbn13,:goodreads_id,:ratings_count,:reviews_count,:text_reviews_count,:work_ratings_count,:work_reviews_count,:work_text_reviews_count,:average_rating,:created_at)",
                    {"id": isbn, "isbn13": api_resp_obj['isbn13'],
                     "goodreads_id": api_resp_obj['id'], "ratings_count": api_resp_obj['ratings_count'],
                     "reviews_count": api_resp_obj['reviews_count'],
                     "text_reviews_count": api_resp_obj['text_reviews_count'],
                     "work_ratings_count": api_resp_obj['work_ratings_count'],
                     "work_reviews_count": api_resp_obj['work_reviews_count'],
                     "work_text_reviews_count": api_resp_obj['work_text_reviews_count'],
                     "average_rating": api_resp_obj['average_rating'], "created_at": created_at})
            except:
                print(f"Unexpected error when processing {isbn} with {api_resp_obj}:", sys.exc_info()[0])
        else:
            print(f" Not added entry to books_extended table for {isbn}.")

        if counter % batch_size == 0:
            print(f"Flushing next batch of records to DB, total records processed post commit {counter}")
            db.commit()
    db.commit()


if __name__ == "__main__":
    main()
