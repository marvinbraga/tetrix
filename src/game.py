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
        self.held_piece = None
        self.can_hold = True
        self.paused = False

        # Game statistics tracking
        self.game_start_time = 0
        self.game_time = 0

        # Animation state
        self._pending_clear = False

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
        # Allow hold again for the new piece
        self.can_hold = True

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
        self.held_piece = None
        self.can_hold = True
        self.state = GameState.PLAYING
        self.paused = False
        self.drop_timer = 0
        self.game_start_time = pygame.time.get_ticks()
        self.game_time = 0
        self._pending_clear = False
        # Clear any existing animations
        self.renderer.anim_manager = self.renderer.anim_manager.__class__()

    def update(self, dt: float):
        """Update game state."""

        if self.state == GameState.MENU:
            self.menu.update()
            return

        if self.state == GameState.GAME_OVER:
            # Still update animations in game over
            self.renderer.anim_manager.update()
            return

        if self.paused:
            return

        # Update animations
        self.renderer.anim_manager.update()

        # Check if line clear animation finished
        if self._pending_clear and not self.renderer.anim_manager.has_line_clear():
            self._complete_line_clear()

        # Don't process input during line clear animation
        if self.renderer.anim_manager.has_line_clear():
            return

        self.input_handler.update()
        actions = self.input_handler.get_actions()

        # Handle input with controlled timing
        self._handle_movement(actions, dt)
        self._handle_rotation(actions, dt)
        self._handle_drop(actions, dt)

        # Update drop speed based on level
        self.drop_interval = int(self.scoring.get_speed() * 1000)

        # Update game time
        if self.state == GameState.PLAYING:
            self.game_time = (pygame.time.get_ticks() - self.game_start_time) / 1000

    def _handle_movement(self, actions, dt: float):
        """Handle horizontal and vertical movement input."""
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

    def _handle_rotation(self, actions, dt: float):
        """Handle piece rotation with wall kicks."""
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

    def _handle_drop(self, actions, dt: float):
        """Handle hard drop, hold piece, and automatic drop."""
        if Action.DROP in actions:
            # Hard drop - count distance
            drop_distance = 0
            while self.board.is_valid_position(self.current_piece, 0, 1):
                self.current_piece.move(0, 1)
                drop_distance += 1

            if drop_distance > 0:
                # Add drop bonus points
                bonus_points = self.scoring.add_drop_bonus(drop_distance)
                # Show floating text for drop bonus
                if bonus_points > 0:
                    self.renderer.anim_manager.add_floating_text(
                        f"+{bonus_points}",
                        self.screen.get_width() // 2,
                        400,
                        (150, 200, 255)
                    )
                self.audio.play('drop')

            self._place_piece()
            return

        if Action.HOLD in actions and self.can_hold:
            self._hold_piece()
            return

        # Automatic drop
        self.drop_timer += dt
        if self.drop_timer >= self.drop_interval:
            self.drop_timer = 0
            if self.board.is_valid_position(self.current_piece, 0, 1):
                self.current_piece.move(0, 1)
            else:
                self._place_piece()

    def _hold_piece(self):
        """Hold the current piece and swap with held piece."""
        if not self.can_hold:
            return

        self.audio.play('hold')  # Play hold sound
        self.can_hold = False

        if self.held_piece is None:
            # First time holding
            self.held_piece = self.current_piece.shape_type
            self.current_piece = self.next_piece
            self.next_piece = self._generate_piece()
        else:
            # Swap current with held
            temp = self.held_piece
            self.held_piece = self.current_piece.shape_type
            self.current_piece = Piece(temp)

        # Reset position to top center
        self.current_piece.position = [Board.WIDTH // 2 - 2, 0]

    def _place_piece(self):
        """Place the current piece and handle line clearing."""
        if self.board.place_piece(self.current_piece):
            # Get lines to clear for animation
            lines_to_clear = []
            for y in range(len(self.board.grid)):
                if all(self.board.grid[y]):
                    lines_to_clear.append(y)

            lines = len(lines_to_clear)

            # Add score and get info about combo/level up
            score_info = self.scoring.add_score(lines)

            if lines > 0:
                # Start line clear animation
                is_tetris = score_info['is_tetris']
                self.renderer.anim_manager.add_line_clear(lines_to_clear, is_tetris)

                # Play appropriate sound
                if is_tetris:
                    self.audio.play('tetris')
                    # Screen shake for Tetris
                    self.renderer.anim_manager.add_screen_shake(intensity=10)
                else:
                    self.audio.play('clear')

                # Show combo if active
                if score_info['combo'] > 1:
                    self.renderer.anim_manager.add_combo(
                        score_info['combo'],
                        self.screen.get_width() // 2,
                        250
                    )
                    self.audio.play('combo')

                # Show score earned
                if score_info['points'] > 0:
                    color = (255, 255, 100) if is_tetris else (255, 255, 255)
                    self.renderer.anim_manager.add_floating_text(
                        f"+{score_info['points']}",
                        self.screen.get_width() // 2,
                        300,
                        color
                    )

                # Check for level up
                if score_info['leveled_up']:
                    self.renderer.anim_manager.add_level_up(self.scoring.level)
                    self.audio.play('levelup')
            else:
                self.audio.play('drop')  # Regular drop sound if no lines cleared

            # Wait for line clear animation before clearing and spawning
            if lines > 0:
                # Store that we need to clear lines after animation
                self._pending_clear = True
            else:
                self._spawn_piece()

    def _complete_line_clear(self):
        """Complete the line clear after animation finishes."""
        self.board.clear_lines()
        self._pending_clear = False
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

        # Get screen shake offset
        shake_offset = self.renderer.anim_manager.get_screen_offset()

        self.renderer.draw_board(self.board, shake_offset=shake_offset)

        if self.state == GameState.PLAYING or self.state == GameState.GAME_OVER:
            # Don't draw active piece in game over if needed, but usually fine
            if self.state == GameState.PLAYING:
                 # Draw ghost piece
                ghost = self._get_ghost_piece()
                self.renderer.draw_piece(ghost, ghost=True, shake_offset=shake_offset)
                self.renderer.draw_piece(self.current_piece, shake_offset=shake_offset)

            self.renderer.draw_ui(self.scoring, self.next_piece, self.held_piece)

            # Draw animations
            self.renderer.anim_manager.draw(
                self.screen,
                self.renderer.board_offset,
                self.renderer.block_size,
                self.board.WIDTH,
                self.renderer.font_title,
                self.renderer.font_label,
                self.renderer.font_value,
                self.renderer.COLOR_TEXT
            )

            if self.paused:
                self.renderer.draw_pause()

            if self.state == GameState.GAME_OVER:
                self.renderer.draw_game_over(self.scoring, self.game_time)

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
                        self.scoring.save_high_score()
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