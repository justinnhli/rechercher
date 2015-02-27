#!/usr/bin/env python3

import unittest

import rechercher

class TestGridWorldSearch(unittest.TestCase):
    def setUp(self):
        self.problem = rechercher.domains.GridWorld(20, 20, (0, 0), (19, 15))
    def test_bfs(self):
        solution = rechercher.breadth_first_search.search(self.problem)
        self.assertIsNotNone(solution)
        self.assertEqual(len(solution.path), 35)
    def test_ucs(self):
        solution = rechercher.uniform_cost_search.search(self.problem)
        self.assertIsNotNone(solution)
        self.assertEqual(len(solution.path), 35)
    def test_astar(self):
        solution = rechercher.astar_search.search(self.problem)
        self.assertIsNotNone(solution)
        self.assertEqual(len(solution.path), 35)

class TestMazeSearch(unittest.TestCase):
    def setUp(self):
        maze_string = ""
        with open("maze-search.data") as fd:
            maze_string = fd.read()
        self.problem = rechercher.domains.Maze(maze_string)
    def test_bfs(self):
        solution, num_visited = rechercher.breadth_first_search.search(self.problem, verbose=True)
        self.assertIsNotNone(solution)
        self.assertEqual(len(solution.path), 39)
        self.assertEqual(num_visited, 111)
    def test_ucs(self):
        solution, num_visited = rechercher.uniform_cost_search.search(self.problem, verbose=True)
        self.assertIsNotNone(solution)
        self.assertEqual(len(solution.path), 39)
        self.assertEqual(num_visited, 111)
    def test_astar(self):
        solution, num_visited = rechercher.astar_search.search(self.problem, verbose=True)
        self.assertIsNotNone(solution)
        self.assertEqual(len(solution.path), 39)
        self.assertEqual(num_visited, 83)

if __name__ == "__main__":
    """
    maze_string = ""
    with open("demo.maze") as fd:
        maze_string = fd.read()
    problem = rechercher.domains.Maze(maze_string)
    solution = rechercher.search(problem, rechercher.BREADTH_FIRST_SEARCH)
    """
    unittest.main()