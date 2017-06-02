import flask
import random
import string
import sqlalchemy
import datetime
import flask_socketio as fsio
from threading import Thread
from . import main
from . import socketio
from .models import db, GameSetup
from .game_instance import GameInstance

# TODO: get rid of and use databases
GLOBAL_DICT = dict()
REQUIRED_PLAYER_COUNT = 4

@main.route('/', methods=['GET', 'POST'])
def index():
    """Landing page."""
    return flask.render_template('index.html')

@main.route('/game', methods=['GET', 'POST'])
def game_page():
    game_id = flask.session.get('game_id', None)
    name = flask.session.get('name', None)

    if game_id is None:
        flask.flash('Invalid game id!')
        return flask.redirect(flask.url_for('.lobby'))

    if name is None:
        flask.flash('You must have a name!')
        return flask.redirect(flask.url_for('.lobby'))

    error = check_room_key(game_id)
    if error:
        flask.flash(error)
        return flask.redirect(flask.url_for('.lobby'))

    joined_game = flask.session.get('joined_game', False)
    if not joined_game:

        # TODO: move to db
        if game_id in GLOBAL_DICT:
            if GLOBAL_DICT[game_id]['player_count'] >= REQUIRED_PLAYER_COUNT:
                flask.flash('Sorry, game room is full. Try a different room.')
                return flask.redirect(flask.url_for('.lobby'))

            GLOBAL_DICT[game_id]['player_count'] += 1
            GLOBAL_DICT[game_id]['players'].append(name)

        else:
            GLOBAL_DICT[game_id] = dict()
            GLOBAL_DICT[game_id]['scripts'] = dict()
            GLOBAL_DICT[game_id]['player_count'] = 1
            GLOBAL_DICT[game_id]['players'] = [name]

        flask.session['joined_game'] = True

    # keep track of names

    return flask.render_template('game.html')

@main.route('/lobby', methods=['GET', 'POST'])
def lobby():
    """
    Contains all currently open rooms, along with a button to instantly connect
    to them.
    """
    if flask.request.method == 'GET':
        # TODO: how to do this better?
        if 'game_id' in flask.session:
            flask.session.pop('game_id')
        if 'joined_game' in flask.session:
            flask.session.pop('joined_game')

    # TODO: filter the database, since it also contains old rooms
    rooms = GameSetup.query.all()

    if flask.request.method == 'POST':

        if flask.request.form['name'] != "":
            flask.session['name'] = flask.request.form['name']
        else:
            flask.session['name'] = 'anon'

        if flask.request.form['submit'] == 'create':
            flask.session['game_id'] = create_room()

        else:
            flask.session['game_id'] = flask.request.form['submit']

        return flask.redirect(flask.url_for('.game_page'))

    return flask.render_template('lobby.html', rooms=rooms)

def create_room():
    """Creates a new chat room and returns the key."""
    # TODO: A safer way of making sure we don't generate duplicate room keys

    def gen_random_string(n):
        return ''.join(random.choice(
            string.ascii_uppercase + string.digits) for _ in range(n))

    while True:
        game_id=gen_random_string(5)
        game = GameSetup(game_id)
        db.session.add(game)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
           continue
        break

    return game_id

def check_room_key(game_id):
    """Check the given room key exists and hasn't expired.
    Returns an error string, or None if the key is ok."""
    game = GameSetup.query.filter_by(game_id=game_id).one_or_none()

    if game is None:
        return "Sorry, that key appears to be invalid. Are you sure it's correct?"

    return None
