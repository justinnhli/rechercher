import math
from ast import literal_eval
from collections import defaultdict, namedtuple
from copy import copy
from enum import Enum, unique
from itertools import chain
from os.path import dirname, join as join_path

from .search import Action, SearchProblem

class GridWorld(SearchProblem):
    @staticmethod
    def state(**kwargs):
        return namedtuple("GridWorldState", ("x", "y"))(**kwargs)
    @staticmethod
    def manhattan_distance(state1, state2):
        return abs(state1.x - state2.x) + abs(state1.y - state2.y)
    @staticmethod
    def heuristic(goal):
        return (lambda state: GridWorld.manhattan_distance(state, goal))
    def __init__(self, width, height, start, goal):
        self.width = width
        self.height = height
        self.goal = GridWorld.state(x=goal[0], y=goal[1])
        super().__init__(
                GridWorld.state(x=start[0], y=start[1]),
                (lambda state: state == self.goal),
                GridWorld.heuristic(self.goal))
    def successors(self, state):
        successors = []
        if state.x - 1 >= 0:
            successors.append(Action("left", GridWorld.state(x=state.x-1, y=state.y), 1))
        if state.y - 1 >= 0:
            successors.append(Action("down", GridWorld.state(x=state.x, y=state.y-1), 1))
        if state.x + 1 < self.width:
            successors.append(Action("right", GridWorld.state(x=state.x+1, y=state.y), 1))
        if state.y + 1 < self.height:
            successors.append(Action("up", GridWorld.state(x=state.x, y=state.y+1), 1))
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
    def __init__(self, maze_string):
        self.maze = []
        self.start = (0, 0)
        self.goal = (0, 0)
        for row, line in enumerate(maze_string.splitlines()):
            row_tiles = []
            for col, char in enumerate(line):
                tile = Maze.char_to_tile(char)
                if tile == Maze.Tile.start:
                    self.start = (col, row)
                elif tile == Maze.Tile.goal:
                    self.goal = (col, row)
                row_tiles.append(tile)
            self.maze.append(row_tiles)
        super().__init__(len(self.maze[0]), len(self.maze), self.start, self.goal)
    def successors(self, state):
        return [Action(action, successor, cost) for action, successor, cost in super().successors(state) if self.maze[successor.y][successor.x] != Maze.Tile.wall]
    def draw(self, state):
        for row in range(len(self.maze)):
            row_string = []
            for col in range(len(self.maze[0])):
                if row == state.y and col == state.x:
                    row_string.append("@")
                elif self.maze[row][col] == Maze.Tile.wall:
                    row_string.append("#")
                else:
                    row_string.append(" ")
            print("".join(row_string))

class WordLadder(SearchProblem):
    @staticmethod
    def state(**kwargs):
        return namedtuple("WordLadderState", "word")(**kwargs)
    @staticmethod
    def levenshtein_distance(s, t):
        if s == t:
            return 0
        elif len(s) == 0:
            return len(t)
        elif len(t) == 0:
            return len(s)
        prev_dist = list(range(len(t) + 1))
        cur_dist = (len(t) + 1) * [0,]
        for i, s_char in enumerate(s):
            cur_dist[0] = i + 1
            for j, t_char in enumerate(t):
                cur_dist[j+1] = min(cur_dist[j] + 1, prev_dist[j+1] + 1, prev_dist[j] + (0 if s_char == t_char else 1))
            prev_dist = copy(cur_dist)
        return cur_dist[-1]
    @staticmethod
    def heuristic(goal):
        return (lambda state: WordLadder.levenshtein_distance(state, goal))
    @staticmethod
    def build_links(words, fixed_length=True):
        links = defaultdict(set)
        words = sorted(words)
        for i, word in enumerate(words):
            for j in range(i+1, len(words)):
                other_word = words[j]
                if len(word) == len(other_word) or (not fixed_length and abs(len(words[i]) - len(words[j])) == 1):
                    if WordLadder.levenshtein_distance(word, other_word) == 1:
                        links[word].add(other_word)
                        links[other_word].add(word)
        return links
    def __init__(self, start, end, fixed_length=True, links_file=None, dictionary_file=None):
        self.end = WordLadder.state(word=end)
        self.fixed_length = fixed_length
        self.links = defaultdict(set)
        if links_file is None and dictionary_file is None:
            links_file = join_path(dirname(__file__), "data/wordladder/links")
        if links_file is not None:
            with open(links_file) as fd:
                self.links = literal_eval("{" + fd.read() + "}")
        else:
            with open(dictionary_file) as fd:
                self.links = WordLadder.build_links(fd.read().splitlines(), self.fixed_length)
        super().__init__(
                WordLadder.state(word=start),
                (lambda state: state == self.end),
                WordLadder.heuristic(self.end))
    def successors(self, state):
        return list(Action(None, WordLadder.state(word=word), 1) for word in self.links[state.word] if not self.fixed_length or len(word) == len(state.word))

class SlidingPuzzle(SearchProblem):
    @staticmethod
    def state(**kwargs):
        return namedtuple('SlidingPuzzleState', ('grid',))(**kwargs)
    @staticmethod
    def in_bounds(row, col, size):
        return (0 <= row < size and 0 <= col < size)
    @staticmethod
    def coord_to_index(row, col, size):
        return row * size + col
    @staticmethod
    def index_to_coord(index, size):
        return (index // size, index % size)
    @staticmethod
    def heuristic(goal):
        def _heuristic(state):
            total = 0
            size = int(math.sqrt(len(state.grid)))
            for i in range(1, 9):
                goal_row, goal_col = SlidingPuzzle.index_to_coord(goal.grid.index(i), size)
                row, col = SlidingPuzzle.index_to_coord(state.grid.index(i), size)
                total += abs(goal_row - row) + abs(goal_col - col)
            return total
        return _heuristic
    def __init__(self, order):
        assert len(order) == len(set(order))
        self.size = int(math.sqrt(len(order)))
        assert self.size ** 2 == len(order)
        self.size = int(self.size)
        order = tuple(order)
        self.goal = SlidingPuzzle.state(grid=tuple(sorted(order)[1:] + [0,]))
        super().__init__(
                SlidingPuzzle.state(grid=order),
                (lambda state: state == self.goal),
                SlidingPuzzle.heuristic(self.goal))
    def successors(self, state):
        index = state.grid.index(0)
        row, col = SlidingPuzzle.index_to_coord(index, self.size)
        result = []
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if SlidingPuzzle.in_bounds(row + dr, col + dc, self.size):
                swap_index = SlidingPuzzle.coord_to_index(row + dr, col + dc, self.size)
                next_state = list(state.grid)
                next_state[index] = next_state[swap_index]
                next_state[swap_index] = 0
                result.append(Action(None, SlidingPuzzle.state(grid=tuple(next_state)), 1))
        return result

class PolynomialDescent(SearchProblem):
    @staticmethod
    def state(**kwargs):
        return namedtuple('ParabolaDescentState', ('x',))(**kwargs)
    @staticmethod
    def heuristic(goal):
        return (lambda state: 2 * (state.x - 4) * (state.x - 2) * (2 * state.x + 2) * (2 * state.x + 4))
    def __init__(self, start):
        super().__init__(
                PolynomialDescent.state(x=start),
                None,
                PolynomialDescent.heuristic(None))
    def successors(self, state):
        results = []
        for i in (-1, 1):
            results.append(Action('{:+.1f}'.format(i), PolynomialDescent.state(x=state.x + i), abs(i)))
        return results

class MissionariesCannibals(SearchProblem):
    @staticmethod
    def state(*args):
        return namedtuple('MCState', ('m', 'c', 'b'))(*args)
    @staticmethod
    def heuristic(goal):
        return 0
    def __init__(self):
        super().__init__(
                MissionariesCannibals.state(3, 3, 1),
                (lambda s: s == namedtuple('MCState', ('m', 'c', 'b'))(0, 0, 0)),
                None)
    def successors(self, state):
        results = []
        if state.b == 1:
            num_m = state.m
            num_c = state.c
        else:
            num_m = 3 - state.m
            num_c = 3 - state.c
        for m, c in ((0, 1), (0, 2), (1, 1), (1, 0), (2, 0)):
            if m > num_m or c > num_c:
                continue
            if state.b == 1:
                new_m = num_m - m
                new_c = num_c - c
                new_b = 0
            else:
                new_m = state.m + m
                new_c = state.c + c
                new_b = 1
            action = Action(
                    '{}M, {}C'.format(m, c),
                    MissionariesCannibals.state(new_m, new_c, new_b),
                    1)
            results.append(action)
        return results
