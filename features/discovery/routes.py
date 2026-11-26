from flask import Blueprint, render_template
from .services import get_all_sessions

bp = Blueprint("discovery", __name__, template_folder="templates")

@bp.get("/sessions")
def index():
    sessions = get_all_sessions()
    return render_template("discovery/discovery.html", sessions=sessions)