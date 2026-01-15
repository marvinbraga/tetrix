"""
Tests for Board class.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from src.board import Board
from src.piece import Piece

class TestBoard(unittest.TestCase):

    def test_board_creation(self):
        board = Board()
        self.assertEqual(len(board.grid), Board.HEIGHT)
        self.assertEqual(len(board.grid[0]), Board.WIDTH)

    def test_valid_position(self):
        board = Board()
        piece = Piece('I')
        piece.position = [0, 0]
        self.assertTrue(board.is_valid_position(piece))

        # Move to invalid position
        piece.position = [-1, 0]
        self.assertFalse(board.is_valid_position(piece))

    def test_place_piece(self):
        board = Board()
        piece = Piece('O')
        piece.position = [0, 0]
        self.assertTrue(board.place_piece(piece))
        self.assertEqual(board.grid[0][1], 1)
        self.assertEqual(board.grid[0][2], 1)
        self.assertEqual(board.grid[1][1], 1)
        self.assertEqual(board.grid[1][2], 1)

    def test_clear_lines(self):
        board = Board()
        # Fill bottom row
        for x in range(Board.WIDTH):
            board.grid[Board.HEIGHT - 1][x] = 1

        lines = board.clear_lines()
        self.assertEqual(lines, 1)
        # Check if line was cleared
        self.assertEqual(board.grid[Board.HEIGHT - 1], [0] * Board.WIDTH)

if __name__ == '__main__':
    unittest.main()