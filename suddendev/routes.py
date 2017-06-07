import flask
import sqlalchemy
import flask_socketio as fsio
import flask_login
import json

from . import main, socketio, login_manager
from .config import Config
from .models import db, User
from .game_instance import GameInstance
from .events import update_players
from requests_oauthlib import OAuth2Session
from .rooms import (
    get_all_open_rooms,
    create_room,
    add_player_to_room,
    get_room_of_player,
)

@main.route('/', methods=['GET', 'POST'])
def index():
    """Landing page."""

    # if user is logged in, go straight to lobby, otherwise go to OAuth
    if flask_login.current_user is not None and flask_login.current_user.is_authenticated:
        auth_url = flask.url_for('.home')
    else:
        google = get_google_auth()
        auth_url, state = google.authorization_url(Config.AUTH_URI, access_type='offline')
        flask.session['oauth_state'] = state
    return flask.render_template('index.html', auth_url=auth_url)

@main.route('/logout', methods=['GET', 'POST'])
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('.index'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_google_auth(state=None, token=None):
    """Helper factory function for OAuth requests."""

    redirect_uri = flask.url_for('.g_callback', _external=True)
    if token:
        return OAuth2Session(Config.CLIENT_ID, token=token)
    if state:
        return OAuth2Session(Config.CLIENT_ID, state=state, redirect_uri=redirect_uri)
    return OAuth2Session(Config.CLIENT_ID, redirect_uri=redirect_uri, scope=Config.SCOPE)

@main.route('/gcallback', methods=['GET', 'POST'])
def g_callback():
    """Callback route for Google's OAuth."""

    if flask_login.current_user is not None and flask_login.current_user.is_authenticated:
        return flask.redirect(flask.url_for('.home'))
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
            return flask.redirect(flask.url_for('.home'))


@main.route('/game', methods=['GET', 'POST'])
@flask_login.login_required
def game_page():
    player_id = flask_login.current_user.id
    game_id = get_room_of_player(player_id)

    if game_id is None:
        flask.flash('Invalid game id!')
        return flask.redirect(flask.url_for('.lobby'))

    return flask.render_template('game.html', user=flask_login.current_user)

@main.route('/docs', methods=['GET'])
def docs():
    return flask.render_template('docs.html')

@flask_login.login_required
@main.route('/scripts', methods=['GET'])
def scripts():
    return flask.render_template('scripts.html')

@main.route('/lobby', methods=['GET', 'POST'])
@flask_login.login_required
def lobby():
    """Point for users to browse and join existing games."""

    rooms = get_all_open_rooms()
    if flask.request.method == 'POST':

        name = 'anon'
        if flask.request.form['name'] != "":
            name = flask.request.form['name']

        player_id = flask_login.current_user.id

        game_id = ""
        if flask.request.form['submit'] == 'create':
            game_id, error_message = create_room(player_id, name)

            if game_id is None:
                flask.flash(error_message)
                return flask.render_template('lobby.html', rooms=rooms, user=flask_login.current_user)

        else:
            game_id = flask.request.form['submit']

        added, error_message = add_player_to_room(game_id, player_id, name)

        if not added:
            flask.flash(error_message)
            return flask.render_template('lobby.html', rooms=rooms, user=flask_login.current_user)
        else:
            # notify all players that a new one has joined
            update_players(game_id)

        return flask.redirect(flask.url_for('.game_page'))

    return flask.render_template('lobby.html', rooms=rooms, user=flask_login.current_user)


@main.route('/home', methods=['GET'])
@flask_login.login_required
def home():
    """Post-login page."""
    # TODO: workout if noob or not - need DB field
    return flask.render_template('home.html', user=flask_login.current_user, noob=True)
