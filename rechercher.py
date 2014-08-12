#!/usr/bin/env python3

from abc import abstractmethod
from collections import namedtuple
from heapq import heappush, heappop

# DOMAINS

class Domain:
    @staticmethod
    @abstractmethod
    def get_state_class():
        raise NotImplementedError()
    @abstractmethod
    def get_successors(self, state):
        raise NotImplementedError()

# GENERIC SEARCH

class SearchProblem:
    def __init__(self, domain, initial_state, goal_test, heuristic=None):
        self.domain = domain
        self.initial_state = initial_state
        self.goal_test = goal_test
        self.heuristic = heuristic
    def get_initial_state(self):
        return self.initial_state
    def is_at_goal(self, state):
        return self.goal_test(state)
    def get_heuristic_cost(self, state):
        return self.heuristic(state)

class SearchNode:
    @staticmethod
    def get_initial_search_node(state):
        return SearchNode([state,], [], 0)
    def __init__(self, path, actions, cost):
        self.path = path
        self.actions = actions
        self.cost = cost
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

def search(search_problem, algo):
    fringe = [SearchNode.get_initial_search_node(search_problem.get_initial_state()),]
    fringe_priority = {}
    visited = set()
    while fringe:
        cur_node = fringe.pop(0)
        while cur_node.state in visited:
            cur_node = fringe.pop(0)
        visited.add(cur_node.state)
        if search_problem.goal_test(cur_node.state):
            return cur_node
        for action, state, cost in search_problem.domain.get_successors(cur_node.state):
            if state not in visited:
                node = SearchNode(cur_node.path + [state,], cur_node.actions + [action,], cur_node.cost + cost)
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
