from db import db

class StudySession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    # zurückgestellt bis user model fertig ist
    # organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    location = db.Column(db.String(200), nullable=True)
    max_participants = db.Column(db.Integer, nullable=False)
    cancelled_at = db.Column(db.DateTime, nullable=True)
