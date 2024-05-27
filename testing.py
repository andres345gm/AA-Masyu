import unittest
import board as b


def arrange_not_solvable__4_4():
    """
    Arrange a board that is not solvable
    """
    n = 4
    pearls_list = [
        [1, 1, 1],
        [1, 2, 1],
        [1, 3, 1],
        [1, 4, 1],
        [2, 1, 1],
        [2, 2, 1],
        [2, 3, 1],
        [2, 4, 1],
        [3, 1, 1],
        [3, 2, 1],
        [3, 3, 1],
        [3, 4, 1],
        [4, 1, 1],
        [4, 2, 1],
        [4, 3, 1],
        [4, 4, 1]
    ]
    board = b.Board(n, pearls_list)

    return board


def arrange_solvable__4_4():
    """
    Arrange a board that is solvable
    """
    n = 4
    pearls_list = [
        [2, 1, 1],
        [3, 1, 2],
        [3, 2, 1],
        [3, 4, 1],
        [2, 4, 2],
        [2, 3, 1]
    ]
    board = b.Board(n, pearls_list)
    return board


def cyclic_graph_solution__4_4():
    graph = {
        (0, 0): [(0, 1), (1, 0)],
        (0, 1): [(1, 1), (0, 0)],
        (0, 2): [],
        (0, 3): [],
        (1, 0): [(0, 0), (2, 0)],
        (1, 1): [(0, 1), (1, 2)],
        (1, 2): [(1, 1), (1, 3)],
        (1, 3): [(2, 3), (1, 2)],
        (2, 0): [(1, 0), (2, 1)],
        (2, 1): [(2, 0), (2, 2)],
        (2, 2): [(3, 2), (2, 1)],
        (2, 3): [(1, 3), (3, 3)],
        (3, 0): [],
        (3, 1): [],
        (3, 2): [(2, 2), (3, 3)],
        (3, 3): [(3, 2), (2, 3)]
    }
    return graph


def incomplete_graph_solution__4_4():
    graph = {
        (0, 0): [(0, 1), (1, 0)],
        (0, 1): [(1, 1), (0, 0)],
        (0, 2): [],
        (0, 3): [],
        (1, 0): [(0, 0), (2, 0)],
        (1, 1): [(0, 1), (1, 2)],
        (1, 2): [(1, 1), (1, 3)],
        (1, 3): [(2, 3), (1, 2)],
        (2, 0): [(1, 0), (2, 1)],
        (2, 1): [(2, 0), (2, 2)],
        (2, 2): [(3, 2), (2, 1)],
        (2, 3): [(1, 3)],
        (3, 0): [],
        (3, 1): [],
        (3, 2): [(2, 2)],
        (3, 3): []
    }
    return graph


class MyTestCase(unittest.TestCase):

    def test_black_pearl_True_4_4(self):
        # This test should return True, because the conditions of the black pearl are met
        board = arrange_solvable__4_4()
        matrix = [
            [0, 0, 0, 0],
            [0, 0, 1, 5],
            [0, 0, 0, 2],
            [0, 0, 0, 0]
        ]
        self.assertTrue(board.verify_black_pearl(matrix, 1, 3))

    def test_black_pearl_False_4_4(self):
        # This test should return False, because the left black pearl is a curve
        board = arrange_solvable__4_4()
        matrix = [
            [0, 0, 0, 0],
            [0, 0, 3, 5],
            [0, 0, 0, 2],
            [0, 0, 0, 0]
        ]
        self.assertFalse(board.verify_black_pearl(matrix, 1, 3))

    def test_white_pearl_True_4_4(self):
        # This test should return True, because the conditions of the white pearl are met
        board = arrange_solvable__4_4()
        matrix = [
            [0, 0, 0, 0],
            [0, 3, 1, 5],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.assertTrue(board.verify_white_pearl(matrix, 1, 2))

    def test_white_pearl_False_4_4(self):
        # This test should return False, because the left white pearl is a curve
        board = arrange_solvable__4_4()
        matrix = [
            [0, 0, 0, 0],
            [0, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.assertFalse(board.verify_white_pearl(matrix, 1, 2))

    def test_solve_not_solvable__4_4(self):
        # This test should return None, because the board is not solvable
        board = arrange_not_solvable__4_4()
        self.assertIsNone(board.solve_board())

    def test_solve_solvable__4_4(self):
        # This test should return a list of lists, because the board is solvable
        board = arrange_solvable__4_4()
        self.assertIsNotNone(board.solve_board())

    def test_verify_solution_solvable__4_4(self):
        # This test should return True, because the board is solvable
        board = arrange_solvable__4_4()
        # A known solution is:
        solution = [
            [4, 5, 0, 0],
            [2, 3, 1, 5],
            [3, 1, 5, 2],
            [0, 0, 3, 6]
        ]
        # Set the board matrix to the solution
        board.matrix = solution
        self.assertTrue(board.verify_board())

    def test_verify_not_solution_solvable__4_4(self):
        # This test should return False, because the board is not solvable
        board = arrange_solvable__4_4()
        # The know solution is changed in order to make the board not solvable
        solution = [
            [4, 5, 0, 0],
            [2, 3, 1, 5],
            [3, 1, 5, 2],
            [0, 0, 3, 0]
        ]
        # Set the board matrix to the solution
        board.matrix = solution
        self.assertFalse(board.verify_board())

    def test_board_to_graph_solvable__4_4(self):
        # This test should return a specific graph
        board = arrange_solvable__4_4()
        solution = [
            [4, 5, 0, 0],
            [2, 3, 1, 5],
            [3, 1, 5, 2],
            [0, 0, 3, 6]
        ]
        # Set the board matrix to the solution
        graph = board.board_to_graph(solution)
        graph_assert = cyclic_graph_solution__4_4()
        self.assertDictEqual(graph, graph_assert)

    def test_verify_cycle_True(self):
        # This test should return True, because the graph has a cycle
        board = arrange_solvable__4_4()
        graph = cyclic_graph_solution__4_4()
        self.assertTrue(board.verify_cycle(graph)[0])

    def test_verify_cycle_False(self):
        # This test should return False, because the graph has no cycle
        board = arrange_solvable__4_4()
        graph = incomplete_graph_solution__4_4()
        self.assertFalse(board.verify_cycle(graph)[0])


if __name__ == '__main__':
    unittest.main()
