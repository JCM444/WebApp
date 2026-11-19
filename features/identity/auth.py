from flask import redirect, request, url_for

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

    return redirect(url_for("identity.login"))
