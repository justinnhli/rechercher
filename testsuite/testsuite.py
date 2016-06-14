#!/usr/bin/env python3

import unittest

import rechercher

class Search_GridWorld(unittest.TestCase):
    def setUp(self):
        self.problem = rechercher.domains.GridWorld(20, 20, (0, 0), (19, 15))
    def test_bfs(self):
        solution, num_visited = rechercher.breadth_first_search(self.problem, verbose=True)
        self.assertIsNotNone(solution)
        self.assertEqual(len(solution.path), 35)
    def test_ucs(self):
        solution, num_visited = rechercher.uniform_cost_search(self.problem, verbose=True)
        self.assertIsNotNone(solution)
        self.assertEqual(len(solution.path), 35)
    def test_astar(self):
        solution, num_visited = rechercher.astar_search(self.problem, verbose=True)
        self.assertIsNotNone(solution)
        self.assertEqual(len(solution.path), 35)

class Search_Maze(unittest.TestCase):
    def setUp(self):
        maze_string = """
            #@#####################
            #   # #   #   # #     #
            # ### # # # ### # ### #
            # #     #           # #
            # # ### # ### #########
            #     # # #           #
            # # # ####### ####### #
            # # #   #         #   #
            # # ##### # # # # ### #
            # #   #   # # # #   # #
            #####################*#
        """
        maze_string = "\n".join(line.strip() for line in maze_string.splitlines()).strip()
        self.problem = rechercher.domains.Maze(maze_string)
    def test_bfs(self):
        solution, num_visited = rechercher.breadth_first_search(self.problem, verbose=True)
        self.assertIsNotNone(solution)
        self.assertEqual(len(solution.path), 39)
        self.assertEqual(num_visited, 111)
    def test_ucs(self):
        solution, num_visited = rechercher.uniform_cost_search(self.problem, verbose=True)
        self.assertIsNotNone(solution)
        self.assertEqual(len(solution.path), 39)
        self.assertEqual(num_visited, 111)
    def test_astar(self):
        solution, num_visited = rechercher.astar_search(self.problem, verbose=True)
        self.assertIsNotNone(solution)
        self.assertEqual(len(solution.path), 39)
        self.assertEqual(num_visited, 83)

class Search_WordLadder(unittest.TestCase):
    def setUp(self):
        self.problem = rechercher.domains.WordLadder("yea", "nay")
    def test_astar(self):
        solution, num_visited = rechercher.breadth_first_search(self.problem, verbose=True)
        self.assertIsNotNone(solution)
        self.assertEqual(len(solution.path), 6)

class Search_SlidingPuzzle(unittest.TestCase):
    def setUp(self):
        self.problem = rechercher.domains.SlidingPuzzle((1, 3, 2, 0, 7, 4, 8, 5, 6))
    def test_astar(self):
        solution, num_visited = rechercher.astar_search(self.problem, verbose=True)
        self.assertIsNotNone(solution)
        self.assertEqual(len(solution.path), 20)
        self.assertEqual(num_visited, 700)

class Search_Polynomial(unittest.TestCase):
    def test_beam_left(self):
        self.assertEqual(rechercher.beam_search(rechercher.domains.PolynomialDescent(-10)).state.x, -2)
    def test_beam_middle(self):
        self.assertEqual(rechercher.beam_search(rechercher.domains.PolynomialDescent(0)).state.x, -1)
    def test_beam_right(self):
        self.assertEqual(rechercher.beam_search(rechercher.domains.PolynomialDescent(10)).state.x, 3)

if __name__ == "__main__":
    unittest.main()
