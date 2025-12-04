from flask import Flask, render_template, request, url_for
import os
import sqlite3

# instantiate the app
app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('bookstore.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_categories():
    conn = get_db_connection()
    categories = conn.execute("SELECT * FROM categories").fetchall()
    conn.close()
    return categories

# set up routes
@app.route('/')
def home():
    return render_template("index.html", categories=get_categories())

@app.route('/category')
def category():
    category_id = request.args.get("categoryId", type=int)
    conn = get_db_connection()
    books = conn.execute(
        "SELECT * FROM books WHERE categoryId = ?",
        (category_id,)
    ).fetchall()
    conn.close()

    return render_template(
        "category.html",
        selectedCategory=category_id,
        categories=get_categories(),
        books=books
    )

# we'll link this for project 2 to an sqlite3 database using flask's get_db() function
@app.route('/search', methods=['POST'])
def search():
    #Link to the search results page.
    term = request.form.get("search", "").strip()
    conn = get_db_connection()
    books = conn.execute(
        "SELECT * FROM books WHERE lower(title) LIKE lower(?)",
        (f"%{term}%",)
    ).fetchall()
    conn.close()

    return render_template(
        "search.html",
        categories=get_categories(),
        books=books,
        term=term
    )

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    conn = get_db_connection()
    book = conn.execute("""
        SELECT books.*, categories.name AS categoryName
        FROM books
        JOIN categories ON categories.id = books.categoryId
        WHERE books.id = ?
    """, (book_id,)).fetchone()
    conn.close()

    return render_template("book_detail.html", book=book, categories = get_categories())

@app.errorhandler(Exception)
def handle_error(e):
    """
    Output any errors - good for debugging.
    """
    return render_template('error.html', error=e) # render the edit template


if __name__ == "__main__":
    app.run(debug = True)
