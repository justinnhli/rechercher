from functools import total_ordering
from collections import namedtuple

from .utils import PriorityQueue

Action = namedtuple('Action', ('name', 'successor', 'cost'))

def state_to_node(state):
    @total_ordering
    class _SearchNode:
        def __init__(self, path, actions):
            self.path = path
            self.actions = actions
        @property
        def state(self):
            return self.path[-1]
        @property
        def cost(self):
            return sum(action.cost for action in self.actions)
        @property
        def depth(self):
            return len(self.path)
        def __lt__(self, other):
            return (self.cost, self.path) < (other.cost, other.path)
        def __hash__(self):
            return hash((self.cost, tuple(self.path)))
        def take_action(self, action):
            return _SearchNode(self.path + [action.successor,], self.actions + [action,])
    return _SearchNode([state,], [])

class SearchProblem:
    @staticmethod
    def state(**kwargs):
        raise NotImplementedError()
    def __init__(self, start, goal_test, heuristic=None):
        self._start = start
        self._goal_test = goal_test
        self._heuristic = heuristic
    def initial_state(self):
        return self._start
    def successors(self, state):
        raise NotImplementedError()
    def is_at_goal(self, state):
        return self._goal_test(state)
    def heuristic_cost(self, state):
        if self._heuristic:
            return self._heuristic(state)
        return 0

def search_algorithm_factory(priority_function):
    def search_algorithm(problem, state=None, verbose=False):
        pq = PriorityQueue()
        if state is None:
            state = problem.initial_state()
        pq.push(state_to_node(state), 0)
        visited = set()
        while pq:
            cur_node = pq.pop()
            if cur_node.state in visited:
                continue
            visited.add(cur_node.state)
            if problem.is_at_goal(cur_node.state):
                if verbose:
                    return cur_node, len(visited)
                else:
                    return cur_node
            for action in problem.successors(cur_node.state):
                if action.successor not in visited:
                    node = cur_node.take_action(action)
                    priority = priority_function(problem, node)
                    if node not in pq or pq.get_priority(node) > priority:
                        pq.set_priority(node, priority)
        return None, len(visited)
    return search_algorithm

depth_first_search = search_algorithm_factory((lambda problem, node: -node.depth))
breadth_first_search = search_algorithm_factory((lambda problem, node: node.cost))
uniform_cost_search = search_algorithm_factory((lambda problem, node: node.cost))
greedy_best_first_search = search_algorithm_factory((lambda problem, node: problem.heuristic_cost(node.state)))
astar_search = search_algorithm_factory((lambda problem, node: node.cost + problem.heuristic_cost(node.state)))

def beam_search(problem, state=None):
    if state is None:
        cur_node = state_to_node(problem.initial_state())
    else:
        cur_node = state_to_node(state)
    while True:
        successors = [cur_node.take_action(action) for action in problem.successors(cur_node.state)]
        successors = sorted(successors, key=(lambda node: problem.heuristic_cost(node.state)))
        if problem.heuristic_cost(successors[0].state) >= problem.heuristic_cost(cur_node.state):
            return cur_node
        else:
            cur_node = successors[0]
