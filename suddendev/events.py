import flask
import flask_login
import flask_socketio as fsio
import sqlalchemy
from . import socketio, redis
from .models import db, User
from .game_instance import GameInstance
from .tasks import play_game
from .rooms import (
    get_room_of_player,
    get_players_in_room,
    remove_player_from_room,
    get_room_state_json_string,
    set_script,
)

NAMESPACE = '/game-session'

@socketio.on('joined', namespace=NAMESPACE)
def joined(message):
    """Sent by clients when they enter a room."""

    player_id = flask_login.current_user.id
    game_id = get_room_of_player(player_id)

    if game_id is None:
        flask.flash("sorry something isn't quite right... try joining another game")
        return flask.redirect(flask.url_for('.main.lobby'))

    # subscribe client to room broadcasts
    fsio.join_room(game_id)
    update_players(game_id)

@socketio.on('left', namespace=NAMESPACE)
def left(message):
    """Sent by clients when they leave a room."""

    # TODO: need to also account for ungraceful exit
    # - setup a heartbeat?

    player_id = flask_login.current_user.id
    game_id = get_room_of_player(player_id)
    if game_id is not None:
        fsio.leave_room(game_id)
        remove_player_from_room(game_id, player_id)


    if get_players_in_room(game_id) == []:
        # TODO: remove room from redis
        pass
    else:
        # notify players that one has left
        update_players(game_id)

        run_game_if_everyone_ready(game_id)

@socketio.on('submit_code', namespace=NAMESPACE)
def submit_code(message):
    """Sent by clients when submitting code."""

    flask_login.current_user.script = message
    db.session.commit()

    player_id = flask_login.current_user.id
    game_id = get_room_of_player(player_id)

    if game_id is None:
        flask.flash("sorry something isn't quite right... try joining another game")
        return flask.redirect(flask.url_for('.main.lobby'))

    set_script(game_id, player_id, message)
    update_players(game_id)

@socketio.on('test', namespace=NAMESPACE)
def test(message):
    """
    Sent by clients to run a wave that tests their (unsubmitted) code.
    The message contains the player script to use.
    """
    player_id = flask_login.current_user.id
    game_id = get_room_of_player(player_id)
    
    player_jsons = get_players_in_room(game_id)
    player_names = []
    player_scripts = []
    for player in player_jsons:
        player_names.append(player['name'])

        # use the submitted script
        if player['id'] == player_id:
            player_scripts.append(message)
        else:
            player_scripts.append(player['script'])

    # TODO: specify test run in call
    handle = play_game.delay(game_id, player_names, player_scripts)
    result = handle.get()
    fsio.emit('result', result, namespace=NAMESPACE)
    pass

@socketio.on('play', namespace=NAMESPACE)
def play(message):
    """Sent by clients to indicate they are ready to play."""
    player_id = flask_login.current_user.id
    game_id = get_room_of_player(player_id)
    run_game_if_everyone_ready(game_id)


def run_game_if_everyone_ready(game_id):
    player_jsons = get_players_in_room(game_id)
    for player in player_jsons:
        if player['status'] != 'ready':
            update_players(game_id)
            return

    player_names = []
    player_scripts = []
    for player in player_jsons:
        player_names.append(player['name'])
        player_scripts.append(player['scripts'])

    handle = play_game.delay(game_id, player_names, player_scripts)
    result = handle.get()

    fsio.emit('result', result, room=game_id, namespace=NAMESPACE)

def update_players(game_id):
    game_json_string = get_room_state_json_string(game_id)
    print(game_json_string)
    if game_json_string is not None:
        print('sending')
        fsio.emit('update', game_json_string, room=game_id, namespace=NAMESPACE)