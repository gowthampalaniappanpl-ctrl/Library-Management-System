
from flask import Blueprint, render_template, request
from flask import redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from database import get_db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        identity = request.form["identity"].strip()
        password = request.form["password"]

        with get_db() as db:
            user = db.execute("""
                SELECT * FROM users
                WHERE email=? OR name=?
            """, (identity, identity)).fetchone()

        if user and check_password_hash(
            user["password_hash"], password
        ):
            session.clear()
            session["user_id"] = user["id"]
            session["name"] = user["name"]
            session["role"] = user["role"]

            return redirect(url_for("reports.dashboard"))

        flash("Invalid login details", "error")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully", "success")

    return redirect(url_for("auth.login"))
