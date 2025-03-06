from flask import Flask

from .config import Config
from .extensions import db, migrate, login_manager
from .routes import main, user, auth
from .models import User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(main)
    app.register_blueprint(user)
    app.register_blueprint(auth, url_prefix='/auth')

    return app