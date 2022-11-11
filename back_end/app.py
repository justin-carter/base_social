import sys

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from back_end.models.models import db
from back_end.routes.api import api_bp


app = Flask(__name__)
jwt = JWTManager(app)

app.config.from_pyfile('config.py')

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(api_bp, url_prefix='/api')

