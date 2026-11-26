from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect
from db import init_db

from features.identity.routes import bp as identity_bp
from features.identity.auth import require_login
from features.discovery.routes import bp as discovery_bp
from features.organization.routes import bp as organization_bp

app = Flask(__name__)

Bootstrap5(app)
CSRFProtect(app)

app.config.from_mapping(
    SECRET_KEY = 'secret_key_just_for_dev_environment',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db',
)

init_db(app)

app.register_blueprint(identity_bp)
app.register_blueprint(discovery_bp)
app.register_blueprint(organization_bp)

app.before_request(require_login)

@app.route('/')
def index():
    return render_template("index.html")
