# Better expose our create_app method.
from .factory import create_app

# Need to access config for creating components
from .config import Config

# Create a global socketio instance which is linked to the app
# in create_app() and is ultimately used to run the app via
# socketio.run(app).
from flask_socketio import SocketIO
socketio = SocketIO()

# As above for celery
from celery import Celery
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)

# Create our main blueprint, used by our routes and events
# which is registered to the app in create_app().
# We're using a blueprint so we can keep app creation seperated
# from the rest of the codebase.
# Not intended for user use.
from flask import Blueprint
main = Blueprint('main', __name__)

from flask_login import LoginManager
login_manager = LoginManager()

from redis import StrictRedis
redis = StrictRedis.from_url(Config.REDIS_URL, decode_responses=True, charset="utf-8",
        max_connections=Config.REDIS_CONNECTION_MAX)

from . import routes, events
