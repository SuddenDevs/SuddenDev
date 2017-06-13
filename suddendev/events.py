import flask
import flask_login
import flask_socketio as fsio
import sqlalchemy
from . import socketio, redis
from .models import db, User
from .game_instance import GameInstance
from .tasks import play_game, test_round
from .rooms import (
    get_room_of_player,
    get_players_in_room,
    remove_player_from_room,
    get_room_state_json_string,
    set_script,
    set_player_ready,
    all_players_are_ready,
    reset_all_players,
    get_name_of_player,
    remove_room,
    get_room_wave,
    set_room_wave,
)

NAMESPACE = '/game-session'

@socketio.on('joined', namespace=NAMESPACE)
def joined(message):
    """Sent by clients when they enter a room."""

    player_id = flask_login.current_user.id
    game_id = get_room_of_player(player_id)
    if game_id is None:
        flask.flash("sorry something isn't quite right... try joining another game")
        return flask.redirect(flask.url_for('.main.home'))


    # subscribe client to room broadcasts
    fsio.join_room(game_id)
    update_players(game_id)

    player_name = get_name_of_player(player_id)
    if player_name is not None:
        fsio.emit('message_room', player_name + ' has joined!', room=game_id, namespace=NAMESPACE)

@socketio.on('left', namespace=NAMESPACE)
def left(message):
    """Sent by clients when they leave a room."""
    player_id = flask_login.current_user.id
    manage_player_leaves(player_id)

@socketio.on('disconnect', namespace=NAMESPACE)
def disconnect():
    """Received when a client ungracefully leaves a room."""
    player_id = flask_login.current_user.id
    manage_player_leaves(player_id)

@socketio.on('submit', namespace=NAMESPACE)
def submit_code(message):
    """Sent by clients when submitting code."""

    flask_login.current_user.script = message
    db.session.commit()

    player_id = flask_login.current_user.id
    game_id = get_room_of_player(player_id)

    if game_id is None:
        flask.flash("sorry something isn't quite right... try joining another game")
        return flask.redirect(flask.url_for('.main.home'))

    set_script(game_id, player_id, message)
    update_players(game_id)

    player_name = get_name_of_player(player_id)
    if player_name is not None:
        fsio.emit('message_room', player_name + ' has submitted a new script.', room=game_id, namespace=NAMESPACE)

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

    wave = get_room_wave(game_id)
    fsio.emit('message_room', 'Testing against wave ' + str(wave), room=flask.request.sid, namespace=NAMESPACE)
    handle = test_round.delay(game_id, player_names, player_scripts, NAMESPACE, flask.request.sid, wave=wave)
    cleared = handle.get()
    fsio.emit('message_result', 'Test run successfully!', room=flask.request.sid, namespace=NAMESPACE)

@socketio.on('play', namespace=NAMESPACE)
def play(message):
    """Sent by clients to indicate they are ready to play."""

    player_id = flask_login.current_user.id
    game_id = get_room_of_player(player_id)
    set_player_ready(game_id, player_id)

    # TODO: guard against no player entry
    player_name = get_name_of_player(player_id)
    if player_name is not None:
        fsio.emit('message_room', player_name + ' is ready to go!', room=game_id, namespace=NAMESPACE)

    run_game_if_everyone_ready(game_id)

def manage_player_leaves(player_id):
    game_id = get_room_of_player(player_id)

    if game_id is None:
        return 

    fsio.leave_room(game_id)
    remove_player_from_room(game_id, player_id)

    if get_players_in_room(game_id) == []:
        remove_room(game_id)
    else:
        # notify players that one has left
        update_players(game_id)

        player_name = get_name_of_player(player_id)
        if player_name is not None:
            fsio.emit('message_room', player_name + ' has left.', room=game_id, namespace=NAMESPACE)

        run_game_if_everyone_ready(game_id)

def run_game_if_everyone_ready(game_id):
    if all_players_are_ready(game_id):
        player_jsons = get_players_in_room(game_id)
        player_names = []
        player_scripts = []
        for player in player_jsons:
            player_names.append(player['name'])
            player_scripts.append(player['script'])

        fsio.emit('message_room', 'Everyone is ready! Here we go...', room=game_id, namespace=NAMESPACE)
        wave = get_room_wave(game_id)
        handle = play_game.delay(game_id, player_names, player_scripts, NAMESPACE, game_id, wave=1)
        highest_wave = handle.get()
        set_room_wave(game_id, highest_wave + 1)
        fsio.emit('message_result', 'Run complete! You reached wave ' + str(highest_wave), room=game_id, namespace=NAMESPACE)
        reset_all_players(game_id)

def update_players(game_id):
    game_json_string = get_room_state_json_string(game_id)
    if game_json_string is not None:
        fsio.emit('update', game_json_string, room=game_id, namespace=NAMESPACE)
