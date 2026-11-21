from flask import Blueprint, render_template

bp = Blueprint("discovery", __name__, template_folder="templates")

@bp.get("/sessions")
def index():
    return render_template("discovery/discovery.html")
