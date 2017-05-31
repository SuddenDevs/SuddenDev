from .entity import Entity

class Enemy(Entity):
    def __init__(self):
        super().__init__(self)
        self.pos = Vector(random.random() * self.map.width,
                            random.random() * self.map.height)
    
    def update(self, delta):
        target = self.map.centre
        self.vel = Vector(1,1)

