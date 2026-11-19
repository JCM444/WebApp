import secrets

from flask import Blueprint, redirect, render_template, session, url_for
from .studid import create_verification


bp = Blueprint("identity", __name__)

pending_verifications = {}

@bp.route('/login')
def login():
    return render_template("login.html")

@bp.route("/login/start")
def start_login():
    token = secrets.token_urlsafe(32)
    
    verification = create_verification(
        token,
        url_for("identity.callback", _external=True)
)

    pending_verifications[verification["id"]] = token
    session["verification_id"] = verification["id"]

    return redirect(verification["link"])

@bp.route("/login/callback")
def callback():
    return "TODO: callback"
