import flask
import os
import random
import string
import sqlalchemy
import datetime
import flask_socketio as fsio
import flask_login
import json
from threading import Thread
from . import main
from . import socketio
from . import login_manager
from .models import db, GameSetup, User
from .game_instance import GameInstance
from requests_oauthlib import OAuth2Session

# TODO: get rid of and use databases
GLOBAL_DICT = dict()
REQUIRED_PLAYER_COUNT = 4

CLIENT_ID = '690133088753-kk72josco183eb8smpq4dgkrqmd0eovm.apps.googleusercontent.com'
CLIENT_SECRET = os.environ['CLIENT_SECRET']
REDIRECT_URI = 'http://localhost:5000/gcallback'
AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
SCOPE = ['https://www.googleapis.com/auth/userinfo.email',
             'https://www.googleapis.com/auth/userinfo.profile']

@main.route('/', methods=['GET', 'POST'])
def index():
    """Landing page."""
    if flask_login.current_user is not None and flask_login.current_user.is_authenticated:
        auth_url = flask.url_for('.lobby')
    else:
        google = get_google_auth()
        auth_url, state = google.authorization_url(AUTH_URI, access_type='offline')
        flask.session['oauth_state'] = state
    return flask.render_template('index.html', auth_url=auth_url)

@main.route('/gcallback', methods=['GET', 'POST'])
def g_callback():
    if flask_login.current_user is not None and flask_login.current_user.is_authenticated:
        return flask.redirect(flask.url_for('.lobby'))
    if 'code' not in flask.request.args and 'state' not in flask.request.args:
        return flask.redirect(flask.url_for('.index'))
    else:
        google = get_google_auth(state=flask.session['oauth_state'])
        token = google.fetch_token(TOKEN_URI, client_secret=CLIENT_SECRET,
                authorization_response=flask.request.url)
        google = get_google_auth(token=token)
        resp = google.get(USER_INFO)
        if resp.status_code == 200:
            user_data = resp.json()
            user = User.query.filter_by(email=user_data['email']).first()

            if user is None:
                user = User()
                user.email = user_data['email']
                user.name = user_data['name']
                user.picture = user_data['picture']

            user.tokens = json.dumps(token)
            db.session.add(user)
            db.session.commit()
            flask_login.login_user(user)
            return flask.redirect(flask.url_for('.lobby'))


@main.route('/game', methods=['GET', 'POST'])
@flask_login.login_required
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
@flask_login.login_required
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

    user = flask_login.current_user
    return flask.render_template('lobby.html', rooms=rooms, user=user)

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

def get_google_auth(state=None, token=None):
    if token:
        return OAuth2Session(CLIENT_ID, token=token)
    if state:
        return OAuth2Session(CLIENT_ID, state=state, redirect_uri=REDIRECT_URI)
    return OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
