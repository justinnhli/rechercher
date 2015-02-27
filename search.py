from .utils import PriorityQueue

class _SearchNode:
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
    def is_at_goal(self, state):
        return self._goal_test(state)
    def heuristic_cost(self, state):
        if self._heuristic:
            return self._heuristic(state)
        return 0
    def draw(self, state):
        raise NotImplementedError()

class AbstractSearchAlgorithm:
    @staticmethod
    def initial_search_node(state):
        return _SearchNode([state,], [], 0, 0)
    def __init__(self, priority_function=None, filter_function=None):
        self.priority_function = priority_function
        self.filter_function = filter_function
    def search(self, problem, verbose=False, animate=False):
        fringe = [AbstractSearchAlgorithm.initial_search_node(problem.initial_state()),]
        fringe_priority = {}
        visited = set()
        result = None
        while result is None and fringe:
            cur_node = fringe.pop(0)
            while cur_node.state in visited:
                cur_node = fringe.pop(0)
            visited.add(cur_node.state)
            if animate:
                try:
                    problem.draw(cur_node.state)
                    print()
                except:
                    pass
            if problem.is_at_goal(cur_node.state):
                result = cur_node
            for action, state, cost in problem.successors(cur_node.state):
                if state not in visited:
                    node = _SearchNode(cur_node.path + [state,], cur_node.actions + [action,], cur_node.cost + cost, problem.heuristic_cost(state))
                    if state in fringe_priority and self.priority_function(fringe_priority[state]) > self.priority_function(node):
                        fringe.remove(fringe_priority[state])
                    fringe_priority[state] = node
                    fringe.append(node)
            fringe = sorted(filter(self.filter_function, fringe), key=self.priority_function)
        if verbose:
            return result, len(visited)
        else:
            return result

depth_first_search = AbstractSearchAlgorithm((lambda node: -node.depth), None)
breadth_first_search = AbstractSearchAlgorithm((lambda node: node.depth), None)
uniform_cost_search = AbstractSearchAlgorithm((lambda node: node.cost), None)
astar_search = AbstractSearchAlgorithm((lambda node: node.cost + node.heuristic), None)
