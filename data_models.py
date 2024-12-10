from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    birth = db.Column(db.String)
    death = db.Column(db.String)

    books = db.relationship('Book', back_populates='author')

    def __repr__(self):
        return f"Author(id={self.id}, name={self.name}\n, birth={self.birth}\ndeath={self.death}\n"

    def __str__(self):
        return (f"Authors Details: ID={self.id} Name={self.name} Birth={self.birth} Death={self.death}")


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    isbn = db.Column(db.String(13))
    title = db.Column(db.String)
    publication_year = db.Column(db.Integer)

    author = db.relationship('Author', back_populates='books')

    def __repr__(self):
        return f"Book(id={self.id}, author_id={self.author_id}, title={self.title}, publication_year={self.publication_year}, isbn={self.isbn}"

    def __str__(self):
        return f"Book Details\nID: {self.id}\nAuthor ID: {self.author_id}\nTitle: {self.title}\nPublished in {self.publication_year}\nISBN: {self.isbn}\n"

