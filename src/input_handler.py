"""
Input handler module for Tetrix game.
Manages keyboard input and maps to game actions.
"""

import pygame
from enum import Enum

class Action(Enum):
    MOVE_LEFT = 0
    MOVE_RIGHT = 1
    MOVE_DOWN = 2
    ROTATE = 3
    DROP = 4
    PAUSE = 5
    RESTART = 6

class InputHandler:
    """
    Handles keyboard input and converts to game actions.
    """

    KEY_MAPPING = {
        pygame.K_LEFT: Action.MOVE_LEFT,
        pygame.K_RIGHT: Action.MOVE_RIGHT,
        pygame.K_DOWN: Action.MOVE_DOWN,
        pygame.K_UP: Action.ROTATE,
        pygame.K_SPACE: Action.DROP,
        pygame.K_p: Action.PAUSE,
        pygame.K_r: Action.RESTART,
    }

    def __init__(self):
        self.pressed_keys = set()

    def update(self):
        """Update the set of currently pressed keys."""
        self.pressed_keys = set()
        keys = pygame.key.get_pressed()
        for key, action in self.KEY_MAPPING.items():
            if keys[key]:
                self.pressed_keys.add(action)

    def get_actions(self):
        """Get the set of actions based on current key presses."""
        return self.pressed_keys.copy()

    def is_action_pressed(self, action: Action) -> bool:
        """Check if a specific action is currently pressed."""
        return action in self.pressed_keys