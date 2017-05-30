import flask
from . import default_config


def create_app(config_filename=None):
    app = flask.Flask(__name__)

    if not config_filename:
        config_filename = default_config.__file__
        if config_filename[-1] == 'c':
            config_filename = config_filename[:-1]

    app.config.from_pyfile(config_filename)

    from suddendev.models import db
    db.init_app(app)

    from suddendev import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from suddendev import socketio
    socketio.init_app(app)

    return app
