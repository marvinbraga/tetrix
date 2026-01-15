"""
Scoring module for Tetrix game.
Handles score calculation, level progression, and high score persistence.
"""

import os
import json
from datetime import datetime

class Scoring:
    """
    Manages scoring, level system, and high scores list.
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
        self.scores_list = self._load_scores()
        self.high_score = self.scores_list[0]['score'] if self.scores_list else 0

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
        self.save_high_score() # Save current score to list before reset
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.scores_list = self._load_scores()
        self.high_score = self.scores_list[0]['score'] if self.scores_list else 0

    def _load_scores(self) -> list:
        """Load the top scores list from disk."""
        if os.path.exists(self.HIGH_SCORE_FILE):
            try:
                with open(self.HIGH_SCORE_FILE, 'r') as f:
                    data = json.load(f)
                    # Support both old format (dict) and new format (list)
                    if isinstance(data, dict):
                        return [{'score': data.get('top_score', 0), 'date': 'Legacy'}]
                    return data
            except:
                return []
        return []

    def save_high_score(self):
        """Save the current score to the top scores list on disk."""
        if self.score <= 0:
            return

        if not os.path.exists('data'):
            os.makedirs('data')
            
        # Add current score
        new_entry = {
            'score': self.score,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'level': self.level
        }
        
        self.scores_list.append(new_entry)
        # Sort by score descending and keep top 10
        self.scores_list.sort(key=lambda x: x['score'], reverse=True)
        self.scores_list = self.scores_list[:10]
        
        try:
            with open(self.HIGH_SCORE_FILE, 'w') as f:
                json.dump(self.scores_list, f)
        except Exception as e:
            print(f"Error saving high scores: {e}")