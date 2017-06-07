import flask
import os
import random
import string
import sqlalchemy
import datetime
import flask_socketio as fsio
import flask_login
import json
import redis
from threading import Thread
from . import main, socketio, redis, login_manager
from .config import Config
from .models import db, User
from .game_instance import GameInstance
from requests_oauthlib import OAuth2Session

REQUIRED_PLAYER_COUNT = 4

# Template for Redis entry of an ongoing game.
# Player ids have to be set one by one because redis does not suppport
# nested data structures
DEFAULT_GAME_STATE = {
        'game_id' : 0,
        'lobby_name' : '',
        'time_created': '',
        'created_by': '',
        'wave' : 1,
        'player_count' : 0,
        'p1' : -1,
        'p2' : -1,
        'p3' : -1,
        'p4' : -1,
        'result' : ''
        }

PLAYER_KEYS = ['p0', 'p1', 'p2', 'p3']

# Template for Redis entry of a player.
DEFAULT_PLAYER_STATE = {
        'state' : 'not_ready',
        'username' : '',
        'game_id' : ''
        }

LOBBY_NAME1 = ['friendly', 'sad', 'brave', 'clever', 'slow', 'keen', 'scared', 'triangular', 'round', 'fiery', 'quiet', 'flaming']
LOBBY_NAME2 = ['anaconda', 'python', 'cobra', 'snek', 'rattlesnek', 'boa', 'viper', 'rainbow boa', 'lizard', 'serpent']

@main.route('/', methods=['GET', 'POST'])
def index():
    """Landing page."""
    # If user is logged in, go straight to lobby, otherwise go to OAuth
    if flask_login.current_user is not None and flask_login.current_user.is_authenticated:
        auth_url = flask.url_for('.lobby')
    else:
        google = get_google_auth()
        auth_url, state = google.authorization_url(Config.AUTH_URI, access_type='offline')
        flask.session['oauth_state'] = state
    return flask.render_template('index.html', auth_url=auth_url)

@main.route('/gcallback', methods=['GET', 'POST'])
def g_callback():
    """
    Callback route for Google's OAuth.
    """
    if flask_login.current_user is not None and flask_login.current_user.is_authenticated:
        return flask.redirect(flask.url_for('.lobby'))
    if 'code' not in flask.request.args and 'state' not in flask.request.args:
        return flask.redirect(flask.url_for('.index'))
    else:
        google = get_google_auth(state=flask.session['oauth_state'])
        token = google.fetch_token(Config.TOKEN_URI, client_secret=Config.CLIENT_SECRET,
                authorization_response=flask.request.url)
        google = get_google_auth(token=token)
        response = google.get(Config.USER_INFO)

        # Successful auth
        if response.status_code == 200:
            user_data = response.json()
            user = User.query.filter_by(email=user_data['email']).first()

            # Create new user if he doesn't exist and add to db
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
    player_id = flask_login.current_user.id
    player_state = redis.hgetall(player_id)
    game_id = player_state['game_id']

    name = flask.session.get('name', None)

    if game_id is None:
        flask.flash('Invalid game id!')
        return flask.redirect(flask.url_for('.lobby'))

    if name is None:
        flask.flash('You must have a name!')
        return flask.redirect(flask.url_for('.lobby'))

    return flask.render_template('game.html', user=flask_login.current_user)

@main.route('/logout', methods=['GET', 'POST'])
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('.index'))

@main.route('/docs', methods=['GET'])
def docs():
    return flask.render_template('docs.html')

@main.route('/lobby', methods=['GET', 'POST'])
@flask_login.login_required
def lobby():
    """
    Contains all currently open rooms, along with a button to instantly connect
    to them.
    """
    rooms = []
    result = redis.smembers('rooms')
    if result is not None:
        for r in result:
            room = redis.hgetall(r)
            if not int(room['player_count']) == REQUIRED_PLAYER_COUNT:
                rooms.append(room)

    if flask.request.method == 'POST':

        if flask.request.form['name'] != "":
            name = flask.request.form['name']
        else:
            name = 'anon'

        player_id = flask_login.current_user.id
        if flask.request.form['submit'] == 'create':
            game_id = create_room()
        else:
            game_id = flask.request.form['submit']

        added = add_player(game_id, player_id, name)
        if added is not None:
            flask.flash(added + '\nError joining game. game_id: ' + str(game_id) + ', player_id: ' + str(player_id))
            return flask.render_template('lobby.html', rooms=rooms, user=flask_login.current_user)

        return flask.redirect(flask.url_for('.game_page'))

    return flask.render_template('lobby.html', rooms=rooms, user=flask_login.current_user)

def create_room():
    """Creates a new chat room and returns the key."""
    # TODO: A safer way of making sure we don't generate duplicate room keys

    def gen_random_string(n):
        return ''.join(random.choice(
            string.ascii_uppercase + string.digits) for _ in range(n))

    game_id = gen_random_string(10)
    while redis.sismember('rooms', game_id):
        game_id = gen_random_string(10)

    redis.sadd('rooms', game_id)
    game = dict(DEFAULT_GAME_STATE)
    # TODO more meaningful name
    game['game_id'] = str(game_id)
    game['lobby_name'] = random.choice(LOBBY_NAME1) + " " + random.choice(LOBBY_NAME2)
    game['time_created'] = str(datetime.datetime.now())
    redis.hmset(game_id, game)

    return game_id

def add_player(game_id, player_id, name):
    """
    Adds a player to the given room entry in Redis. Creates a player hash map
    to store the player's state and game_id. Returns True if adding the player
    was successful.
    """

    if not redis.sismember('rooms', game_id):
        return 'This game does not exist'

    player_hm = DEFAULT_PLAYER_STATE
    player_hm['game_id'] = game_id
    player_hm['username'] = name

    # lock = redis.lock(game_id)

    game_state = redis.hgetall(game_id)

    count = int(game_state['player_count'])
    if count < REQUIRED_PLAYER_COUNT:
        if count == 0:
            redis.hset(game_id, 'created_by', name)

        redis.hset(game_id, PLAYER_KEYS[count], player_id)
        redis.hmset(player_id, player_hm)
        redis.hset(game_id, 'player_count', count + 1)

        # lock.release()
        return None
    else:
        return 'Game is full.'

    # lock.release()
    return 'Something went wrong.'

def get_players_in_room(game_id):
    """
    Get player ids of all players in a given game.
    """
    if not redis.sismember('rooms', game_id):
        return None
    else:
        result = []
        game_state = redis.hgetall(game_id)
        for p in PLAYER_KEYS:
            if game_state[p] != str(-1):
                result.append(game_state[p])
            else:
                break
        return result

def get_google_auth(state=None, token=None):
    """
    Helper factory function for OAuth requests.
    """
    redirect_uri = flask.url_for('.g_callback', _external=True)
    if token:
        return OAuth2Session(Config.CLIENT_ID, token=token)
    if state:
        return OAuth2Session(Config.CLIENT_ID, state=state, redirect_uri=redirect_uri)
    return OAuth2Session(Config.CLIENT_ID, redirect_uri=redirect_uri, scope=Config.SCOPE)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
