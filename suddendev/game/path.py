from .vector import Vector
import numbers

class Path:
    # Can pass in a list of vectors or tuples of coordinates or any combination
    # of both.
    def __init__(self, *points):
        self.points = []
        self.current_index = None
        self.set_points(points)

    # Converts argument to a vector, either from a vector or from a (x,y) tuple.
    def arg_to_vector(self, point):
        if isinstance(point, Vector):
            return point
        elif isinstance(point, tuple):
            return Vector(point[0], point[1])

        return None

    # Returns whether a given point is in the path.
    def contains_point(self, point):
        vector = self.arg_to_vector(point)
        if vector is None:
            return False

        for p in self.points:
            if p == vector:
                return True

        return False

    # Adds a new point to the path.
    def add_point(self, point):
        vector = self.arg_to_vector(point)
        if vector is not None:
            self.points.append(vector)
            if self.current_index is None:
                self.current_index = 0

    # Removes a new point from the path.
    def remove_point(self, point):
        vector = self.arg_to_vector(point)
        if vector is  None:
            return

        for p in self.points:
            if p == vector:
                self.points.remove(p)
                return

    # Sets path's points to the given list of points.
    def set_points(self, points):
        changed = False

        if len(points) != len(self.points):
            changed = True
        else:
            for i in range(len(points)):
                p = self.arg_to_vector(points[i])
                if p != self.points[i]:
                    changed = True
                    break

        if changed:
            for p in points:
                self.add_point(p)
            if self.points:
                self.current_index = 0
            else:
                self.current_index = None


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
