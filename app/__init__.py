from flask import Flask

from .config import Config
from .extensions import db, migrate
from .routes import main
from .models import models

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main)

    return app