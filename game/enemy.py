from entity import Entity

class Enemy(Entity):
    def __init__(self, game):
        super().__init__(self)
        self.game = game

