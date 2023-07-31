# The Book Library project


## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Application Structure](#application-structure)
* [Core Functionalities](#core-functionalities)

## General info
Library App project is a full-featured, dynamic web application that allows user to query for any book,
from a list of books stored in the library database and display the book to the user, user is able to 
sort books either by book title or author name. They are also able to add new book to the library, add author, delete author etc


## Technologies
Project is created with:
* Python
* Html 5
* CSS
* Flask
* API (chatgpt)
	
## Application Structure
The Book Library application will consist of several key parts:
* User Interface (UI): An intuitive web interface built using Flask, HTML, and CSS. It provides forms for adding books and author as well as querying books and also display recommendations from an LLM API
* Data Management: A Python file to handle operations related to the sqlite data source. This file exposes functions for listing all books, adding an author, and adding a book
* Persistent Storage: An sqlite database file to store user and movie data. This file will act as the database for the application.

## Core Functionalities

The core functionalities of the Library application will include:
* Add an author: Use of form to get book info from user and update database with the info
* Add a book: Use of form to get author info from user and update database with the info
* Delete a book: Remove a book from the database.
* Delete an author: Remove an author from the database.
* List all books: View all the books title and author name stored in library database on homepage.
* Data Source Management: Python file is used to manage interactions with the sql data source.