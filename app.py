from flask import get_flashed_messages, render_template, request, redirect, url_for, flash, session, jsonify
from data_manager.data_models import *


@app.route('/')
def index():
    """
        Get triggered when client sends a request to the endpoint. It stores flash messages and sessions which are sent
        to html page as data for page formatting
    :return:
    """
    try:
        # Queries chatgpt and get the response for books recommendation
        # all_books_title = get_all_books_titles()
        # books_prompt_for_ai = f"Based on the story plot of these books: {all_books_title}, recommend 5 new books for me"
        # response = get_book_suggestion_from_ai(books_prompt_for_ai)
        # response = response.split('\n')
        # response = response[2:]

        # Hard coded response due to external ai api cost constraints
        response = ["Recommendations......................."]

        # Flash messages and session data check returned from different endpoint across the web app
        flash_message = None
        if len(get_flashed_messages()) > 0:
            flash_message = get_flashed_messages()[0]

        search_results = session.pop('search_results', None)

        sorted_results = session.pop('sorted', None)

        titles_and_names_ratings = get_all_book_titles_and_author_names_ratings()
        return render_template('index.html', titles_and_names_ratings=titles_and_names_ratings,
                               flash_message=flash_message, response=response,
                               search_results=search_results, sorted_results=sorted_results)
    except(AttributeError, ValueError, TypeError, FileNotFoundError):
        return render_template('404.html')


@app.route('/add_author', methods=["GET", "POST"])
def add_author():
    """
        Gets triggered when a post request is sent to the endpoint. It adds an author to the database
    :return:
    """
    try:
        if request.method == "POST":
            state = 'post'
            name = request.form["author_name"]
            author = Author(
                id=None,
                name=name,
                birth_date=request.form["birth_date"],
                date_of_death=request.form["death_date"]
            )
            db.session.add(author)
            db.session.commit()
            return render_template('add_author.html', state=state, name=name)
        else:
            state = 'get'
            return render_template('add_author.html', state=state)
    except(AttributeError, ValueError, TypeError, FileNotFoundError,
           sqlalchemy.exc.NoResultFound, sqlalchemy.exc.IntegrityError):
        return render_template('404.html')


@app.route('/add_book', methods=["GET", "POST"])
def add_book():
    """
        Gets triggered when a post request is sent to the endpoint. It adds a book to the database
    :return:
    """
    try:
        if request.method == "POST":
            state = 'post'
            title = request.form["title"]
            book = Book(
                id=None,
                isbn=request.form["isbn"],
                title=title,
                publication_year=request.form["year"],
                author_id=request.form["authors"],
                rating=request.form["rating"]
            )
            db.session.add(book)
            db.session.commit()
            return render_template('add_book.html', state=state, title=title)
        else:
            state = 'get'
            all_users = get_all_authors_name_and_id()
            return render_template('add_book.html', state=state, all_users=all_users)
    except(AttributeError, ValueError, TypeError, FileNotFoundError,
           sqlalchemy.exc.NoResultFound, sqlalchemy.exc.IntegrityError):
        return render_template('404.html')


@app.route('/book/<int:book_id>/delete')
def delete_book(book_id):
    """
        Gets triggered when a request is sent to the endpoint. It deletes a book from the database
    :param book_id:
    :return:
    """
    try:
        all_details = get_all_details(book_id)
        author_id, author_count = get_author_count_and_id(book_id)
        book = db.session.get(Book, book_id)
        author = db.session.get(Author, author_id)

        # checks to delete only book if book author still have some books written by them in the database
        if book and author_count > 1:
            db.session.delete(book)
            db.session.commit()

            # Flash the success message
            flash(f'The book [ {all_details[0]} ] has been deleted successfully.', 'success')
            return redirect(url_for('index'))

        # checks to delete book and author if book author doesn't have any other books written by them in the database
        elif book and author_count == 1:
            db.session.delete(book)
            db.session.delete(author)
            db.session.commit()
            # Flash the success message
            flash(f'The book [ {all_details[0]} ] and author [ {all_details[4]} ] have been deleted successfully.', 'success')
            return redirect(url_for('index'))
    except(AttributeError, ValueError, TypeError, FileNotFoundError,
           sqlalchemy.exc.NoResultFound, sqlalchemy.exc.IntegrityError):
        return render_template('404.html')


@app.route('/author/<int:author_id>/delete')
def delete_author(author_id):
    """
        Get triggered when the client sends a request to the endpoint. Deletes author and all books in the database
        written by the author
    :param author_id:
    :return:
    """
    try:
        author = db.session.get(Author, author_id)
        name = author.name
        db.session.delete(author)
        book_ids = get_book_ids_from_author_id(author_id)
        for book_id in book_ids:
            book = db.session.get(Book, book_id[0])
            db.session.delete(book)
        db.session.commit()
        flash(f'The Author [ {name} ] and all their books have been deleted successfully.', 'success')
        return redirect(url_for('index'))
    except(AttributeError, ValueError, TypeError, FileNotFoundError,
           sqlalchemy.exc.NoResultFound, sqlalchemy.exc.IntegrityError):
        return render_template('404.html')


@app.route('/book_details/<int:book_id>')
def book_details(book_id):
    """
        Get triggered when the client sends a request to the endpoint. Displays details information of book ans its author
    :param book_id:
    :return:
    """
    try:
        all_details = get_all_details(book_id)
        return render_template('book_details.html', all_details=all_details)
    except(AttributeError, ValueError, TypeError, FileNotFoundError):
        return render_template('404.html')

@app.route('/search')
def search():
    """
        Get triggered when the client sends a request to the endpoint. Returns a list of books that matches the
        queried term
    :return:
    """
    try:
        matching_titles_and_name = []
        all_titles_and_names = get_all_book_titles_and_author_names_ratings()
        search_keyword = request.args.get('search_result')

        for book_and_title in all_titles_and_names:
            if search_keyword in book_and_title[0] or search_keyword in book_and_title[1]:
                book_and_title_dict = {
                    'title': book_and_title[0],
                    'author': book_and_title[1],
                    'rating': book_and_title[2],
                    'book_id': book_and_title[3],
                    'author_id': book_and_title[4]
                }
                matching_titles_and_name.append(book_and_title_dict)
        if not matching_titles_and_name:
            flash(f'Your search doesn\'t match any record', 'success')
            return redirect(url_for('index'))
        else:
            session['search_results'] = matching_titles_and_name
            return redirect(url_for('index'))
    except(AttributeError, ValueError, TypeError, FileNotFoundError):
        return render_template('404.html')


@app.route('/sorting')
def sort_by_book_title_or_name():
    """
        Get triggered when client sends a request to the endpoint. It returns book data after sorting either by
        book title or by book name
    :return:
    """
    try:
        matching_titles_and_name = []
        all_titles_and_names = get_all_book_titles_and_author_names_ratings()
        for book_and_title in all_titles_and_names:
            book_and_title_dict = {
                'title': book_and_title[0],
                'author': book_and_title[1],
                'rating': book_and_title[2],
                'book_id': book_and_title[3],
                'author_id': book_and_title[4]
            }
            matching_titles_and_name.append(book_and_title_dict)

        sort = request.args.get('sort')
        if sort == 'title':
            sorted_books = sorted(matching_titles_and_name, key=lambda x: x['title'])
            session['sorted'] = sorted_books
            return redirect(url_for('index'))
        elif sort == 'author':
            sorted_books = sorted(matching_titles_and_name, key=lambda x: x['author'])
            session['sorted'] = sorted_books
            return redirect(url_for('index'))
    except(AttributeError, ValueError, TypeError, FileNotFoundError):
        return render_template('404.html')


@app.errorhandler(404)
def page_not_found(error):
    """
        Handles 404 error when it is triggered by client
    :param error:
    :return:
    """
    return render_template('404.html'), 404


@app.errorhandler(400)
def page_not_found(error):
    """
        Handles 400 error when it is triggered by client
    :param error:
    :return:
    """
    return jsonify({"error": "Not Found"}), 400


@app.errorhandler(500)
def internal_server_error(error):
    """
        Handles 500 error when it is triggered by client
    :param error:
    :return:
    """
    return jsonify({"error": "Not Found"}), 500


@app.errorhandler(405)
def internal_server_error(error):
    """
        Handles 405 error when triggered by client
    :param error:
    :return:
    """
    return jsonify({"error": "Not Found"}), 405


if __name__ == "__main__":
    # Launch the Flask dev server
    app.run(host="0.0.0.0", port=5000, debug=True)
