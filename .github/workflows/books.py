from flask import Blueprint, render_template
from flask import request, redirect, url_for, flash
from database import get_db

books_bp = Blueprint(
    "books", __name__, url_prefix="/books"
)

@books_bp.route("/")
def index():

    with get_db() as db:
        books = db.execute(
            "SELECT * FROM books ORDER BY id DESC"
        ).fetchall()

    return render_template("books.html", books=books)


@books_bp.route("/add", methods=["POST"])
def add():

    isbn = request.form.get("isbn", "").strip()
    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()
    category = request.form.get("category", "").strip()
    publisher = request.form.get("publisher", "").strip()

    try:
        copies = int(request.form.get("total_copies", 1))

        if not title or not author or copies < 0:
            raise ValueError()

        with get_db() as db:
            db.execute("""
                INSERT INTO books
                (isbn,title,author,category,publisher,
                 total_copies,available_copies)
                VALUES(?,?,?,?,?,?,?)
            """, (
                isbn or None, title, author, category,
                publisher, copies, copies
            ))

        flash("Book added successfully", "success")

    except Exception:
        flash("Invalid details or duplicate ISBN", "error")

    return redirect(url_for("books.index"))


@books_bp.route("/<int:book_id>/delete", methods=["POST"])
def delete(book_id):

    try:
        with get_db() as db:
            db.execute(
                "DELETE FROM books WHERE id=?",
                (book_id,)
            )

        flash("Book deleted successfully", "success")

    except Exception:
        flash("Cannot delete a book with existing records", "error")

    return redirect(url_for("books.index"))
