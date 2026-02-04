# Tetrix

A Tetris clone implemented in Python using Pygame.

## Getting Started

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

### Running the game

To run the game immediately (uv will handle dependencies automatically):

```bash
uv run python main.py
```

### Development setup

To set up the local virtual environment and install dependencies:

```bash
uv sync
```

## Controls

- Left/Right Arrow: Move piece
- Down Arrow: Soft drop
- Up Arrow: Rotate piece
- Space: Hard drop
- C or Shift: Hold piece
- P: Pause
- R: Restart (when game over)
- ESC: Return to menu

## Features

- Classic Tetris gameplay
- 7 different tetromino pieces
- Score and level system
- Next piece preview
- Hold piece system (save piece for later)
- Line clearing animations
- High score tracking with top 10 rankings
- Game statistics (time played, lines cleared, level)
- New high score feedback with ranking position
- Multiple visual themes (Neon, Pastel, Retro)
- Sound effects

## Project Structure

- `src/`: Source code
- `assets/`: Game assets (images, sounds, fonts)
- `data/`: Game data (high scores)
- `tests/`: Unit tests