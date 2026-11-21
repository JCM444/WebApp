from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)

    from features.identity.models import User
    from features.organization.models import StudySession

    with app.app_context():
        db.create_all()