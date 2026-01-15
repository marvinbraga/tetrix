"""
Scoring module for Tetrix game.
Handles score calculation, level progression, and speed adjustments.
"""

class Scoring:
    """
    Manages scoring and level system.
    """

    # Points for clearing lines
    POINTS = {
        1: 40,
        2: 100,
        3: 300,
        4: 1200
    }

    # Lines needed to advance to next level
    LINES_PER_LEVEL = 10

    def __init__(self):
        self.score = 0
        self.level = 1
        self.lines_cleared = 0

    def add_score(self, lines: int):
        """Add score based on lines cleared."""
        if lines in self.POINTS:
            self.score += self.POINTS[lines] * self.level
        self.lines_cleared += lines
        self._update_level()

    def _update_level(self):
        """Update level based on total lines cleared."""
        new_level = (self.lines_cleared // self.LINES_PER_LEVEL) + 1
        self.level = min(new_level, 20)  # Cap at level 20

    def get_speed(self) -> float:
        """Get drop speed in seconds per line based on level."""
        # Speed increases with level, minimum 0.1 seconds
        return max(1.0 - (self.level - 1) * 0.05, 0.1)

    def reset(self):
        """Reset scoring."""
        self.score = 0
        self.level = 1
        self.lines_cleared = 0