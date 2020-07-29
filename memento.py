from collections import deque


class PointContainerMemento(object):
    def __init__(self):
        self.points = []


class PlotHistory(object):
    def __init__(self):
        self.history = deque()