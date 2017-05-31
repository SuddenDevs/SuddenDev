import flask
import flask_socketio as fsio
from . import socketio


NAMESPACE = '/game-session'


@socketio.on('joined', namespace=NAMESPACE)
def joined(message):
    """Sent by clients when they enter a room. """
    room = flask.session.get('game_id')
    fsio.join_room(room)
    fsio.emit('status', {'msg': 'someone has joined!'}, namespace=NAMESPACE, room=room)

@socketio.on('text', namespace=NAMESPACE)
def text(message):
    """Sent by a client when the user entered a new message."""
    room = flask.session.get('game_id')
    fsio.emit('message', {'msg': 'someone' + ':' + message['msg']}, namespace=NAMESPACE, room=room)

@socketio.on('left', namespace=NAMESPACE)
def left(message):
    """Sent by clients when they leave a room."""
    room = flask.session.get('room_key')
    fsio.leave_room(room)
    fsio.emit('status', {'msg': 'somebody' + ' has left the room.'}, namespace=NAMESPACE, room=room)
