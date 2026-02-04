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
        self.combo = 0  # Track consecutive line clears
        self.last_level = 1  # Track level changes

    def add_score(self, lines: int) -> dict:
        """
        Add score based on lines cleared.
        Returns dict with score info for animations.
        """
        points_earned = 0
        combo_multiplier = 1.0

        if lines > 0:
            # Base points
            points_earned = self.POINTS[lines] * self.level

            # Combo system
            self.combo += 1
            if self.combo > 1:
                # Multiplier: 1.5x at combo 2, 2x at combo 3, 2.5x at combo 4, etc.
                combo_multiplier = 1.0 + (self.combo - 1) * 0.5
                combo_multiplier = min(combo_multiplier, 3.0)  # Cap at 3x
                points_earned = int(points_earned * combo_multiplier)

            self.score += points_earned
            self.lines_cleared += lines
        else:
            # Reset combo if no lines cleared
            self.combo = 0

        # Check for level up
        old_level = self.level
        self._update_level()
        leveled_up = self.level > old_level

        if self.score > self.high_score:
            self.high_score = self.score

        return {
            'points': points_earned,
            'combo': self.combo,
            'combo_multiplier': combo_multiplier,
            'leveled_up': leveled_up,
            'is_tetris': lines == 4
        }

    def add_drop_bonus(self, lines_dropped: int) -> int:
        """
        Add bonus points for hard drop.
        Returns points earned (2 points per line dropped).
        """
        bonus = lines_dropped * 2
        self.score += bonus

        if self.score > self.high_score:
            self.high_score = self.score

        return bonus

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
        self.combo = 0
        self.last_level = 1
        self.scores_list = self._load_scores()
        self.high_score = self.scores_list[0]['score'] if self.scores_list else 0

    def _load_scores(self) -> list:
        """Load the top scores list from disk."""
        # Ensure data directory exists
        if not os.path.exists('data'):
            os.makedirs('data')

        if os.path.exists(self.HIGH_SCORE_FILE):
            try:
                with open(self.HIGH_SCORE_FILE, 'r') as f:
                    data = json.load(f)
                    # Support both old format (dict) and new format (list)
                    if isinstance(data, dict):
                        return [{'score': data.get('top_score', 0), 'date': 'Legacy'}]
                    return data
            except json.JSONDecodeError as e:
                print(f"Error decoding high scores JSON: {e}")
                return []
            except (IOError, OSError) as e:
                print(f"Error reading high scores file: {e}")
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