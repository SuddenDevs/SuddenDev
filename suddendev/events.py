import flask
import flask_socketio as fsio
from . import socketio


NAMESPACE = '/game-session'


@socketio.on('joined', namespace=NAMESPACE)
def joined(message):
    """Sent by clients when they enter a room. """
    room = flask.session.get('game_id')
    fsio.join_room(room)

@socketio.on('left', namespace=NAMESPACE)
def left(message):
    """Sent by clients when they leave a room."""
    room = flask.session.get('room_key')
    fsio.leave_room(room)
