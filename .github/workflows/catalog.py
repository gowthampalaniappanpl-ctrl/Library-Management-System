
from flask import Blueprint, render_template, request
from database import get_db

catalog_bp = Blueprint(
    "catalog", __name__, url_prefix="/catalog"
)

@catalog_bp.route("/")
def index():

    search = request.args.get("q", "").strip()

    with get_db() as db:

        books = db.execute("""
            SELECT * FROM books
            WHERE title LIKE ?
            OR author LIKE ?
            OR isbn LIKE ?
            OR category LIKE ?
            ORDER BY title
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        )).fetchall()

    return render_template(
        "catalog.html",
        books=books,
        q=search
    )
