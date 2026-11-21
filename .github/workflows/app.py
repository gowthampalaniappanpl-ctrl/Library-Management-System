
from flask import Flask, session, redirect, url_for, request
from database import init_db

from auth import auth_bp
from books import books_bp
from users import users_bp
from catalog import catalog_bp
from circulation import circulation_bp
from fines import fines_bp
from reservations import reservations_bp
from reports import reports_bp

app = Flask(__name__)

app.config["SECRET_KEY"] = "change-this-secret-key"

@app.before_request
def protect_pages():

    public_pages = ["auth.login", "static"]

    if request.endpoint not in public_pages:
        if "user_id" not in session:
            return redirect(url_for("auth.login"))

@app.context_processor
def inject_user():
    return {"current_user": session}

# Register all modules

app.register_blueprint(auth_bp)
app.register_blueprint(books_bp)
app.register_blueprint(users_bp)
app.register_blueprint(catalog_bp)
app.register_blueprint(circulation_bp)
app.register_blueprint(fines_bp)
app.register_blueprint(reservations_bp)
app.register_blueprint(reports_bp)

if __name__ == "__main__":

    init_db()

    app.run(debug=True)
