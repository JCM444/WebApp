from flask import redirect, request, url_for, session

PUBLIC_ENDPOINTS = {
  "index",
  "identity.login",
  "identity.start_login",
  "identity.callback",
  "static"
}


def require_login():
    if request.endpoint is None or request.endpoint in PUBLIC_ENDPOINTS:
        return

    if not session.get("authenticated"):
        return redirect(url_for("identity.login"))
