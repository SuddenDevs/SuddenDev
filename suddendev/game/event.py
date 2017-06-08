from enum import Enum

class Event:
    def __init__(self, event_type, *args):
        self.event_type = event_type
        self.body = args

class EventType(Enum):
    ENEMY_SPAWN = 'Enemy_Spawn'
    ENEMY_DEATH = 'Enemy_Death'
    PLAYER_DEATH = 'Player_Death'
    POWERUP_SPAWN = 'Powerup_Spawn'
    POWERUP_USED = 'Powerup_Used'
    GAME_START = 'Game_Start'
    GAME_END = 'Game_End'
    MESSAGE_SENT = 'Message_Sent'
    ATTACK = 'Attack'
