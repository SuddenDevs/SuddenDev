import flask
import os
from .config import Config


def create_app():
    app = flask.Flask(__name__)

    app.config.from_object(os.environ['APP_SETTINGS'])

    from suddendev.models import db
    db.init_app(app)

    from suddendev import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from suddendev import socketio
    socketio.init_app(app)

    from suddendev import celery
    celery.conf.update(app.config)

    return app
