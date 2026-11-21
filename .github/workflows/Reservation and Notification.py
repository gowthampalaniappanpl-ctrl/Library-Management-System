
from flask import Blueprint, render_template
from flask import request, redirect, url_for, flash
from database import get_db

reservations_bp = Blueprint(
    "reservations", __name__, url_prefix="/reservations"
)

@reservations_bp.route("/")
def index():

    with get_db() as db:

        reservations = db.execute("""
            SELECT reservations.*, books.title,
                   users.name AS user_name
            FROM reservations
            JOIN books ON books.id=reservations.book_id
            JOIN users ON users.id=reservations.user_id
            ORDER BY reservations.id DESC
        """).fetchall()

        books = db.execute(
            "SELECT id,title FROM books"
        ).fetchall()

        users = db.execute("""
            SELECT id,name FROM users
            WHERE role='student'
        """).fetchall()

        notifications = db.execute("""
            SELECT notifications.*, users.name AS user_name
            FROM notifications
            JOIN users ON users.id=notifications.user_id
            ORDER BY notifications.id DESC
        """).fetchall()

    return render_template(
        "reservations.html",
        reservations=reservations,
        books=books,
        users=users,
        notifications=notifications
    )


@reservations_bp.route("/add", methods=["POST"])
def add():

    book_id = request.form["book_id"]
    user_id = request.form["user_id"]

    try:
        with get_db() as db:

            db.execute("""
                INSERT INTO reservations(book_id,user_id)
                VALUES(?,?)
            """, (book_id, user_id))

            db.execute("""
                INSERT INTO notifications(user_id,message)
                VALUES(?,?)
            """, (
                user_id,
                "Your book reservation has been recorded."
            ))

        flash("Reservation created", "success")

    except Exception:
        flash("Reservation failed", "error")

    return redirect(url_for("reservations.index"))


@reservations_bp.route(
    "/<int:reservation_id>/cancel",
    methods=["POST"]
)
def cancel(reservation_id):

    with get_db() as db:

        db.execute("""
            UPDATE reservations
            SET status='cancelled'
            WHERE id=? AND status='waiting'
        """, (reservation_id,))

    flash("Reservation cancelled", "success")

    return redirect(url_for("reservations.index"))


@reservations_bp.route(
    "/notification/<int:notification_id>/read",
    methods=["POST"]
)
def mark_read(notification_id):

    with get_db() as db:

        db.execute("""
            UPDATE notifications
            SET is_read=1 WHERE id=?
        """, (notification_id,))

    return redirect(url_for("reservations.index"))
