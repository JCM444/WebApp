from flask import Blueprint, render_template

bp = Blueprint('organization', __name__, template_folder='templates')

@bp.route('/create')
def create_session():
    return render_template('create_session.html')