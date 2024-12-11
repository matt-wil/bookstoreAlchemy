from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    """
    This class represents an Author in the library database.

    Attributes:
        id (int): The unique identifier for the author (primary key).
        name (str): The author's name.
        birth (str): The author's date of birth (optional).
        death (str): The author's date of death (optional).
        books (relationship): A relationship with the Book model, representing
            the books written by this author.

    """
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    birth = db.Column(db.String)
    death = db.Column(db.String)

    books = db.relationship('Book', back_populates='author')

    def __repr__(self):
        """
        Returns a string representation of the Author object for debugging purposes.
        Includes ID, name, birth, and death information.

        :return: str - A formatted string representation of the Author.
        """
        return f"Author(id={self.id}, name={self.name}\n, birth={self.birth}\ndeath={self.death}\n"

    def __str__(self):
        """
        Returns a human-readable string representation of the Author object.
        Includes ID, name, birth, and death information.

        :return: str - A formatted string with Author details for user display.
        """
        return (f"Authors Details: ID={self.id} Name={self.name} Birth={self.birth} Death={self.death}")


class Book(db.Model):
    """
    This class represents a Book in the library database.

    Attributes:
        id (int): The unique identifier for the book (primary key).
        author_id (int): The foreign key referencing the Author ID.
        isbn (str): The International Standard Book Number (ISBN) of the book (optional).
        title (str): The title of the book.
        publication_year (int): The year the book was published.
        author (relationship): A relationship with the Author model, representing
            the author of the book.

    """
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    isbn = db.Column(db.String(13))
    title = db.Column(db.String)
    publication_year = db.Column(db.Integer)

    author = db.relationship('Author', back_populates='books')

    def __repr__(self):
        """
        Returns a string representation of the Book object for debugging purposes.
        Includes ID, author ID, title, publication year, and ISBN information.

        :return: str - A formatted string representation of the Book.
        """
        return f"Book(id={self.id}, author_id={self.author_id}, title={self.title}, publication_year={self.publication_year}, isbn={self.isbn}"

    def __str__(self):
        """
        Returns a human-readable string representation of the Book object.
        Includes ID, author ID, title, publication year, and ISBN information.

        :return: str - A formatted string with Book details for user display.
        """
        return f"Book Details: ID={self.id} Author ID={self.author_id} Title={self.title} Published={self.publication_year} ISBN={self.isbn} "

