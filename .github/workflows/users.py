
from flask import Blueprint, render_template
from flask import request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from database import get_db

users_bp = Blueprint(
    "users", __name__, url_prefix="/users"
)

@users_bp.route("/")
def index():

    with get_db() as db:
        users = db.execute("""
            SELECT id,name,email,phone,role
            FROM users ORDER BY id DESC
        """).fetchall()

    return render_template("users.html", users=users)


@users_bp.route("/add", methods=["POST"])
def add():

    name = request.form["name"].strip()
    email = request.form["email"].strip().lower()
    phone = request.form.get("phone", "")
    role = request.form.get("role", "student")
    password = request.form["password"]

    if role not in ("student", "librarian", "admin"):
        flash("Invalid user role", "error")
        return redirect(url_for("users.index"))

    if not name or not email or len(password) < 6:
        flash("Enter valid details and a 6-character password", "error")
        return redirect(url_for("users.index"))

    try:
        hashed_password = generate_password_hash(password)

        with get_db() as db:
            db.execute("""
                INSERT INTO users
                (name,email,phone,role,password_hash)
                VALUES(?,?,?,?,?)
            """, (
                name, email, phone, role, hashed_password
            ))

        flash("User created successfully", "success")

    except Exception:
        flash("Email already registered", "error")

    return redirect(url_for("users.index"))


@users_bp.route("/<int:user_id>/delete", methods=["POST"])
def delete(user_id):

    if user_id == 1:
        flash("Cannot delete initial administrator", "error")
    else:
        try:
            with get_db() as db:
                db.execute(
                    "DELETE FROM users WHERE id=?",
                    (user_id,)
                )

            flash("User deleted", "success")

        except Exception:
            flash("User has existing library records", "error")

    return redirect(url_for("users.index"))
