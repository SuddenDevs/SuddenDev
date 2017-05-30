# Better expose our create_app method.
from .factory import create_app

# Create a global socketio instance which is linked to the app
# in create_app() and is ultimately used to run the app via
# socketio.run(app).
from flask_socketio import SocketIO
socketio = SocketIO()

# Create our main blueprint, used by our routes and events
# which is registered to the app in create_app().
# We're using a blueprint so we can keep app creation seperated
# from the rest of the codebase.
# Not intended for user use.
from flask import Blueprint
main = Blueprint('main', __name__)

from . import routes, events
