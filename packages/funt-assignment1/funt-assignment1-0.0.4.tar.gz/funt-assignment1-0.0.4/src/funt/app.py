from flask import Flask

from . import views
from .model import db, db_file


def create_app():
    app = Flask(__name__)

    app.register_blueprint(views.bp)

    return app


def init_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_file}"
    db.init_app(app)

    with app.app_context():
        db.create_all()
