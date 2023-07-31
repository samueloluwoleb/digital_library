import sqlalchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from data_manager.ai_book_recommendation import *
from config import config
import os

# create the extension
db = SQLAlchemy()

# Initialize flask app and set some parameters value
app = Flask(__name__, instance_relative_config=False,
            template_folder=os.path.join(os.path.dirname(__file__), '../templates'),
            static_folder=os.path.join(os.path.dirname(__file__), '../static'))

# initialize the app with the extension
app.config.from_object(config)
db.init_app(app)


class Author(db.Model):
    """
        Maps to author table in the database and instance properties initialized as column fields
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    birth_date = db.Column(db.String, nullable=False)
    date_of_death = db.Column(db.String)

    def __repr__(self):
        return f"Author(Author id: = {self.id}, Author name: = {self.name})"

    def __str__(self):
        return f"Author name: {self.name}, Author id: {self.id}"


class Book(db.Model):
    """
        Maps to books table in the database and instance properties initialized as column fields
    """
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    isbn = db.Column(db.String, unique=True)
    title = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer)

    def __repr__(self):
        return f"Book(Book id: = {self.id}, Book title: = {self.title})"

    def __str__(self):
        return f"Book title: {self.title}, Book id: {self.id}"


with app.app_context():
    db.create_all()


def get_all_authors_name_and_id():
    """
        Returns the selected query data and used to populate the Authors dropdown list on Add Book page
    :return:
    """
    try:
        all_authors_result = db.session.execute(db.select(Author.name, Author.id)).all()
        return all_authors_result
    except(sqlalchemy.exc.NoResultFound, sqlalchemy.exc.IntegrityError):
        return []


def get_all_book_titles_and_author_names_ratings():
    """
        Returns the selected all query data
    :return:
    """
    try:
        all_titles_and_names_ratings = db.session.execute(
            db.select(Book.title, Author.name, Book.rating, Book.id, Author.id).
            join(Author, Book.author_id == Author.id)).all()
        return all_titles_and_names_ratings
    except(sqlalchemy.exc.NoResultFound, sqlalchemy.exc.IntegrityError):
        return []


def get_all_details(book_id):
    """
        Returns the query data that matches the sql condition of provided book_id
    :param book_id:
    :return:
    """
    try:
        all_details = db.session.execute(db.select(Book.title, Book.isbn, Book.publication_year,
                                                   Book.rating, Author.name, Author.birth_date, Author.date_of_death).join
                                         (Author, Book.author_id == Author.id).where(Book.id == book_id)).one()
        return all_details
    except(sqlalchemy.exc.NoResultFound, sqlalchemy.exc.IntegrityError):
        return []


def get_author_count_and_id(book_id):
    """
        Returns the query data that matches the sql condition of provided book_id
    :param book_id:
    :return:
    """
    try:
        author_id = db.session.execute(db.session.query(Book.author_id).where(Book.id == book_id)).one()
        author_id = author_id[0]
        author_count = db.session.execute(db.session.query(func.count(Book.author_id)).where
                                          (Book.author_id == author_id)).one()
        author_count = author_count[0]
        return author_id, author_count
    except(sqlalchemy.exc.NoResultFound, sqlalchemy.exc.IntegrityError):
        return []


def get_book_ids_from_author_id(author_id):
    """
        Returns the query data that matches the sql condition of provided author_id
    :param author_id:
    :return:
    """
    try:
        book_ids = db.session.execute(db.session.query(Book.id).where(Book.author_id == author_id)).all()
        return book_ids
    except(sqlalchemy.exc.NoResultFound, sqlalchemy.exc.IntegrityError):
        return []


def get_all_books_titles():
    """
        Returns the query data that matches the sql condition
    :return:
    """
    try:
        all_books_list = []
        all_books_title = db.session.execute(db.select(Book.title)).all()
        for book_title in all_books_title:
            all_books_list.append(book_title[0])
        titles = ', '.join(all_books_list)
        return titles
    except(sqlalchemy.exc.NoResultFound, sqlalchemy.exc.IntegrityError):
        return []



