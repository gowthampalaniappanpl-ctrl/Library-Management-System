
from datetime import date, timedelta
from flask import Blueprint, render_template
from flask import request, redirect, url_for, flash
from database import get_db, FINE_PER_DAY

circulation_bp = Blueprint(
    "circulation", __name__, url_prefix="/circulation"
)

@circulation_bp.route("/")
def index():

    with get_db() as db:

        loans = db.execute("""
            SELECT loans.*, books.title,
            users.name AS user_name
            FROM loans
            JOIN books ON books.id=loans.book_id
            JOIN users ON users.id=loans.user_id
            ORDER BY loans.id DESC
        """).fetchall()

        users = db.execute("""
            SELECT id,name FROM users
            WHERE role='student'
        """).fetchall()

        books = db.execute("""
            SELECT id,title,available_copies
            FROM books WHERE available_copies > 0
        """).fetchall()

    return render_template(
        "circulation.html",
        loans=loans,
        users=users,
        books=books
    )


@circulation_bp.route("/borrow", methods=["POST"])
def borrow():

    try:
        book_id = int(request.form["book_id"])
        user_id = int(request.form["user_id"])
        days = min(60, max(1, int(request.form.get("days", 14))))

        with get_db() as db:

            book = db.execute("""
                SELECT available_copies
                FROM books WHERE id=?
            """, (book_id,)).fetchone()

            if not book or book["available_copies"] < 1:
                raise ValueError("Book is not available")

            today = date.today()
            due = today + timedelta(days=days)

            db.execute("""
                INSERT INTO loans
                (book_id,user_id,issue_date,due_date)
                VALUES(?,?,?,?)
            """, (
                book_id, user_id,
                today.isoformat(), due.isoformat()
            ))

            db.execute("""
                UPDATE books
                SET available_copies = available_copies - 1
                WHERE id=?
            """, (book_id,))

            db.execute("""
                INSERT INTO notifications(user_id,message)
                VALUES(?,?)
            """, (
                user_id,
                f"Book issued. Return by {due.isoformat()}"
            ))

        flash("Book issued successfully", "success")

    except Exception as e:
        flash(str(e), "error")

    return redirect(url_for("circulation.index"))


@circulation_bp.route("/<int:loan_id>/return", methods=["POST"])
def return_book(loan_id):

    with get_db() as db:

        loan = db.execute("""
            SELECT * FROM loans
            WHERE id=? AND status='borrowed'
        """, (loan_id,)).fetchone()

        if not loan:
            flash("Active loan not found", "error")
            return redirect(url_for("circulation.index"))

        today = date.today()
        due = date.fromisoformat(loan["due_date"])

        overdue_days = max(0, (today - due).days)
        fine = overdue_days * FINE_PER_DAY

        db.execute("""
            UPDATE loans
            SET status='returned', return_date=?
            WHERE id=?
        """, (today.isoformat(), loan_id))

        db.execute("""
            UPDATE books
            SET available_copies=available_copies+1
            WHERE id=?
        """, (loan["book_id"],))

        if fine > 0:
            db.execute("""
                INSERT INTO fines(loan_id,user_id,amount)
                VALUES(?,?,?)
            """, (loan_id, loan["user_id"], fine))

        db.execute("""
            INSERT INTO notifications(user_id,message)
            VALUES(?,?)
        """, (
            loan["user_id"],
            f"Book returned. Fine: Rs. {fine:.2f}"
        ))

    flash(f"Book returned. Fine: Rs. {fine:.2f}", "success")

    return redirect(url_for("circulation.index"))
