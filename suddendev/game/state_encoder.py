#!/usr/bin/python3

import json
from .event import EventType
from .game import Game

def encodeState(game):
    return json.dumps(game, cls=StateEncoder)

def clamp(x): 
    return max(0, min(x, 255))

class StateEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Game):
            return self.serializeState(o)

        return {}

    def serializeState(self, state):
        return { 
                'wave': state.wave,
                'enemies': self.serializeEnemies(state.enemies),
                'pickups': self.serializePickups(state.pickups),
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
                'healthMax': entity.health_max,
                'health': entity.health
                }

    def serializePlayers(self, players):
        result = []
        for p in players:
            result.append(self.serializePlayer(p))
        return result

    def serializePlayer(self, p):
        json = self.serializeEntity(p)
        json['player_id'] = p.player_id
        json['name'] = p.name
        json['ammo'] = p.ammo
        json['range_visible'] = p.range_visible
        json['range_attackable'] = p.range_attackable
        json['color'] = self.serializeColor(p.color)
        return json

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
    #Duplication, will extend if enemies or pickups start to differ

    def serializeEnemies(self, enemies):
        result = []
        for e in enemies:
            json = self.serializeEntity(e)
            json['range_attackable'] = e.range_attackable
            json['enemy_type'] = e.enemy_type.value
            result.append(json)
        return result

    def serializePickups(self, pickups):
        result = []
        for p in pickups:
            result.append(self.serializePickup(p))
        return result

    def serializeCore(self, core):
        return self.serializeEntity(core)

    def serializePickup(self, pickup):
        json = self.serializeEntity(pickup)
        json['type'] = pickup.pickup_type.value
        json['value'] = pickup.value
        return json

    def serializeMessage(self, message):
        json = {
                'source' : self.serializePlayer(message.source),
                'string' : message.string,
                }
        return json

    def serializeChatBubble(self, chat):
        json = {
                'source' : self.serializePlayer(chat.player),
                'string' : chat.string
                }
        return json

    def serializeEvents(self, events):
        result = []
        for e in events:
            json = {'name': e.event_type.value}
            body = None

            # Case Analysis to encode body
            # TODO: make this less ugly
            if (e.event_type == EventType.ENEMY_SPAWN or e.event_type == EventType.ENEMY_DEATH):
                body = self.serializeEntity(e.body[0]);
            elif e.event_type == EventType.PLAYER_DEATH:
                body = self.serializePlayer(e.body[0]);
            elif e.event_type == EventType.PICKUP_SPAWN or e.event_type == EventType.PICKUP_USED:
                body = self.serializePickup(e.body[0]);
            elif e.event_type == EventType.GAME_END:
                body = e.body[0].value
            elif e.event_type == EventType.PRINT or e.event_type == EventType.ERROR:
                body = [
                        e.body[0],
                        self.serializePlayer(e.body[1])
                        ]
            elif e.event_type == EventType.ATTACK:
                body = [
                        self.serializeEntity(e.body[0]),
                        self.serializeEntity(e.body[1]),
                        ]
            elif e.event_type == EventType.MESSAGE_SENT:
                body = self.serializeMessage(e.body[0])
            elif e.event_type == EventType.CHAT_BUBBLE:
                body = self.serializeChatBubble(e.body[0])

            json['body'] = body
            result.append(json)
        return result
