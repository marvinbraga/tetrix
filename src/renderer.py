"""
Renderer module for Tetrix game.
Handles rendering of game elements with a modern, sophisticated aesthetic.
"""

import pygame
from typing import Optional
from .board import Board
from .piece import Piece
from .scoring import Scoring
from .animations import AnimationManager

class Renderer:
    """
    Handles rendering of game elements using a modern dark theme.
    """

    # Default Theme
    THEMES = {
        'NEON': {
            'BG': (26, 26, 46),
            'GRID': (30, 30, 60),
            'PANEL': (22, 33, 62),
            'TEXT': (233, 69, 96),
            'TEXT_WHITE': (240, 240, 240),
            'PIECES': {
                'I': (0, 240, 240),
                'O': (240, 240, 0),
                'T': (160, 0, 240),
                'S': (0, 240, 0),
                'Z': (240, 0, 0),
                'J': (0, 0, 240),
                'L': (240, 160, 0)
            }
        },
        'PASTEL': {
            'BG': (40, 40, 50),
            'GRID': (50, 50, 60),
            'PANEL': (35, 35, 45),
            'TEXT': (255, 183, 178),
            'TEXT_WHITE': (255, 255, 255),
            'PIECES': {
                'I': (150, 230, 230),
                'O': (255, 255, 180),
                'T': (200, 160, 230),
                'S': (160, 230, 160),
                'Z': (255, 160, 160),
                'J': (160, 160, 230),
                'L': (255, 200, 150)
            }
        },
        'RETRO': {
            'BG': (15, 56, 15),
            'GRID': (48, 98, 48),
            'PANEL': (15, 56, 15),
            'TEXT': (139, 172, 15),
            'TEXT_WHITE': (155, 188, 15),
            'PIECES': {
                # All pieces green shades
                'I': (139, 172, 15),
                'O': (139, 172, 15),
                'T': (48, 98, 48),
                'S': (15, 56, 15),
                'Z': (15, 56, 15),
                'J': (48, 98, 48),
                'L': (139, 172, 15)
            }
        }
    }

    def __init__(self, screen: pygame.Surface, settings, block_size: int = 30):
        self.screen = screen
        self.settings = settings
        self.block_size = block_size
        self.board_offset = (50, 50)

        # Load theme from settings
        self.current_theme_name = self.settings.get('theme')
        self._apply_theme(self.current_theme_name)

        # Initialize fonts
        try:
            self.font_title = pygame.font.Font(None, 60)
            self.font_label = pygame.font.Font(None, 36)
            self.font_value = pygame.font.Font(None, 48)
        except:
            self.font_title = pygame.font.SysFont('Arial', 60, bold=True)
            self.font_label = pygame.font.SysFont('Arial', 30)
            self.font_value = pygame.font.SysFont('Arial', 40, bold=True)

        # Animation manager
        self.anim_manager = AnimationManager()

    def _apply_theme(self, theme_name):
        """Apply the selected theme colors."""
        theme = self.THEMES[theme_name]
        self.COLOR_BG = theme['BG']
        self.COLOR_GRID = theme['GRID']
        self.COLOR_PANEL = theme['PANEL']
        self.COLOR_TEXT = theme['TEXT']
        self.COLOR_TEXT_WHITE = theme['TEXT_WHITE']
        self.PIECE_COLORS = theme['PIECES']

    def set_theme(self, theme_name):
        """Set a specific theme."""
        if theme_name in self.THEMES:
            self.current_theme_name = theme_name
            self._apply_theme(theme_name)
            self.settings.set('theme', theme_name)

    def _draw_block(self, x, y, color, alpha=255, ghost=False):
        """Helper to draw a single block with 3D effect."""
        rect = pygame.Rect(x, y, self.block_size, self.block_size)
        
        if ghost:
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)
            return

        pygame.draw.rect(self.screen, color, rect)

        highlight_points = [(x, y + self.block_size), (x, y), (x + self.block_size, y)]
        lighter = tuple(min(255, c + 100) for c in color)
        pygame.draw.lines(self.screen, lighter, False, highlight_points, 2)

        shadow_points = [(x, y + self.block_size), (x + self.block_size, y + self.block_size), (x + self.block_size, y)]
        darker = tuple(max(0, c - 80) for c in color)
        pygame.draw.lines(self.screen, darker, False, shadow_points, 2)

        inset = 4
        gloss_rect = pygame.Rect(x + inset, y + inset, self.block_size - inset*2, self.block_size - inset*2)
        mid_color = tuple(min(255, c + 30) for c in color)
        pygame.draw.rect(self.screen, mid_color, gloss_rect)

    def draw_board(self, board: Board, shake_offset: tuple = (0, 0)):
        """Draw the game board with grid and locked pieces."""
        offset_x, offset_y = shake_offset

        board_rect = pygame.Rect(
            self.board_offset[0] + offset_x,
            self.board_offset[1] + offset_y,
            board.WIDTH * self.block_size,
            board.HEIGHT * self.block_size
        )
        pygame.draw.rect(self.screen, (20, 20, 35) if self.current_theme_name == 'NEON' else self.COLOR_PANEL, board_rect)
        pygame.draw.rect(self.screen, self.COLOR_TEXT, board_rect, 2)

        for x in range(board.WIDTH):
            start = (self.board_offset[0] + offset_x + x * self.block_size, self.board_offset[1] + offset_y)
            end = (self.board_offset[0] + offset_x + x * self.block_size, self.board_offset[1] + offset_y + board.HEIGHT * self.block_size)
            pygame.draw.line(self.screen, self.COLOR_GRID, start, end, 1)

        for y in range(board.HEIGHT):
            start = (self.board_offset[0] + offset_x, self.board_offset[1] + offset_y + y * self.block_size)
            end = (self.board_offset[0] + offset_x + board.WIDTH * self.block_size, self.board_offset[1] + offset_y + y * self.block_size)
            pygame.draw.line(self.screen, self.COLOR_GRID, start, end, 1)

        for y, row in enumerate(board.grid):
            for x, val in enumerate(row):
                if val:
                    color = board.colors[y][x]
                    # If color is missing or we want to enforce theme colors for retro
                    if self.current_theme_name == 'RETRO' or not color:
                        # Map stored piece type back to color if possible, or use default
                         # Note: board.colors stores RGB tuples.
                         # For theme switching to work perfectly on existing pieces,
                         # we might need to store Piece Types in the grid, not Colors.
                         # But for now, we will just draw what's there unless it's Retro.
                         if self.current_theme_name == 'RETRO':
                             color = self.PIECE_COLORS['T'] # Use generic green
                         elif not color:
                             color = (128, 128, 128)

                    draw_x = self.board_offset[0] + offset_x + x * self.block_size
                    draw_y = self.board_offset[1] + offset_y + y * self.block_size
                    self._draw_block(draw_x, draw_y, color)

    def draw_piece(self, piece: Piece, offset_x: int = 0, offset_y: int = 0, ghost: bool = False, shake_offset: tuple = (0, 0)):
        """Draw a piece."""
        color = self.PIECE_COLORS.get(piece.shape_type, piece.color)
        shake_x, shake_y = shake_offset

        for x, y in piece.get_positions():
            draw_x = self.board_offset[0] + shake_x + (x + offset_x) * self.block_size
            draw_y = self.board_offset[1] + shake_y + (y + offset_y) * self.block_size

            if draw_y < self.board_offset[1] + shake_y:
                continue

            self._draw_block(draw_x, draw_y, color, ghost=ghost)

    def draw_ui(self, scoring: Scoring, next_piece: Piece, held_piece=None):
        """Draw the User Interface."""
        panel_x = 400

        title_surf = self.font_title.render("TETRIX", True, self.COLOR_TEXT)
        self.screen.blit(title_surf, (panel_x, 30))

        self._draw_info_box("SCORE", str(scoring.score), panel_x, 100)
        self._draw_info_box("BEST", str(scoring.high_score), panel_x, 200)
        self._draw_info_box("LEVEL", str(scoring.level), panel_x, 300)
        self._draw_info_box("LINES", str(scoring.lines_cleared), panel_x, 400)

        # Draw HOLD piece (on the right panel, compact size)
        hold_label_surf = self.font_label.render("HOLD", True, self.COLOR_TEXT_WHITE)
        self.screen.blit(hold_label_surf, (panel_x, 500))

        if held_piece:
            from .piece import Piece
            hold_piece_obj = Piece(held_piece)
            self._draw_piece_preview(hold_piece_obj, panel_x, 535, small=True)
        else:
            # Draw empty hold box (compact)
            preview_rect = pygame.Rect(panel_x, 535, 90, 90)
            pygame.draw.rect(self.screen, self.COLOR_PANEL, preview_rect, 0, 8)
            pygame.draw.rect(self.screen, self.COLOR_GRID, preview_rect, 2, 8)

        # Draw NEXT piece (side by side with HOLD)
        label_surf = self.font_label.render("NEXT", True, self.COLOR_TEXT_WHITE)
        self.screen.blit(label_surf, (panel_x + 100, 500))

        self._draw_piece_preview(next_piece, panel_x + 100, 535, small=True)

    def _draw_piece_preview(self, piece: Piece, x: int, y: int, small: bool = False):
        """Helper method to draw a piece preview box."""
        box_size = 90 if small else 150
        preview_rect = pygame.Rect(x, y, box_size, box_size)
        pygame.draw.rect(self.screen, self.COLOR_PANEL, preview_rect, 0, 8)
        pygame.draw.rect(self.screen, self.COLOR_GRID, preview_rect, 2, 8)

        center_x = x + box_size // 2
        center_y = y + box_size // 2
        prev_block_size = 20 if small else self.block_size

        shape = piece.shape
        min_c, max_c = 4, 0
        min_r, max_r = 4, 0
        has_block = False
        for r in range(4):
            for c in range(4):
                if shape[r][c]:
                    min_c = min(min_c, c)
                    max_c = max(max_c, c)
                    min_r = min(min_r, r)
                    max_r = max(max_r, r)
                    has_block = True

        if has_block:
            w = (max_c - min_c + 1) * prev_block_size
            h = (max_r - min_r + 1) * prev_block_size
            start_x = center_x - w // 2
            start_y = center_y - h // 2

            color = self.PIECE_COLORS.get(piece.shape_type, piece.color)

            for r in range(4):
                for c in range(4):
                    if shape[r][c]:
                        draw_x = start_x + (c - min_c) * prev_block_size
                        draw_y = start_y + (r - min_r) * prev_block_size
                        rect = pygame.Rect(draw_x, draw_y, prev_block_size, prev_block_size)
                        pygame.draw.rect(self.screen, color, rect)
                        pygame.draw.rect(self.screen, (255,255,255), rect, 1)


    def _draw_info_box(self, label, value, x, y):
        """Helper to draw a standardized info box."""
        label_surf = self.font_label.render(label, True, self.COLOR_TEXT_WHITE)
        self.screen.blit(label_surf, (x, y))
        
        val_rect = pygame.Rect(x, y + 30, 150, 50)
        pygame.draw.rect(self.screen, self.COLOR_PANEL, val_rect, 0, 8)
        
        val_surf = self.font_value.render(value, True, self.COLOR_TEXT)
        val_rect_text = val_surf.get_rect(center=val_rect.center)
        self.screen.blit(val_surf, val_rect_text)

    def draw_game_over(self, scoring: Scoring, game_time: float):
        """Draw game over overlay with statistics and high score feedback."""
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        center_x = self.screen.get_width() // 2
        y_pos = 100

        # Check if new high score
        is_new_high_score = False
        rank_position = None
        for i, entry in enumerate(scoring.scores_list):
            if entry['score'] == scoring.score:
                is_new_high_score = True
                rank_position = i + 1
                break

        # Game Over title
        go_surf = self.font_title.render("GAME OVER", True, self.COLOR_TEXT)
        go_rect = go_surf.get_rect(center=(center_x, y_pos))
        self.screen.blit(go_surf, go_rect)
        y_pos += 80

        # New High Score message with animation effect
        if is_new_high_score and rank_position is not None:
            import pygame.time
            pulse = abs((pygame.time.get_ticks() % 1000) - 500) / 500.0
            highlight_color = tuple(
                int(self.COLOR_TEXT[i] + (255 - self.COLOR_TEXT[i]) * pulse * 0.5)
                for i in range(3)
            )

            new_hs_surf = self.font_value.render("NEW HIGH SCORE!", True, highlight_color)
            new_hs_rect = new_hs_surf.get_rect(center=(center_x, y_pos))
            self.screen.blit(new_hs_surf, new_hs_rect)
            y_pos += 60

            rank_text = f"#{rank_position} in Top 10"
            rank_surf = self.font_label.render(rank_text, True, self.COLOR_TEXT_WHITE)
            rank_rect = rank_surf.get_rect(center=(center_x, y_pos))
            self.screen.blit(rank_surf, rank_rect)
            y_pos += 50

        # Game Statistics
        stats_font = pygame.font.Font(None, 32)

        # Format game time
        minutes = int(game_time // 60)
        seconds = int(game_time % 60)
        time_text = f"Time: {minutes:02d}:{seconds:02d}"

        stats = [
            f"Score: {scoring.score}",
            f"Level: {scoring.level}",
            f"Lines: {scoring.lines_cleared}",
            time_text
        ]

        for stat in stats:
            stat_surf = stats_font.render(stat, True, self.COLOR_TEXT_WHITE)
            stat_rect = stat_surf.get_rect(center=(center_x, y_pos))
            self.screen.blit(stat_surf, stat_rect)
            y_pos += 40

        y_pos += 20

        # Instructions
        restart_surf = self.font_label.render("Press 'R' to Restart", True, self.COLOR_TEXT_WHITE)
        restart_rect = restart_surf.get_rect(center=(center_x, y_pos))
        self.screen.blit(restart_surf, restart_rect)
        y_pos += 40

        menu_surf = self.font_label.render("Press 'ESC' for Menu", True, self.COLOR_TEXT_WHITE)
        menu_rect = menu_surf.get_rect(center=(center_x, y_pos))
        self.screen.blit(menu_surf, menu_rect)

    def draw_pause(self):
        """Draw pause overlay."""
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        pause_surf = self.font_title.render("PAUSED", True, (255, 255, 255))
        pause_rect = pause_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(pause_surf, pause_rect)
        
        menu_surf = self.font_label.render("Press 'ESC' for Menu", True, self.COLOR_TEXT_WHITE)
        menu_rect = menu_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 50))
        self.screen.blit(menu_surf, menu_rect)