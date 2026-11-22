from flask import redirect, request, url_for, session

from db import db
from .models import User

PUBLIC_ENDPOINTS = {
  "index",
  "identity.login",
  "identity.start_login",
  "identity.callback",
  "identity.register",
  "static"
}


def current_user():
    user_id = session.get("user_id")
    return db.session.get(User, user_id) if user_id else None


def login_user(user):
    session.clear()
    session["user_id"] = user.id


def require_login():
    if request.endpoint is None or request.endpoint in PUBLIC_ENDPOINTS:
        return

    if not current_user():
        session.clear()
        return redirect(url_for("identity.login"))
