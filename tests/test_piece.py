"""
Tests for Piece class.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from src.piece import Piece

class TestPiece(unittest.TestCase):

    def test_piece_creation(self):
        piece = Piece('I')
        self.assertEqual(piece.shape_type, 'I')
        self.assertEqual(piece.position, [0, 0])
        self.assertEqual(piece.rotation, 0)

    def test_piece_rotation(self):
        piece = Piece('T')
        original_shape = [row[:] for row in piece.shape]
        piece.rotate()
        self.assertNotEqual(piece.shape, original_shape)
        self.assertEqual(piece.rotation, 1)

    def test_piece_movement(self):
        piece = Piece('O')
        piece.move(2, 3)
        self.assertEqual(piece.position, [2, 3])

    def test_get_positions(self):
        piece = Piece('I')
        positions = piece.get_positions()
        expected = [(0, 1), (1, 1), (2, 1), (3, 1)]
        self.assertEqual(positions, expected)

if __name__ == '__main__':
    unittest.main()