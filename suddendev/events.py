import flask
import flask_socketio as fsio
from . import socketio
from .tasks import play_game
from .models import db, GameSetup
from .routes import GLOBAL_DICT
import sqlalchemy

NAMESPACE = '/game-session'
REQUIRED_PLAYER_COUNT = 4

@socketio.on('joined', namespace=NAMESPACE)
def joined(message):
    """Sent by clients when they enter a room."""
    game_id = flask.session.get('game_id')
    fsio.join_room(game_id)

    # TODO: move to database and guard against errors
    player_count = GLOBAL_DICT[game_id]['player_count']
    player_names = GLOBAL_DICT[game_id]['players']

    fsio.emit('player_count', '{\"count\" : ' + str(REQUIRED_PLAYER_COUNT-player_count) + '}', room=game_id, namespace=NAMESPACE)

    # If there are enough players, start the game
    if player_count == REQUIRED_PLAYER_COUNT:
        fsio.emit('game_start', {}, room=game_id, namespace=NAMESPACE)
        result = play_game.delay(game_id, player_names).get()
        fsio.emit('result', result, room=game_id, namespace=NAMESPACE)

@socketio.on('left', namespace=NAMESPACE)
def left(message):
    """Sent by clients when they leave a room."""
    room = flask.session.get('game_id')
    fsio.leave_room(room)
