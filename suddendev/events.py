import flask
import flask_login
import flask_socketio as fsio
import sqlalchemy
from . import socketio, redis
from .models import db, User
from .routes import REQUIRED_PLAYER_COUNT, get_players_in_room # TODO: need to get rid of
from .game_instance import GameInstance
from .tasks import play_game

NAMESPACE = '/game-session'

@socketio.on('joined', namespace=NAMESPACE)
def joined(message):
    """Sent by clients when they enter a room."""
    player_id = flask_login.current_user.id
    game_id = redis.hgetall(player_id)['game_id']
    game_state = redis.hgetall(game_id)
    fsio.join_room(game_id)

    if game_id == 0:
        flask.flash("sorry something isn't quite right... try joining another game")
        return flask.redirect(flask.url_for('.main.lobby'))

    player_count = game_state['player_count']
    players = get_players_in_room(game_id)

    player_names = []
    player_scripts = {}

    for p in players:
        name = redis.hgetall(p)['username']
        player_names.append(name)
        player_scripts[name] = User.query.get(p).script

    # TODO: use json dumps and make less ugly
    fsio.emit('player_count', '{\"count\" : ' + str(REQUIRED_PLAYER_COUNT-int(player_count)) + '}', room=game_id, namespace=NAMESPACE)

    # If there are enough players, start the game
    if int(player_count) == REQUIRED_PLAYER_COUNT:
        fsio.emit('game_start', {}, room=game_id, namespace=NAMESPACE)

        if game_state['result'] == '':
            result = play_game.delay(game_id, player_names, player_scripts)
            result = result.get()
            redis.hset(game_id, 'result', result)
        else:
            result = game_state['result']
        fsio.emit('result', result, room=game_id, namespace=NAMESPACE)

@socketio.on('left', namespace=NAMESPACE)
def left(message):
    """Sent by clients when they leave a room."""
    player_id = flask_login.current_user.id
    game_id = redis.hgetall(player_id)['game_id']
    fsio.leave_room(game_id)

@socketio.on('submit_code', namespace=NAMESPACE)
def submit_code(message):
    flask_login.current_user.script = message
    db.session.commit()
