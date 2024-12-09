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
def authors():
    if request.method == 'GET':
        return render_template('add_author.html')

    if request.method == 'POST':
        name = request.form.get('name')
        birth = request.form.get('birthdate')
        death = request.form.get('date_of_death')

        if not name:
            flash("Name is required!", "error")
            return render_template('add_author.html')

        new_author = Author(name=name, birth=birth, death=death)
        if new_author:
            logging.debug('New Author Created')

        try:
            db.session.add(new_author)
            db.session.commit()
            flash(f"{new_author}", "success")
            return redirect('/add_author')
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "error")
            print(f"Error: {e}")
            logging.debug(e)

    return render_template('add_author.html')


if __name__ == '__main__':
    app.run(debug=True)


# this only needs to be run once
# with app.app_context():
#     db.create_all()
