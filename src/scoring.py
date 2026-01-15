"""
Scoring module for Tetrix game.
Handles score calculation, level progression, and high score persistence.
"""

import os
import json

class Scoring:
    """
    Manages scoring, level system, and high scores.
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
    
    HIGH_SCORE_FILE = os.path.join('data', 'high_scores.json')

    def __init__(self):
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.high_score = self._load_high_score()

    def add_score(self, lines: int):
        """Add score based on lines cleared."""
        if lines in self.POINTS:
            self.score += self.POINTS[lines] * self.level
        self.lines_cleared += lines
        self._update_level()
        
        if self.score > self.high_score:
            self.high_score = self.score

    def _update_level(self):
        """Update level based on total lines cleared."""
        new_level = (self.lines_cleared // self.LINES_PER_LEVEL) + 1
        self.level = min(new_level, 20)  # Cap at level 20

    def get_speed(self) -> float:
        """Get drop speed in seconds per line based on level."""
        # Speed increases with level, minimum 0.1 seconds
        return max(1.0 - (self.level - 1) * 0.05, 0.1)

    def reset(self):
        """Reset scoring for a new game."""
        self.save_high_score() # Save before reset
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.high_score = self._load_high_score()

    def _load_high_score(self) -> int:
        """Load the top score from disk."""
        if os.path.exists(self.HIGH_SCORE_FILE):
            try:
                with open(self.HIGH_SCORE_FILE, 'r') as f:
                    data = json.load(f)
                    return data.get('top_score', 0)
            except:
                return 0
        return 0

    def save_high_score(self):
        """Save the top score to disk."""
        if not os.path.exists('data'):
            os.makedirs('data')
            
        data = {'top_score': self.high_score}
        try:
            with open(self.HIGH_SCORE_FILE, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving high score: {e}")
