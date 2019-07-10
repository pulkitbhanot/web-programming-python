/* Script to create the required tables
There are 4 tables
1) users table to store the user information post registration, the password stored is a salted hashed password. There is a unique index on the username column
2) books table to store the basic book information as read from the csv file. id for the table maps to the ISBN for the book as 1 book will always have 1 ISBN. There are 2 indexes 1 on title and the other one on author to make the search faster.
3) books_extended table to store the information retrieved from calling the goodreads api's
4) reviews table to store the book reviews. The primary key for the table is book id and user id. This also makes sure that we only have 1 review per user.

For the 4 tables there are 3 columns created_at, updated_at and deleted_at to keep track of different events. Currently only created_at column is used.
*/

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    firstname VARCHAR NOT NULL,
    lastname VARCHAR NOT NULL,
    created_at timestamp NOT NULL,
    updated_at timestamp ,
    deleted_at timestamp 
);

CREATE UNIQUE INDEX username_users_index ON users (username);

CREATE TABLE books (
    id VARCHAR(50) PRIMARY KEY,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year SMALLINT NOT NULL,
    created_at timestamp NOT NULL,
    updated_at timestamp ,
    deleted_at timestamp 
);

CREATE INDEX title_books_index ON books (title);
CREATE INDEX author_books_index ON books (author);

CREATE TABLE books_extended (
    id VARCHAR(50) PRIMARY KEY REFERENCES books(id),
    isbn13 VARCHAR(50),
    goodreads_id INTEGER NOT NULL,
    ratings_count INTEGER NOT NULL DEFAULT 0,
    reviews_count INTEGER NOT NULL DEFAULT 0,
    text_reviews_count INTEGER NOT NULL DEFAULT 0,
    work_ratings_count INTEGER NOT NULL DEFAULT 0,
    work_reviews_count INTEGER NOT NULL DEFAULT 0,
    work_text_reviews_count INTEGER NOT NULL DEFAULT 0,
    average_rating NUMERIC DEFAULT 0.0,
    created_at timestamp NOT NULL,
    updated_at timestamp ,
    deleted_at timestamp 
);

CREATE TABLE reviews (
    book_id VARCHAR(50) REFERENCES books(id),
    user_id SERIAL REFERENCES users(id),
    review VARCHAR,
    created_at timestamp NOT NULL,
    updated_at timestamp ,
    deleted_at timestamp,
    PRIMARY KEY (book_id,user_id) 
);




