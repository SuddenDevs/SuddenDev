import flask
import random
import string
import sqlalchemy
import datetime
from . import main
from .forms import EnterChatForm, SetupChatForm
from .models import db, ChatRoom

# TODO: deal with pranksters setting up multiple pranks


@main.route('/', methods=['GET', 'POST'])
def index():
    """Landing page. Includes form for joining a chat session."""
    form = EnterChatForm()
    if form.validate_on_submit():
        flask.session['room_key'] = form.key.data
        flask.session['victim'] = True
        return flask.redirect(flask.url_for('.victim_chat'))

    elif flask.request.method == 'GET':
        form.key.data = flask.session.get('room_key', '')
    return flask.render_template('index.html', form=form)


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
    user_room_key = flask.session.get('room_key', None)
    if user_room_key is None:
        flask.flash('You need to enter a key to join a chat!')
        return flask.redirect(flask.url_for('.index'), form=EnterChatForm())

    # check the user has a valid room key
    error = check_room_key(user_room_key)
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
        flask.session.pop('room_key')
        flask.session.pop('victim')

    # TODO: filter the database, since it also contains old rooms
    rooms = ChatRoom.query.all()

    if flask.request.method == 'POST':
        flask.session['room_key'] = flask.request.form['room_key']
        flask.session['victim'] = True

        return victim_chat()

    return flask.render_template('lobby.html', rooms=rooms)


@main.route('/itsaprankbro', methods=['GET', 'POST'])
def prank_index():
    """Page revaealing the prank.
    Includes a form for starting a new session."""
    form = SetupChatForm()
    if form.validate_on_submit():
            room_key = create_room()
            flask.session['room_key'] = room_key
            flask.session['victim'] = False
            return flask.redirect(flask.url_for('.prankster_chat'))
    else:
        return flask.render_template('prank_index.html', form=form)


# TODO: eliminate check duplication against victim_chat
@main.route('/itsaprankbro/chat')
def prankster_chat():
    """Checks for a valid room key and victim flag in session.
    Redirects back to index if key is invalid or expired, and back to
    to homepage with an error. Otherwise, serves the prankster's chat page."""

    # check the victim isn't on the wrong page
    victim_flag = flask.session.get('victim', True)
    if victim_flag:
        return flask.redirect(flask.url_for('.victim_chat'))  # TODO: notify them?

    # check the user *has* a room key
    user_room_key = flask.session.get('room_key', None)
    if user_room_key is None:
        flask.flash('You need to enter a key to join a chat!')
        return flask.redirect(flask.url_for('.index'), form=EnterChatForm())

    # check the user has a valid room key
    error = check_room_key(user_room_key)
    if error:
        flask.flash(error)
        return flask.redirect(flask.url_for('.index'), form=EnterChatForm())

    # check the user has a valid room key
    error = check_room_key(user_room_key)
    if error:
        flask.flash(error)
        return flask.redirect(flask.url_for('.prank_index'), form=EnterChatForm())

    return flask.render_template('prankster_chat.html', room_key=user_room_key)


def create_room():
    """Creates a new chat room and returns the key."""
    # TODO: A safer way of making sure we don't generate duplicate room keys

    def gen_random_string(n):
        return ''.join(random.choice(
            string.ascii_uppercase + string.digits) for _ in range(n))

    while True:
        room = ChatRoom(room_key=gen_random_string(5))
        db.session.add(room)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
           continue
        return room.room_key


def check_room_key(room_key):
    """Check the given room key exists and hasn't expired.
    Returns an error string, or None if the key is ok."""
    room = ChatRoom.query.filter_by(room_key=room_key).one_or_none()

    if room is None:
        return "Sorry, that key appears to be invalid. Are you sure it's correct?"

    if room.end_time < datetime.datetime.now():
        return "Sorry, it looks like your session has timed-out."

    return None
