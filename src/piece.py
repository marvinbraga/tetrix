"""
Piece module for Tetrix game.
Contains the Piece class representing tetrominoes.
"""

class Piece:
    """
    Represents a tetromino piece in the game.
    """

    # Tetromino shapes (4x4 matrices)
    SHAPES = {
        'I': [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        'O': [
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        'T': [
            [0, 1, 0, 0],
            [1, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        'S': [
            [0, 1, 1, 0],
            [1, 1, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        'Z': [
            [1, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        'J': [
            [1, 0, 0, 0],
            [1, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        'L': [
            [0, 0, 1, 0],
            [1, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
    }

    COLORS = {
        'I': (0, 255, 255),  # Cyan
        'O': (255, 255, 0),  # Yellow
        'T': (128, 0, 128),  # Purple
        'S': (0, 255, 0),    # Green
        'Z': (255, 0, 0),    # Red
        'J': (0, 0, 255),    # Blue
        'L': (255, 165, 0)   # Orange
    }

    def __init__(self, shape_type: str):
        self.shape_type = shape_type
        self.shape = [row[:] for row in self.SHAPES[shape_type]]
        self.color = self.COLORS[shape_type]
        self.position = [0, 0]  # x, y
        self.rotation = 0

    def rotate(self):
        """Rotate the piece 90 degrees clockwise."""
        # Transpose and reverse each row for rotation
        self.shape = [list(reversed(col)) for col in zip(*self.shape)]
        self.rotation = (self.rotation + 1) % 4

    def move(self, dx: int, dy: int):
        """Move the piece by dx, dy."""
        self.position[0] += dx
        self.position[1] += dy

    def get_positions(self):
        """Get absolute positions of the piece blocks."""
        positions = []
        for y in range(4):
            for x in range(4):
                if self.shape[y][x]:
                    positions.append((self.position[0] + x, self.position[1] + y))
        return positions

    def clone(self):
        """Create a copy of the piece for preview."""
        clone = Piece(self.shape_type)
        clone.shape = [row[:] for row in self.shape]
        clone.position = self.position[:]
        clone.rotation = self.rotation
        return clone