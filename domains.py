#!/usr/bin/env python3

from collections import namedtuple

from rechercher import Domain

class GridWorld(Domain):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    @staticmethod
    def get_state_class():
        return namedtuple("State", ("x", "y"))
    def get_successors(self, state):
        successors = []
        if state.x - 1 > 0:
            successors.append(("left", GridWorld.get_state_class()(x=state.x-1, y=state.y), 1))
        if state.y - 1 > 0:
            successors.append(("down", GridWorld.get_state_class()(x=state.x, y=state.y-1), 1))
        if state.x + 1 <= self.width:
            successors.append(("right", GridWorld.get_state_class()(x=state.x+1, y=state.y), 1))
        if state.y + 1 <= self.width:
            successors.append(("right", GridWorld.get_state_class()(x=state.x, y=state.y+1), 1))
        return successors
