import flask
import random
import string
import sqlalchemy
import datetime
from . import main
from .forms import CreateGameForm
from .models import db, GameController
from .game_instance import GameInstance
import flask_socketio as fsio
from threading import Thread
from . import socketio

# TODO: deal with pranksters setting up multiple pranks

@main.route('/', methods=['GET', 'POST'])
def index():
    """Landing page."""
    return flask.redirect(flask.url_for('.lobby'))

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

@main.route('/game_create', methods=['GET', 'POST'])
def game_create():
    form = CreateGameForm()
    if form.validate_on_submit():
            game_id = create_room()
            flask.session['game_id'] = game_id
            return flask.redirect(flask.url_for('.game_page'))
    else:
        return flask.render_template('game_create.html', form=form)

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
        flask.session['game_id'] = flask.request.form['game_id']
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

        # game = GameInstance(game_id, flask.current_app._get_current_object())
        # thread = Thread(target = game.run)
        # thread.start()
       
        return game_id

def check_room_key(game_id):
    """Check the given room key exists and hasn't expired.
    Returns an error string, or None if the key is ok."""
    game = GameController.query.filter_by(game_id=game_id).one_or_none()

    if game is None:
        return "Sorry, that key appears to be invalid. Are you sure it's correct?"

    return None
