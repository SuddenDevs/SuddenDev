import flask
import random
import string
import sqlalchemy
import datetime
import flask_socketio as fsio
from threading import Thread
from . import main
from . import socketio
from .tasks import play_game
from .models import db, GameController
from .game_instance import GameInstance

@main.route('/', methods=['GET', 'POST'])
def index():
    """Landing page."""
    return flask.render_template('index.html')

@main.route('/game', methods=['GET', 'POST'])
def game_page():
    user_game_id = flask.session.get('game_id', None)

    if user_game_id is None:
        flask.flash('Invalid game id!')
        return flask.redirect(flask.url_for('.lobby'))

    error = check_room_key(user_game_id)
    if error:
        flask.flash(error)
        return flask.redirect(flask.url_for('.lobby'))

    return flask.render_template('game.html')

@main.route('/lobby', methods=['GET', 'POST'])
def lobby():
    """
    Contains all currently open rooms, along with a button to instantly connect
    to them.
    """
    if flask.request.method == 'GET':
        if 'game_id' in flask.session:
            flask.session.pop('game_id')

    # TODO: filter the database, since it also contains old rooms
    rooms = GameController.query.all()

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
        game = GameController(game_id)
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
    game = GameController.query.filter_by(game_id=game_id).one_or_none()

    if game is None:
        return "Sorry, that key appears to be invalid. Are you sure it's correct?"

    return None
