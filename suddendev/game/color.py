import random

class Color3:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

def random_color3():
    r = random.randint(100, 255)
    g = random.randint(100, 255)
    b = random.randint(100, 255)
    return Color3(r, g, b)

class Color4(Color3):
    def __init__(self, r, g, b, a):
        super().__init__(r, g, b)
        self.a = a
