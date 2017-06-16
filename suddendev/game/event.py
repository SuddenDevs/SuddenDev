from enum import Enum

class Event:
    def __init__(self, event_type, *args):
        self.event_type = event_type
        self.body = args

class EventType(Enum):
    ENEMY_SPAWN = 'Enemy_Spawn'
    ENEMY_DEATH = 'Enemy_Death'
    PLAYER_DEATH = 'Player_Death'
    PICKUP_SPAWN = 'Pickup_Spawn'
    PICKUP_USED = 'Pickup_Used'
    GAME_START = 'Game_Start'
    GAME_END = 'Game_End'
    MESSAGE_SENT = 'Message_Sent'
    PRINT = 'Print'
    ERROR = 'Error'
    ATTACK = 'Attack'
    CHAT_BUBBLE = 'Chat_Bubble'

class GameOverType(Enum):
    LOSE_PLAYERS = 'Lose_Players'
    LOSE_CORE = 'Lose_Core'
    LOSE_TIMEOUT = 'Lose_Timeout'
    WIN = 'Win'
