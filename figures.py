
class Point(object):
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def clone(self):
        return type(self)(
            self.x,
            self.y,
            self.radius)

    def __str__(self):
        return f"X: {self.x}, Y: {self.y}"