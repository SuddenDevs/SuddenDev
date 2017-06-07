from enum import Enum

class Message:
    def __init__(self, source, mtype, entity, vector, string, to_self):
        self.source = source
        self.mtype = mtype
        self.string = string

        self.entity = entity
        self.vector = vector
        self.to_self = to_self

class MessageType(Enum):
    HELP = 'help'
    OK = 'ok'
    KILL = 'kill'
    NEED_AMMO = 'need ammo'
    LOW_HEALTH = 'low health'
