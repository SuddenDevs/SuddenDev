import flask
import random
import string
import sqlalchemy
import datetime
from . import main
from .forms import EnterChatForm, SetupChatForm, CreateGameForm
from .models import db, GameController
from .game_instance import GameInstance
import flask_socketio as fsio
from threading import Thread
from . import socketio

# TODO: deal with pranksters setting up multiple pranks

@main.route('/', methods=['GET', 'POST'])
def index():
    """Landing page. Includes form for joining a chat session."""
    form = EnterChatForm()
    if form.validate_on_submit():
        flask.session['game_id'] = form.key.data
        return flask.redirect(flask.url_for('.victim_chat'))

    elif flask.request.method == 'GET':
        form.key.data = flask.session.get('game_id', '')
    return flask.render_template('index.html', form=form)

@main.route('/game', methods=['GET', 'POST'])
def game_page():
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

@main.route('/chat')
def victim_chat():
    """Checks for a valid room key and victim flag in session.
    Redirects back to index if key is invalid or expired, and back to
    to homepage with an error. Otherwise, serves the chat page."""

    # check the prankster isn't on the wrong page
    victim_flag = flask.session.get('victim', False)
    if not victim_flag:
        return flask.redirect(flask.url_for('.prankster_chat'))  # TODO: notify them?

    # check the user *has* a room key
    user_game_id = flask.session.get('game_id', None)
    if user_game_id is None:
        flask.flash('Invalid game id!')
        return flask.redirect(flask.url_for('.index'), form=EnterChatForm())

    # check the user has a valid room key
    error = check_room_key(user_game_id)
    if error:
        flask.flash(error)
        return flask.redirect(flask.url_for('.index'), form=EnterChatForm())

    return flask.render_template('victim_chat.html')

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
        return victim_chat()

    return flask.render_template('lobby.html', rooms=rooms)

@main.route('/itsaprankbro', methods=['GET', 'POST'])
def prank_index():
    """Page revaealing the prank.
    Includes a form for starting a new session."""
    form = CreateGameForm()
    if form.validate_on_submit():
            game_id = create_room()
            flask.session['game_id'] = game_id
            return flask.redirect(flask.url_for('.prankster_chat'))
    else:
        return flask.render_template('prank_index.html', form=form)


# TODO: eliminate check duplication against victim_chat
@main.route('/itsaprankbro/chat')
def prankster_chat():
    """Checks for a valid room key and victim flag in session.
    Redirects back to index if key is invalid or expired, and back to
    to homepage with an error. Otherwise, serves the prankster's chat page."""

    # check the user *has* a room key
    user_game_id = flask.session.get('game_id', None)
    if user_game_id is None:
        flask.flash('Invalid game id.')
        return flask.redirect(flask.url_for('.index'), form=EnterChatForm())

    # check the user has a valid room key
    error = check_room_key(user_game_id)
    if error:
        flask.flash(error)
        return flask.redirect(flask.url_for('.index'), form=EnterChatForm())

    # check the user has a valid room key
    error = check_room_key(user_game_id)
    if error:
        flask.flash(error)
        return flask.redirect(flask.url_for('.prank_index'), form=EnterChatForm())

    return flask.render_template('prankster_chat.html', game_id=user_game_id)


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

        game = GameInstance(game_id, flask.current_app._get_current_object())
        thread = Thread(target = game.update_clients)
        thread.start()
       
        return game.game_id


def check_room_key(game_id):
    """Check the given room key exists and hasn't expired.
    Returns an error string, or None if the key is ok."""
    game = GameController.query.filter_by(game_id=game_id).one_or_none()

    if game is None:
        return "Sorry, that key appears to be invalid. Are you sure it's correct?"

    return None
