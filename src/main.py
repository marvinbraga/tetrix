"""
Main entry point for Tetrix game.
"""

from .game import Game

def main():
    """Start the game."""
    game = Game()
    game.run()

if __name__ == '__main__':
    main()