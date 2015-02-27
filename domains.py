from collections import namedtuple
from enum import Enum, unique

from rechercher import SearchProblem

class GridWorld(SearchProblem):
    @staticmethod
    def state(**kwargs):
        return namedtuple("State", ("x", "y"))(**kwargs)
    @staticmethod
    def heuristic(goal):
        return (lambda state: abs(state.x - goal.x) + abs(state.y - goal.y))
    def __init__(self, width, height, start, goal):
        self.width = width
        self.height = height
        self.goal = self.state(x=goal[0], y=goal[1])
        super().__init__(
                self.state(x=start[0], y=start[1]),
                (lambda state: state == self.goal),
                (lambda state: GridWorld.heuristic(self.goal)(state)))
    def successors(self, state):
        successors = []
        if state.x - 1 > 0:
            successors.append(("left", GridWorld.state(x=state.x-1, y=state.y), 1))
        if state.y - 1 > 0:
            successors.append(("down", GridWorld.state(x=state.x, y=state.y-1), 1))
        if state.x + 1 <= self.width:
            successors.append(("right", GridWorld.state(x=state.x+1, y=state.y), 1))
        if state.y + 1 <= self.width:
            successors.append(("up", GridWorld.state(x=state.x, y=state.y+1), 1))
        return successors

class Maze(GridWorld):
    @unique
    class Tile(Enum):
        start = "@"
        wall = "#"
        goal = "*"
        space = " "
    @staticmethod
    def char_to_tile(char):
        if char == "#":
            return Maze.Tile.wall
        elif char == " ":
            return Maze.Tile.space
        elif char == "@":
            return Maze.Tile.start
        elif char == "*":
            return Maze.Tile.goal
    def __init__(self, file):
        self.maze = []
        self.start = (0, 0)
        self.goal = (0, 0)
        with open(file) as fd:
            for row, line in enumerate(fd.read().splitlines()):
                row_tiles = []
                for col, char in enumerate(line):
                    tile = Maze.char_to_tile(char)
                    if tile == Maze.Tile.start:
                        self.start = (row, col)
                    elif tile == Maze.Tile.goal:
                        self.goal = (row, col)
                    row_tiles.append(tile)
                self.maze.append(row_tiles)
        super().__init__(len(self.maze[0]), len(self.maze), self.start, self.goal)
    def successors(self, state):
        return [state for state in super().successors(state) if self.maze[state.x][state.y] != Maze.Tile.wall]
