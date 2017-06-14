import random

class Color3:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

def random_color3():
    lightness = 0.6
    extra = random.random() * 0.5
    one = [lightness, 0, extra]
    two = [0, lightness, extra]
    three = [0, extra, lightness]
    four = [lightness, extra, 0]
    five = [extra, lightness, 0]
    six = [lightness, extra, 0]
    choice = [one, two, three, four, five, six]

    select = random.choice(choice)
    chosen = list(map(lambda x: x * 255, random.choice(choice)))

    r = int(chosen[0])
    g = int(chosen[1])
    b = int(chosen[2])

    return Color3(r, g, b)

class Color4(Color3):
    def __init__(self, r, g, b, a):
        super().__init__(r, g, b)
        self.a = a
