import secrets

from flask import Blueprint, redirect, render_template, session, url_for, abort, request
from requests import RequestException

from db import db
from .auth import current_user, login_user
from .forms import DisplayNameForm
from .models import User
from .studid import create_verification, get_verification


bp = Blueprint("identity", __name__, template_folder="templates")

@bp.route('/login')
def login():
    return render_template("identity/login.html")

@bp.route("/login/start")
def start_login():
    token = secrets.token_urlsafe(32)
    
    verification = create_verification(
        token,
        url_for("identity.callback", _external=True)
)

    session["verification_id"] = verification["id"]
    session["verification_token"] = token

    return redirect(verification["link"])

@bp.route("/login/callback")
def callback():
    verification_id = request.args.get("verificationId")

    # browsercheck
    if not verification_id or verification_id != session.get("verification_id"):
        abort(403)

    #ask studid
    try:
        result = get_verification(verification_id, session["verification_token"])
    except RequestException:
        abort(502, "studid error.")

    identity = result.get("session")

    # remove used verification tokens
    session.pop("verification_id", None)
    session.pop("verification_token", None)

    identifier = identity.get("authIdentifier")
    if not identifier:
        abort(403, "'authIdentifier' fehlt. Keine eindeutige Nutzerzuordnung möglich.")

    if identity.get("entityId") != "https://identity.hwr-berlin.de/idp/shibboleth":
        abort(403, "Nur HWR Berlin erlaubt.")
        
    user = db.session.execute(db.select(User).filter_by(auth_identifier=identifier)).scalar_one_or_none()
    if not user:
        session.clear()
        session["pending_identifier"] = identifier
        return redirect(url_for("identity.register"))

    login_user(user)
    return redirect(url_for("index"))

@bp.route("/register", methods=["GET", "POST"])
def register():
    identifier = session.get("pending_identifier")
    if not identifier:
        return redirect(url_for("identity.login"))

    form = DisplayNameForm()
    if not form.validate_on_submit():
        return render_template("identity/register.html", form=form)

    user = User(auth_identifier=identifier, display_name=form.display_name.data.strip())
    db.session.add(user)
    db.session.commit()

    login_user(user)
    return redirect(url_for("index"))

@bp.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@bp.route("/profile", methods=["GET", "POST"])
def profile():
    user = current_user()

    form = DisplayNameForm(obj=user)
    form.submit.label.text = "Speichern"
    if form.validate_on_submit():
        user.display_name = form.display_name.data.strip()
        db.session.commit()
        return redirect(url_for("identity.profile"))

    return render_template("identity/profile.html", user=user, form=form)
