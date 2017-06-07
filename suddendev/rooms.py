import random
import datetime
import string
import json
from . import redis
from .lobby_names import LOBBY_ADJECTIVES, LOBBY_NOUNS

# max num of players in a game
MAX_PLAYER_COUNT = 4

# TODO: proper db setup for the default script, and general tracking of user scripts
DEFAULT_SCRIPT = """
# Attacking script
timer = 0

def update(player, delta):
    global timer
    timer += delta
	
    # Find Target
    min_dist = sys.float_info.max
    target = None
    for e in enemies_visible:
        mag = Vector.Length(e.pos - player.pos)
        if mag < min_dist:
            min_dist = mag
            target = e
			
    if target is not None:
        diff = player.pos - target.pos
        mag = min(player.speed, min_dist)
        player.vel = Vector.Normalize(diff) * mag
    else:
        player.vel = Vector(0,0)
"""

# Below dicts describe the loose schema being used to manage games on Redis.
# Redis hashes do not support nesting, so we get past this
# (and make updating the client easier) by using JSON strings.
# These are associated with a game_id for each active (possibly full) room.
GAME_JSON_TEMPLATE = {
    'game_id' : None,           # the game_id of the room (included again for rendering)
    'lobby_name' : None,        # the human-readable name of the room
    'time_created': None,       # the time the room was created
    'created_by': None,         # the display name of the room creator
    'player_count' : 0,         # the number of players currently in the room
    'players': [],              # a list of PLAYER_JSON (see template below)
}

# These form part of a GAME_JSON in the 'players' list.
PLAYER_JSON_TEMPLATE = {
    'id': None,                 # the system-wide id of the player
    'name': None,               # the display name of the player (possibly not unique)
    'script': DEFAULT_SCRIPT,   # the most recently submitted script by the player
    'status': 'editing'         # current player status - 'ready' locked-in waiting to run
                                #                       - 'editing' still editing, not ready
}

# Additionally, for each active user we have a mapping to their current game.
# (This is literally just <player_id> -> <game_id>)
# To keep track of current rooms, we have a set of game_ids
# with key 'rooms'.

def create_room(creator_display_name):
    """
    Creates a new game room and returns a game_id to use as a handle.
    Takes the display name of the user who created the game.
    """

    def gen_random_string(n):
        return ''.join(random.choice(
            string.ascii_uppercase + string.digits) for _ in range(n))

    # TODO: acquire lock for 'rooms'
    game_id = gen_random_string(10)
    while redis.sismember('rooms', game_id):
        game_id = gen_random_string(10)
    redis.sadd('rooms', game_id)
    # TODO: release lock for 'rooms'

    game_json = dict(GAME_JSON_TEMPLATE)
    game_json['game_id'] = game_id
    game_json['lobby_name'] = random.choice(LOBBY_ADJECTIVES) + " " + random.choice(LOBBY_NOUNS) #TODO: ensure unique?
    game_json['time_created'] = str(datetime.datetime.now())
    game_json['created_by'] = creator_display_name

    # TODO: acquire lock for 'game_id' (probably not necessary but concurrency is a scary thing...)
    redis.set(game_id, json.dumps(game_json))
    # TODO: release lock for 'game_id'

    return game_id

def get_players_in_room(game_id):
    """
    Get a list of player ids for all players in the given game room.
    If no such game room exists, return None.
    """

    # TODO: acquire lock for 'game_id'
    game_json_string = redis.get(game_id)
    # TODO: release lock

    if game_json_string is None:
        return None

    game_json = json.loads(game_json_string)
    return game_json['players']

def get_all_open_rooms():
    """
    Returns all open rooms.
    There is no guarantee that the room will remain open.
    """

    # TODO: acquire lock for 'rooms'
    rooms = redis.smembers('rooms')
    # TODO: release lock for 'rooms'

    if rooms is None:
        return []

    open_rooms = []
    for game_id in rooms:
        # TODO: acquire lock for 'game_id'
        game_json_string = redis.get(game_id)
        # TODO: release lock for 'game_id'

        if game_json_string is not None:
            game_json = json.loads(game_json_string)

            if game_json['player_count'] < MAX_PLAYER_COUNT:
                open_rooms.append(game_json)

    return open_rooms

def add_player_to_room(game_id, player_id, name):
    """
    Adds a player to the given room entry in Redis.
    Returns a flag to indicate success, and a user facing error message
    (which is empty if successful).

    Failure occurs when a room with the 'game_id' does not exist or, when
    the room in question is full.
    In either case, get_all_open_rooms() should be called and the view
    updated.
    """

    if not room_exists(game_id):
        return False, "Sorry, something seems to have gone wrong, please try another room."

    # TODO: acquire lock for game_id
    game_json_string = redis.get(game_id)

    if game_json_string is None:
        # TODO: release lock for game_id
        return False, "Sorry, something seems to have gone wrong, please try another room."

    game_json = json.loads(game_json_string)
    if game_json['player_count'] >= MAX_PLAYER_COUNT:
        # TODO: release lock for game_id
        return False, "Sorry, the last space was *just* taken,  please try another room."

    player_json = dict(PLAYER_JSON_TEMPLATE)
    player_json['id'] = player_id
    player_json['name'] = name
    game_json['players'].append(player_json)
    redis.set(game_id, json.dumps(game_json))
    # TODO: release lock for game_id

    redis.set(player_id, game_id)

    return True, ""

def remove_player_from_room(game_id, player_id):
    """
    Removes a player from the given room, if the room exists
    and the player was infact a member.
    """

    if room_exists(game_id):
        # TODO: acquire lock for game_id
        game_json_string = redis.get(game_id)

        if game_json_string is None:
            return

        game_json = json.loads(game_json_string)
        for player_json in game_json['players']:
            if player_json['id'] == player_id:
                game_json['players'].remove(player_json)
                break

        redis.set(game_id, json.dumps(game_json))
        # TODO: release lock for game_id

def get_room_of_player(player_id):
    """
    Return the id of the game a player belongs to.
    If there is no such game, return None.
    """
    return redis.get(player_id)

def room_exists(game_id):
    # TODO: acquire lock for 'rooms'
    room_exists = redis.sismember('rooms', game_id)
    # TODO: release lock for 'rooms'
    return room_exists

def get_room_state_json_string(game_id):
    """Returns none if the room does not exist."""
    # TODO: acquire lock for game_id
    game_json_string = redis.get(game_id)
    # TODO: release lock for game_id
    return game_json_string

def set_script(game_id, player_id, script):
    """
    Sets the given script for the user, if the game exists,
    and the players is a member of the game.
    """
    # TODO: acquire lock for game_id
    game_json_string = redis.get(game_id)

    if game_json_string is None:
        # TODO: release lock for game_id
        return

    game_json = json.loads(game_json_string)
    for player in game_json['players']:

        if player['id'] == player_id:
            player['script'] = script
            break

    redis.set(game_id, json.dumps(game_json))
    # TODO: release lock for game_id
