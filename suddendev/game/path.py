from .vector import Vector
import numbers

class Path:
    # Can pass in a list of vectors or tuples of coordinates or any combination
    # of both.
    def __init__(self, *points):
        self.points = []

        for p in points:
            if isinstance(p, Vector):
                self.points.append(p)
            elif isinstance(p, tuple):
                self.points.append(Vector(p[0], p[1]))

        self.current_index = None

        if self.points:
            self.current_index = 0

    # Returns true if path is either finished or there are no points in the path.
    def is_empty(self):
        return self.current_index is None

    # Advances the target vector. If loop is true, goes back to beginning if end is reached.
    def set_next_target(self, loop=False):
        self.current_index += 1
        if self.current_index >= len(self.points):
            if loop:
                self.current_index = 0
            else:
                self.current_index = None

    # Returns current target vector.
    def current_target(self):
        if self.is_empty():
            return None

        return self.points[self.current_index]
