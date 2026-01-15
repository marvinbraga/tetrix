# Tetrix

A Tetris clone implemented in Python using Pygame.

## Installation & Running

### Using uv (Recommended)

If you have [uv](https://github.com/astral-sh/uv) installed, you can run the game directly without manual environment setup:

```bash
uv run python main.py
```

### Traditional approach

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Linux/macOS
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the game:
   ```bash
   python main.py
   ```

## Controls

- Left/Right Arrow: Move piece
- Down Arrow: Soft drop
- Up Arrow: Rotate piece
- Space: Hard drop
- P: Pause
- R: Restart (when game over)

## Features

- Classic Tetris gameplay
- 7 different tetromino pieces
- Score and level system
- Next piece preview
- Line clearing animations

## Project Structure

- `src/`: Source code
- `assets/`: Game assets (images, sounds, fonts)
- `data/`: Game data (high scores)
- `tests/`: Unit tests