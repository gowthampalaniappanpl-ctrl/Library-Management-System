
from flask import Blueprint, render_template
from flask import redirect, url_for, flash
from database import get_db

fines_bp = Blueprint(
    "fines", __name__, url_prefix="/fines"
)

@fines_bp.route("/")
def index():

    with get_db() as db:

        fines = db.execute("""
            SELECT fines.*,
                   users.name AS user_name,
                   loans.id AS loan_id,
                   books.title
            FROM fines
            JOIN users ON users.id=fines.user_id
            JOIN loans ON loans.id=fines.loan_id
            JOIN books ON books.id=loans.book_id
            ORDER BY fines.id DESC
        """).fetchall()

    return render_template("fines.html", fines=fines)


@fines_bp.route("/<int:fine_id>/pay", methods=["POST"])
def pay(fine_id):

    with get_db() as db:

        result = db.execute("""
            UPDATE fines
            SET paid=1
            WHERE id=? AND paid=0
        """, (fine_id,))

    if result.rowcount:
        flash("Fine payment recorded", "success")
    else:
        flash("Fine already paid or not found", "error")

    return redirect(url_for("fines.index"))
