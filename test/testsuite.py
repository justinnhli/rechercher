#!/usr/bin/env python3

import unittest

import rechercher

class TestGridWorldSearch(unittest.TestCase):
    def setUp(self):
        self.problem = rechercher.domains.GridWorld(20, 20, (0, 0), (19, 15))
    def test_bfs(self):
        solution = rechercher.search(self.problem, rechercher.BREADTH_FIRST_SEARCH)
        self.assertIsNotNone(solution)
        self.assertEqual(len(solution.path), 35)
    def test_ucs(self):
        solution = rechercher.search(self.problem, rechercher.UNIFORM_COST_SEARCH)
        self.assertIsNotNone(solution)
        self.assertEqual(len(solution.path), 35)
    def test_astar(self):
        solution = rechercher.search(self.problem, rechercher.ASTAR_SEARCH)
        self.assertIsNotNone(solution)
        self.assertEqual(len(solution.path), 35)

def main():
    problem = rechercher.domains.GridWorld(20, 20, (0, 0), (19, 15))
    solution = rechercher.search(problem, rechercher.DEPTH_FIRST_SEARCH)
    if solution:
        print(len(solution.path))

if __name__ == "__main__":
    #unittest.main()
    main()
