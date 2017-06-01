import flask
import flask_socketio as fsio
from . import socketio
from .tasks import play_game


NAMESPACE = '/game-session'


@socketio.on('joined', namespace=NAMESPACE)
def joined(message):
    """Sent by clients when they enter a room. """
    room = flask.session.get('game_id')
    fsio.join_room(room)

@socketio.on('startgame', namespace=NAMESPACE)
def start_game(message):
    game_id = flask.session.get('game_id')
    result = play_game.delay(game_id).get()
    fsio.emit('result', result, room=game_id, namespace=NAMESPACE)

@socketio.on('left', namespace=NAMESPACE)
def left(message):
    """Sent by clients when they leave a room."""
    room = flask.session.get('game_id')
    fsio.leave_room(room)
