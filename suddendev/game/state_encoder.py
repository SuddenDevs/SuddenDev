#!/usr/bin/python3

import json
from .event import EventType

def encodeState(game):
    return json.dumps(game, cls=StateEncoder)

def clamp(x): 
    return max(0, min(x, 255))

class StateEncoder(json.JSONEncoder):
    def default(self, o):
        return self.serializeState(o)

    def serializeState(self, state):
        return { 
                'wave': state.wave,
                'enemies': self.serializeEnemies(state.enemies),
                'powerups': self.serializePowerups(state.powerups),
                'walls': self.serializeWalls(state.walls),
                'players': self.serializePlayers(state.players),
                'core': self.serializeCore(state.core),
                'events': self.serializeEvents(state.events)
        }

    def serializeEntity(self, entity):
        return {
                'tag': entity.tag,
                'pos': self.serializeVector(entity.pos),
                'vel': self.serializeVector(entity.vel),
                'size': entity.size,
                'healthMax': entity.healthMax,
                'health': entity.health
                }

    def serializePlayers(self, players):
        result = []
        for p in players:
            json = self.serializeEntity(p)
            json['name'] = p.name
            json['ammo'] = p.ammo
            json['color'] = self.serializeColor(p.color)
            result.append(json)
        return result

    def serializeWalls(self, walls):
        result = []
        for w in walls:
            json = self.serializeEntity(w)
            json['pos'] = self.serializeVector(w.pos)
            json['dim'] = self.serializeVector(w.dim)
            result.append(json)
        return result

    def serializeVector(self, pos):
        return {'x' : pos.x, 'y': pos.y}

    def serializeColor(self, color):
        return "0x{0:02x}{1:02x}{2:02x}".format(clamp(color.r), clamp(color.g), clamp(color.b))

    #TODO
    #Duplication, will extend if enemies or powerups start to differ

    def serializeEnemies(self, enemies):
        result = []
        for e in enemies:
            json = self.serializeEntity(e)
            result.append(json)
        return result

    def serializePowerups(self, powerups):
        result = []
        for p in powerups:
            json = self.serializeEntity(p)
            json['powerup_type'] = p.powerup_type.value
            result.append(json)
        return result

    def serializeCore(self, core):
        return self.serializeEntity(core)

    def serializeEvents(self, events):
        result = []
        for e in events:
            json = {'name': e.event_type.value}
            body = None

            # Case Analysis to encode body
            # TODO: make this less ugly
            if e.event_type == EventType.ENEMY_SPAWN or e.event_type == EventType.ENEMY_DEATH:
                body = self.serializeEntity(e.body[0]);
            elif e.event_type == EventType.POWERUP_SPAWN or e.event_type == EventType.POWERUP_USED:
                body = self.serializeEntity(e.body[0]);

            json['body'] = body
            result.append(json)
        return result
