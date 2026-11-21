
from flask import Blueprint, render_template
from database import get_db

reports_bp = Blueprint("reports", __name__)

@reports_bp.route("/")
def dashboard():

    with get_db() as db:

        stats = {
            "books": db.execute(
                "SELECT COUNT(*) FROM books"
            ).fetchone()[0],

            "copies": db.execute(
                "SELECT COALESCE(SUM(total_copies),0) FROM books"
            ).fetchone()[0],

            "users": db.execute("""
                SELECT COUNT(*) FROM users
                WHERE role='student'
            """).fetchone()[0],

            "borrowed": db.execute("""
                SELECT COUNT(*) FROM loans
                WHERE status='borrowed'
            """).fetchone()[0],

            "overdue": db.execute("""
                SELECT COUNT(*) FROM loans
                WHERE status='borrowed'
                AND due_date < date('now','localtime')
            """).fetchone()[0],

            "unpaid": db.execute("""
                SELECT COALESCE(SUM(amount),0)
                FROM fines WHERE paid=0
            """).fetchone()[0]
        }

        recent = db.execute("""
            SELECT loans.*, books.title,
                   users.name AS user_name
            FROM loans
            JOIN books ON books.id=loans.book_id
            JOIN users ON users.id=loans.user_id
            ORDER BY loans.id DESC
            LIMIT 10
        """).fetchall()

        categories = db.execute("""
            SELECT category, COUNT(*) AS count
            FROM books
            GROUP BY category
            ORDER BY count DESC
        """).fetchall()

    return render_template(
        "dashboard.html",
        stats=stats,
        recent=recent,
        categories=categories
    )
