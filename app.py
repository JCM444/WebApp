from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy

from features.identity.routes import bp as identity_bp
from features.identity.auth import require_login

app = Flask(__name__)

bootstrap = Bootstrap5(app)

app.config.from_mapping(
    SECRET_KEY = 'secret_key_just_for_dev_environment',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db',
)

db = SQLAlchemy(app)

app.register_blueprint(identity_bp)
app.before_request(require_login)

@app.route('/')
def index():
    return render_template("index.html")
