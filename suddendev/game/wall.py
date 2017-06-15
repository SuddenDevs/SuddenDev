from .entity import Entity
from .vector import Vector

class Wall(Entity):
    def __init__(self, pos, dim):
        super().__init__()
        self.speed_max = 0
        self.pos = pos
        self.dim = dim

    def intersects(self, center, radius):
        width = self.dim.x
        height = self.dim.y

        circle_distance_x = abs(center.x - (self.pos.x + width/2));
        circle_distance_y = abs(center.y - (self.pos.y + height/2));

        if circle_distance_x > (width/2 + radius):
            return False
        if circle_distance_y > (height/2 + radius):
            return False

        if circle_distance_x <= (width/2 + radius):
            return True
        if circle_distance_y <= (height/2 + radius):
            return True

        cornerDistance_sq = (circle_distance_x - width/2)**2 + (circle_distance_y - height/2)**2
        return cornerDistance_sq <= radius**2;
