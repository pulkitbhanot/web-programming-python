# Project 1

Web Programming with Python and JavaScript

## SQL tables schema is committed in the file create.sql

There are 4 tables
1) users table to store the user information post registration, the password stored is a salted hashed password. There is a unique index on the username column
2) books table to store the basic book information as read from the csv file. id for the table maps to the ISBN for the book as 1 book will always have 1 ISBN. There are 2 indexes 1 on title and the other one on author to make the search faster.
3) books_extended table to store the information retrieved from calling the goodreads api's
4) reviews table to store the book reviews. The primary key for the table is book id and user id. This also makes sure that we only have 1 review per user.

For the 4 tables there are 3 columns created_at, updated_at and deleted_at to keep track of different events. Currently only created_at column is used.

## import.py

This file contains the code to process the csv file, make calls to the goodreads api and persist the response along with other attributes read from the csv file to db in batched og 100.

## Web application

Supports
- Login and registration of users.
- Search books based on ISBN, author and text and leave reviews for them.
- Has error handling to make sure a user cannot register with the same email multiple times and cannot provide review on the same book multiple times.
- has an api to return a json response for the book queried based on the ISBN
- Does session management across all the pages till a user is logged in. Also, if the user ever explicitly request the index page (/) the session information is cleared.

Code comments are added across individual python files.

## Running the server

The environment variables to run the different parts of the program are in the file .env_setup. Please run `source .env_setup` to setup these variables.

To run the import program just run `python3 import.py`, the output logs are committed alongside in import_logs. For the following 7 ISBN, goodreads didnot return any data

 0385536073
 0061974618
 0440244498
 0743292511
 0084386874
 0380753022
 097496090X

To run the web app just run `flask run`