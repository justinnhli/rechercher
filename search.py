from abc import abstractmethod
from collections import namedtuple
from heapq import heappush, heappop

class SearchProblem:
    def __init__(self, start, goal_test, heuristic=None):
        self._start = start
        self._goal_test = goal_test
        self._heuristic = heuristic
    def initial_state(self):
        return self._start
    def is_at_goal(self, state):
        return self._goal_test(state)
    def heuristic_cost(self, state):
        if self._heuristic:
            return self._heuristic(state)
        return 0

class SearchNode:
    @staticmethod
    def initial_search_node(state):
        return SearchNode([state,], [], 0, 0)
    def __init__(self, path, actions, cost, heuristic=0):
        self.path = path
        self.actions = actions
        self.cost = cost
        self.heuristic = heuristic
    @property
    def state(self):
        return self.path[-1]
    @property
    def depth(self):
        return len(self.path)
    def __eq__(self, other):
        return hash(self) == hash(other)
    def __hash__(self):
        return hash(self.state)

# SEARCH

SearchAlgorithm = namedtuple("SearchAlgorithm", ("key_fn", "filter_fn"))

DEPTH_FIRST_SEARCH = SearchAlgorithm((lambda node: -node.depth), None)
BREADTH_FIRST_SEARCH = SearchAlgorithm((lambda node: node.depth), None)
UNIFORM_COST_SEARCH = SearchAlgorithm((lambda node: node.cost), None)
ASTAR_SEARCH = SearchAlgorithm((lambda node: node.cost + node.heuristic), None)

def search(search_problem, algo):
    fringe = [SearchNode.initial_search_node(search_problem.initial_state()),]
    fringe_priority = {}
    visited = set()
    while fringe:
        cur_node = fringe.pop(0)
        while cur_node.state in visited:
            cur_node = fringe.pop(0)
        visited.add(cur_node.state)
        if search_problem.is_at_goal(cur_node.state):
            return cur_node
        for action, state, cost in search_problem.successors(cur_node.state):
            if state not in visited:
                node = SearchNode(cur_node.path + [state,], cur_node.actions + [action,], cur_node.cost + cost, search_problem.heuristic_cost(state))
                if state in fringe_priority and algo.key_fn(fringe_priority[state]) > algo.key_fn(node):
                    fringe.remove(fringe_priority[state])
                fringe_priority[state] = node
                fringe.append(node)
        fringe = sorted(filter(algo.filter_fn, fringe), key=algo.key_fn)
    return None

# UTILITY CLASSES

class PriorityQueue:
    Pair = namedtuple("Pair", ("priority", "item"))
    def __init__(self, key_fn):
        self.queue = []
        self.key_fn = key_fn
        self.items = {}
        self.removed = set()
    def __contains__(self, item):
        return item in self.items
    def push(self, item):
        assert item is not None and item not in self.items
        pair = PriorityQueue.Pair(self.key_fn(item), item)
        self.items[item] = pair
        heappush(self.queue, pair)
    def pop(self):
        while self.queue:
            pair = heappop(self.queue)
            if pair.item is not None:
                del self.items[pair.item]
                return pair.item
    def remove(self, item):
        if item in self.items:
            self.items[item].item = None
        else:
            raise KeyError(item)
    def get_priority(self, item):
        if item in self.items:
            return self.items[item].priority
        else:
            raise KeyError(item)
