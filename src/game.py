"""
Game module for Tetrix.
Contains the main Game class that orchestrates the game loop.
"""

import pygame
import random
import sys
from .board import Board
from .piece import Piece
from .scoring import Scoring
from .renderer import Renderer
from .input_handler import InputHandler, Action
from .audio import SoundManager
from .menu import MainMenu
from .settings import Settings

class GameState:
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2

class Game:
    """
    Main game class handling the game loop and state.
    """

    def __init__(self, width: int = 600, height: int = 700):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Tetrix')
        self.clock = pygame.time.Clock()
        self.fps = 60

        self.settings = Settings()
        self.board = Board()
        self.scoring = Scoring()
        self.renderer = Renderer(self.screen, self.settings)
        self.input_handler = InputHandler()
        self.audio = SoundManager()
        
        # Menu System
        self.menu = MainMenu(self.screen, self.renderer, self.scoring, self.audio)
        self.state = GameState.MENU

        self.current_piece = self._generate_piece()
        self.next_piece = self._generate_piece()
        self.paused = False

        self.drop_timer = 0
        self.drop_interval = 1000  # milliseconds

        # Movement timers for controlled input
        self.move_left_timer = 0
        self.move_right_timer = 0
        self.move_down_timer = 0
        self.rotate_timer = 0
        self.MOVE_DELAY = 200  # initial delay in ms
        self.MOVE_REPEAT = 50  # repeat rate in ms
        self.ROTATE_DELAY = 150  # delay between rotations

    def _generate_piece(self) -> Piece:
        """Generate a random new piece."""
        shapes = list(Piece.SHAPES.keys())
        return Piece(random.choice(shapes))

    def _spawn_piece(self):
        """Spawn the next piece."""
        self.current_piece = self.next_piece
        self.next_piece = self._generate_piece()
        # Reset position to top center
        self.current_piece.position = [Board.WIDTH // 2 - 2, 0]

        # Check for game over
        if not self.board.is_valid_position(self.current_piece):
            self.state = GameState.GAME_OVER
            self.audio.play('gameover')

    def start_game(self):
        """Reset and start a new game."""
        self.board = Board()
        self.scoring.reset()
        self.current_piece = self._generate_piece()
        self.next_piece = self._generate_piece()
        self.state = GameState.PLAYING
        self.paused = False
        self.drop_timer = 0

    def update(self, dt: float):
        """Update game state."""
        
        if self.state == GameState.MENU:
            self.menu.update()
            return
            
        if self.state == GameState.GAME_OVER:
            return

        if self.paused:
            return

        self.input_handler.update()
        actions = self.input_handler.get_actions()

        # Handle input with controlled timing
        if Action.MOVE_LEFT in actions:
            if self.move_left_timer <= 0:
                if self.board.is_valid_position(self.current_piece, -1, 0):
                    self.current_piece.move(-1, 0)
                    self.audio.play('move')
                self.move_left_timer = self.MOVE_DELAY if self.move_left_timer == 0 else self.MOVE_REPEAT
            self.move_left_timer -= dt
        else:
            self.move_left_timer = 0

        if Action.MOVE_RIGHT in actions:
            if self.move_right_timer <= 0:
                if self.board.is_valid_position(self.current_piece, 1, 0):
                    self.current_piece.move(1, 0)
                    self.audio.play('move')
                self.move_right_timer = self.MOVE_DELAY if self.move_right_timer == 0 else self.MOVE_REPEAT
            self.move_right_timer -= dt
        else:
            self.move_right_timer = 0

        if Action.MOVE_DOWN in actions:
            if self.move_down_timer <= 0:
                if self.board.is_valid_position(self.current_piece, 0, 1):
                    self.current_piece.move(0, 1)
                    self.drop_timer = max(0, self.drop_timer - 200)  # accelerate drop
                self.move_down_timer = self.MOVE_REPEAT
            self.move_down_timer -= dt
        else:
            self.move_down_timer = 0

        if Action.ROTATE in actions and self.rotate_timer <= 0:
            # Try rotation with wall kicks
            original_shape = [row[:] for row in self.current_piece.shape]
            original_pos = self.current_piece.position[:]
            self.current_piece.rotate()
            if not self.board.is_valid_position(self.current_piece):
                # Try wall kick left
                self.current_piece.move(-1, 0)
                if not self.board.is_valid_position(self.current_piece):
                    # Try wall kick right
                    self.current_piece.move(2, 0)  # back to original +1
                    if not self.board.is_valid_position(self.current_piece):
                        # Revert
                        self.current_piece.position = original_pos
                        self.current_piece.shape = original_shape
                        self.current_piece.rotation = (self.current_piece.rotation - 1) % 4
                    else:
                        self.audio.play('rotate')
                else:
                    self.audio.play('rotate')
            else:
                self.audio.play('rotate')
            self.rotate_timer = self.ROTATE_DELAY

        self.rotate_timer -= dt

        if Action.DROP in actions:
            # Hard drop
            dropped = False
            while self.board.is_valid_position(self.current_piece, 0, 1):
                self.current_piece.move(0, 1)
                dropped = True
            
            if dropped:
                self.audio.play('drop')
            
            self._place_piece()
            return

        # Automatic drop
        self.drop_timer += dt
        if self.drop_timer >= self.drop_interval:
            self.drop_timer = 0
            if self.board.is_valid_position(self.current_piece, 0, 1):
                self.current_piece.move(0, 1)
            else:
                self._place_piece()

        # Update drop speed based on level
        self.drop_interval = int(self.scoring.get_speed() * 1000)

    def _place_piece(self):
        """Place the current piece and handle line clearing."""
        if self.board.place_piece(self.current_piece):
            lines = self.board.clear_lines()
            if lines > 0:
                self.audio.play('clear')
            else:
                self.audio.play('drop') # Regular drop sound if no lines cleared
                
            self.scoring.add_score(lines)
            self._spawn_piece()

    def _get_ghost_piece(self):
        """Calculate the ghost piece position."""
        ghost = self.current_piece.clone()
        while self.board.is_valid_position(ghost, 0, 1):
            ghost.move(0, 1)
        return ghost

    def render(self):
        """Render the game."""
        
        if self.state == GameState.MENU:
            self.menu.draw()
            pygame.display.flip()
            return

        # Game Rendering
        self.screen.fill(self.renderer.COLOR_BG)

        self.renderer.draw_board(self.board)
        
        if self.state == GameState.PLAYING or self.state == GameState.GAME_OVER:
            # Don't draw active piece in game over if needed, but usually fine
            if self.state == GameState.PLAYING:
                 # Draw ghost piece
                ghost = self._get_ghost_piece()
                self.renderer.draw_piece(ghost, ghost=True)
                self.renderer.draw_piece(self.current_piece)
            
            self.renderer.draw_ui(self.scoring, self.next_piece)
            
            if self.paused:
                self.renderer.draw_pause()
                
            if self.state == GameState.GAME_OVER:
                self.renderer.draw_game_over()

        pygame.display.flip()

    def handle_events(self):
        """Handle pygame events."""
        events = pygame.event.get()
        
        # Pass events to menu if in menu state
        if self.state == GameState.MENU:
            action = self.menu.handle_input(events)
            if action == "START":
                self.start_game()
            elif action == "EXIT":
                return False
            # Theme change is handled internally by menu modifying renderer
            
        for event in events:
            if event.type == pygame.QUIT:
                self.scoring.save_high_score()
                return False
            
            elif event.type == pygame.KEYDOWN:
                if self.state == GameState.PLAYING:
                    if event.key == pygame.K_p:
                        self.paused = not self.paused
                    elif event.key == pygame.K_ESCAPE:
                        # Return to menu
                        self.scoring.save_high_score()
                        self.state = GameState.MENU
                        
                elif self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_r:
                        self.start_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU

        return True

    def run(self):
        """Main game loop."""
        running = True
        while running:
            dt = self.clock.tick(self.fps)
            running = self.handle_events()
            self.update(dt)
            self.render()

        pygame.quit()
        sys.exit()