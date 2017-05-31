#!/usr/bin/python3

import json

def encodeState(state):
    return json.dumps(state, cls=StateEncoder)

class StateEncoder(json.JSONEncoder):
    def default(self, o):
        return self.serializeState(o)

    def serializeState(self, state):
        return { 
                'players': self.serializePlayers(state.players),
                'enemies': self.serializeEnemies(state.enemies),
                'powerups': self.serializePowerups(state.powerups),
                'core': self.serializeCore(state.core)
        }

    def serializeEntity(self, entity):
        return {
                'tag': entity.tag,
                'pos': self.serializeVector(entity.position),
                'vel': self.serializeVector(entity.vel),
                'size': self.serializeVector(entity.size),
                'healthMax': entity.healthMax,
                'health': entity.health
                }

    def serializePlayers(self, players):
        result = []
        for p in players:
            json = self.serializeEntity(p)
            json['name'] = p.name;
            json['ammo'] = p.ammo;
            json['color'] = self.serializeColor(p.color);
            result.append(json)
        return result

    def serializeVector(self, pos):
        return {'x' : pos.x, 'y': pos.y}

    def serializeColor(self, color):
        return {
                'r': color.r,
                'g': color.g,
                'b': color.b
                }

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
            result.append(json)
        return result

    def serializeCore(self, core):
        return self.serializeEntity(core)
