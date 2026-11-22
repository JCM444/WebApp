import secrets

from flask import Blueprint, redirect, render_template, session, url_for, abort, request
from requests import RequestException

from db import db
from .models import User
from .studid import create_verification, get_verification


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
    verification_id = request.args.get("verificationId")

    # browsercheck
    if not verification_id or verification_id != session.get("verification_id"):
        abort(403)

    token = pending_verifications.get(verification_id)
    if not token:
        abort(400)

    #ask studid
    try:
        result = get_verification(verification_id, token)
    except RequestException:
        abort(502, "studid error.")

    identity = result.get("session")

    # remove used verification tokens
    pending_verifications.pop(verification_id, None)
    session.pop("verification_id", None)

    identifier = identity.get("authIdentifier")
    if not identifier:
        abort(403, "'authIdentifier' fehlt. Keine eindeutige Nutzerzuordnung möglich.")

    if identity.get("entityId") != "https://identity.hwr-berlin.de/idp/shibboleth":
        abort(403, "Nur HWR Berlin erlaubt.")
        
    session.clear()

    user = User.query.filter_by(auth_identifier=identifier).first()
    if not user:
        session["pending_identifier"] = identifier
        return redirect(url_for("identity.register"))

    session["user_id"] = user.id
    return redirect(url_for("index"))

@bp.route("/register", methods=["GET", "POST"])
def register():
    identifier = session.get("pending_identifier")
    if not identifier:
        return redirect(url_for("identity.login"))

    name = request.form.get("display_name", "").strip()[:100]
    if request.method == "GET" or not name:
        return render_template("register.html")

    user = User(auth_identifier=identifier, display_name=name)
    db.session.add(user)
    db.session.commit()

    session.clear()
    session["user_id"] = user.id
    return redirect(url_for("index"))

@bp.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@bp.get("/profile")
def profile():
    user = User.query.filter_by(id=session.get("user_id")).first()
    return render_template("profile.html", user=user)
