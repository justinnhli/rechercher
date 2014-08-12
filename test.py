#!/usr/bin/env python3

from rechercher import SearchProblem, search, UNIFORM_COST_SEARCH
from domains import GridWorld

def main():
    problem = SearchProblem(
        GridWorld(20, 20),
        GridWorld.get_state_class()(x=0, y=0),
        (lambda state: state.x == 19 and state.y == 15),
        heuristic=(lambda state: abs(19 - state.x) + abs(15 - state.y)))
    solution = search(problem, UNIFORM_COST_SEARCH)
    if solution:
        print(solution.path)

if __name__ == "__main__":
    main()
