import os
from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book
from dotenv import load_dotenv
import logging

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.sqlite'
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')

db.init_app(app)
logging.basicConfig(filename='flask_debug.log', level=logging.DEBUG)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    Route handler for adding a new author to the database

    - Handles both GET and POST requests
    - On POST:
        - Extracts author information from the form
        - Validates that the name is not empty
        - Creates a new Author object
        - Logs the creation of the new author (debug level)
        - Adds the author to the database session and commits the changes
        - Flashes a success message if successful
        - Redirects back to the add_author page
        - Flashes an error message and rolls back the session on any exception
    - On GET:
        - Renders the add_author.html template
    """
    if request.method == 'POST':
        name = request.form.get('name')
        birth = request.form.get('birthdate')
        death = request.form.get('date_of_death')

        if not name:
            flash("Name is required!", "error")
            return redirect('/add_author')

        new_author = Author(name=name, birth=birth, death=death)
        if new_author:
            logging.debug(f'New Author Created\n{new_author}\n')

        try:
            db.session.add(new_author)
            db.session.commit()
            flash(f"{new_author}", "success")
            return redirect('/add_author')
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "error")
            print(f"Error: {e}")
            logging.debug(f"{e}\n")

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Route handler for adding a new book to the database

    - Handles both GET and POST requests
    - On POST:
        - Extracts book information from the form
        - Validates that title and year_published are not empty
        - Creates a new Book object
        - Logs the creation of the new book (debug level)
        - Adds the book to the database session and commits the changes
        - Flashes a success message if successful
    - On GET:
        - Queries all authors and stores them in a variable
        - Renders the add_book.html template with the list of authors
    """
    if request.method == 'POST':
        title = request.form.get('title')
        year_published = request.form.get('year_of_publication')
        # V2 --Implement WorldCat API to retrieve the ISBN from the title
        isbn = request.form.get('isbn')
        author = request.form.get('drop-authors')
        if not title and year_published:
            flash("Title and year of publication are required!", "error")
            return redirect('/add_book')

        new_book = Book(title=title, isbn=isbn, publication_year=year_published, author_id=author)
        if new_book:
            logging.debug(f"New Book Created\n{new_book}\n")
        try:
            db.session.add(new_book)
            db.session.commit()
            flash(f"{new_book}", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "error")
            print(f"Error: {e}")
            logging.debug(f"{e}\n")

    db_authors = Author.query.all()
    return render_template('add_book.html', authors=db_authors)


@app.route('/', methods=['GET'])
def home():
    """
    Renders the home page, displaying all books and their authors with sorting functionality.

    - Retrieves the sorting criteria (`sort_by`) from the query string (defaults to 'title').
    - Queries the database for all books, optionally sorting them by title or by author name
      using the relationship between Book and Author models.
    - Passes the sorted list of books to the `home.html` template for rendering.

    :return: The rendered home.html template with sorted book data.
    """
    # V2 -- Implement Pagination
    # V2 -- Implement API to retrieve Book Covers for HTML
    sort_by = request.args.get("sort_by", "title")
    query = request.args.get("query", "")
    if query:
        books = Book.query.filter(Book.title.ilike(f"%{query}%")).all()
    else:
        if sort_by == "title":
            books = Book.query.order_by(Book.title).all()
        elif sort_by == "author":
            books = Book.query.order_by(Author.name).join(Book.author).all()
        else:
            books = Book.query.all()
    return render_template('home.html', books=books)


if __name__ == '__main__':
    app.run(debug=True)


# this only needs to be run once
# with app.app_context():
#     db.create_all()
