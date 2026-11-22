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


def require_login():
    if request.endpoint is None or request.endpoint in PUBLIC_ENDPOINTS:
        return

    user_id = session.get("user_id")
    if not user_id or not db.session.get(User, user_id):
        session.clear()
        return redirect(url_for("identity.login"))
