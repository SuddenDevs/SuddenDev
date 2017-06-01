import flask
import flask_socketio as fsio
from . import socketio
from .tasks import play_game
from .models import db, GameController
import sqlalchemy

NAMESPACE = '/game-session'
REQUIRED_PLAYER_COUNT = 4

@socketio.on('joined', namespace=NAMESPACE)
def joined(message):
    """Sent by clients when they enter a room."""
    game_id = flask.session.get('game_id')
    fsio.join_room(game_id)
    game = GameController.query.filter_by(game_id=game_id).one_or_none()
    game.player_count += 1
    db.session.commit()
    fsio.emit('player_count', '{\"count\" : ' + str(REQUIRED_PLAYER_COUNT-game.player_count) + '}', room=game_id, namespace=NAMESPACE)

    # If there are enough players, start the game
    if game.player_count == REQUIRED_PLAYER_COUNT:
        fsio.emit('game_start', {}, room=game_id, namespace=NAMESPACE)
        result = play_game.delay(game_id).get()
        fsio.emit('result', result, room=game_id, namespace=NAMESPACE)

@socketio.on('left', namespace=NAMESPACE)
def left(message):
    """Sent by clients when they leave a room."""
    room = flask.session.get('game_id')
    fsio.leave_room(room)
