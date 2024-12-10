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

    if request.method == 'POST':
        title = request.form.get('title')
        year_published = request.form.get('year_of_publication')
        # Implement API to retrieve the ISBN from the title
        isbn = request.form.get('isbn')
        author_name = request.form.get('drop-authors')
        author = Author.query.filter_by(name=author_name).first()

        if not title and year_published:
            flash("Title and year of publication are required!", "error")
            return redirect('/add_book')
        if author:
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
    render_template()


if __name__ == '__main__':
    app.run(debug=True)


# this only needs to be run once
# with app.app_context():
#     db.create_all()
