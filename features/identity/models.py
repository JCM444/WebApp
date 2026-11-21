from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auth_identifier = db.Column(db.String(255), unique=True, nullable=False)
    display_name = db.Column(db.String(100), nullable=True)
