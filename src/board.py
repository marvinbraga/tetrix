"""
Board module for Tetrix game.
Contains the Board class representing the game grid.
"""

from typing import List, Tuple, Optional
from .piece import Piece

class Board:
    """
    Represents the game board/grid.
    """

    WIDTH = 10
    HEIGHT = 20

    def __init__(self):
        self.grid = [[0 for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
        self.colors = [[None for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]

    def is_valid_position(self, piece: Piece, offset_x: int = 0, offset_y: int = 0) -> bool:
        """Check if a piece can be placed at the given position."""
        for x, y in piece.get_positions():
            x += offset_x
            y += offset_y
            if x < 0 or x >= self.WIDTH or y >= self.HEIGHT:
                return False
            if y >= 0 and self.grid[y][x] != 0:
                return False
        return True

    def place_piece(self, piece: Piece) -> bool:
        """Place a piece on the board if valid."""
        if not self.is_valid_position(piece):
            return False
        for x, y in piece.get_positions():
            if y >= 0:
                self.grid[y][x] = 1
                self.colors[y][x] = piece.color
        return True

    def clear_lines(self) -> int:
        """Clear completed lines and return the number of lines cleared."""
        lines_to_clear = []
        for y in range(self.HEIGHT):
            if all(self.grid[y]):
                lines_to_clear.append(y)

        # Remove lines from bottom to top
        for y in reversed(lines_to_clear):
            del self.grid[y]
            del self.colors[y]
            # Add new empty line at top
            self.grid.insert(0, [0] * self.WIDTH)
            self.colors.insert(0, [None] * self.WIDTH)

        return len(lines_to_clear)

    def get_filled_lines(self) -> List[int]:
        """Get indices of filled lines."""
        filled = []
        for y in range(self.HEIGHT):
            if all(self.grid[y]):
                filled.append(y)
        return filled

    def draw(self, screen, block_size: int, offset_x: int, offset_y: int):
        """Draw the board on the screen."""
        import pygame
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                if self.grid[y][x]:
                    rect = pygame.Rect(
                        offset_x + x * block_size,
                        offset_y + y * block_size,
                        block_size,
                        block_size
                    )
                    pygame.draw.rect(screen, self.colors[y][x], rect)
                    pygame.draw.rect(screen, (255, 255, 255), rect, 1)  # Border