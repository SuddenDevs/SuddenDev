import flask
import flask_socketio as fsio
from . import socketio


NAMESPACE = '/chat-session'


@socketio.on('joined', namespace=NAMESPACE)
def joined(message):
    """Sent by clients when they enter a room. """
    fsio.emit('status', {'msg': 'someone has joined!'}, namespace=NAMESPACE)


@socketio.on('text', namespace=NAMESPACE)
def text(message):
    """Sent by a client when the user entered a new message."""
    fsio.emit('message', {'msg': 'someone' + ':' + message['msg']}, namespace=NAMESPACE)


@socketio.on('left', namespace=NAMESPACE)
def left(message):
    """Sent by clients when they leave a room."""
    fsio.emit('status', {'msg': 'somebody' + ' has left the room.'}, namespace=NAMESPACE)

