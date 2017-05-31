class Color3:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

class Color4(Color3):
    def __init__(self, r, g, b, a):
        super().__init__(r, g, b)
        self.a = a
