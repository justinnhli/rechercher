#!/usr/bin/env python3

from rechercher import SearchProblem, search, UNIFORM_COST_SEARCH
from domains import GridWorld

def main():
    problem = SearchProblem(
        GridWorld(20, 20),
        GridWorld.get_state(x=0, y=0),
        (lambda state: state.x == 19 and state.y == 15),
        heuristic=GridWorld.heuristic(GridWorld.get_state(x=19, y=15)))
    solution = search(problem, UNIFORM_COST_SEARCH)
    if solution:
        print(solution.path[0])
        for action, state in zip(solution.actions, solution.path[1:]):
            print("  action: {}".format(action))
            print(state)

if __name__ == "__main__":
    main()
