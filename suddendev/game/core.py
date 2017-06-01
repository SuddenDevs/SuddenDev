from .entity import Entity
from .vector import Vector

class Core(Entity):
    def __init__(self):
        super().__init__()
        self.pos = Vector(0, 0)
