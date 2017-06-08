from enum import Enum

class Message:
    def __init__(self, source, mtype, entity, vector, string, to_self, body):
        self.source = source
        self.mtype = mtype
        self.string = string

        self.entity = entity
        self.vector = vector
        self.to_self = to_self

        self.body = body

class MessageType(Enum):
    HELP = 'help'
    OK = 'ok'
    KILL = 'kill'
    NEED_AMMO = 'need ammo'
    NEED_HEALTH = 'need health'
    POWERUP_HERE = 'powerup here'
    HEALTH_UP_HERE = 'health up here'
    AMMO_UP_HERE = 'ammo up here'
    ENEMY_HERE = 'enemy here'
