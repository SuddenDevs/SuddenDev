#!/usr/bin/python3

from json import JSONEncoder

class StateEncoder(JSONEncoder):
    def default(self, o):
        return self.serializeState(o)

    def serializeState(self, state):
        return { 
                'players': self.serializePlayers(state.players),
                'enemies': self.serializeEnemies(state.enemies),
                'powerups': self.serializePowerups(state.powerups),
                'core': self.serializeCore(state.core)
        }

    #TODO
    def serializeEntity(self, entity):
        return {
                'tag': entity.tag,
                'pos': self.serializePosition(entity.position)
                }

    def serializePlayers(self, players):
        result = []
        for p in players:
            result.append(
                {
                    'tag': p.tag,
                    'health': p.health,
                    'ammo': p.ammo,
                    'name': p.name,
                    'position': self.serializePosition(p.position)
                }
            )
        return result

    def serializeEnemies(self, enemies):
        result = []
        for e in enemies:
            result.append( 
                    {
                    'tag' : e.tag,
                    'health' : e.health,
                    'position' : self.serializePosition(e.position)
                    }
                )
        return result

    def serializePosition(self, pos):
        return {'x' : pos.x, 'y': pos.y}

    def serializePowerups(self, powerups):
        result = []
        for p in powerups:
            result.append(
                        {
                        'tag': p.tag,
                        'type': p.type,
                        'position': self.serializePosition(p.position)
                        }
                    )
        return result

    def serializeCore(self, core):
        return {
                'health': core.health,
                'position': self.serializePosition(core.position)
                }
