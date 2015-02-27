from collections import defaultdict, namedtuple
from enum import Enum, unique

from .search import SearchProblem

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
        self.goal = self.state(x=goal[0], y=goal[1])
        super().__init__(
                self.state(x=start[0], y=start[1]),
                (lambda state: state == self.goal),
                (lambda state: GridWorld.heuristic(self.goal)(state)))
    def successors(self, state):
        successors = []
        if state.x - 1 >= 0:
            successors.append(("left", GridWorld.state(x=state.x-1, y=state.y), 1))
        if state.y - 1 >= 0:
            successors.append(("down", GridWorld.state(x=state.x, y=state.y-1), 1))
        if state.x + 1 < self.width:
            successors.append(("right", GridWorld.state(x=state.x+1, y=state.y), 1))
        if state.y + 1 < self.height:
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
        return [(action, successor, cost) for action, successor, cost in super().successors(state) if self.maze[successor.y][successor.x] != Maze.Tile.wall]
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
        for i in range(len(s)):
            cur_dist[0] = i + 1
            for j in range(len(t)):
                cur_dist[j+1] = min(cur_dist[j] + 1, prev_dist[j+1] + 1, prev_dist[j] + (0 if s[i] == t[j] else 1))
            for j in range(len(cur_dist)):
                prev_dist[j] = cur_dist[j]
        return cur_dist[-1]
    @staticmethod
    def heuristic(goal):
        return (lambda state: WordLadder.levenshtein_distance(state, goal))
    @staticmethod
    def build_links(words, fixed_length=True):
        links = defaultdict(set)
        words = sorted(words)
        for i in range(len(words)):
            word = words[i]
            for j in range(i+1, len(words)):
                other_word = words[j]
                if len(word) == len(other_word) or (not fixed_length and abs(len(words[i]) - len(words[j])) == 1):
                    if WordLadder.levenshtein_distance(word, other_word) == 1:
                        links[word].add(other_word)
                        links[other_word].add(word)
        return links
    def __init__(self, start, end, fixed_length=True, links_file=None, dictionary_file=None):
        self.end = self.state(word=end)
        self.fixed_length = fixed_length
        self.links = {}
        if links_file is None and dictionary_file is None:
            from os.path import dirname, join as join_path
            links_file = join_path(dirname(__file__), "data/wordladder/links")
        if links_file is not None:
            from ast import literal_eval
            with open(links_file) as fd:
                self.links = literal_eval("{" + fd.read() + "}")
        else:
            with open(dictionary_file) as fd:
                self.links = WordLadder.build_links(fd.read().splitlines(), self.fixed_length)
        super().__init__(
                self.state(word=start),
                (lambda state: state == self.end),
                (lambda state: WordLadder.heuristic(self.end)(state)))
    def successors(self, state):
        return list((None, WordLadder.state(word=word), 1) for word in self.links[state.word] if not self.fixed_length or len(word) == len(state.word))
    def draw(self, state):
        print(state.word)
