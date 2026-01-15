"""
Renderer module for Tetrix game.
Handles rendering of game elements with a modern, sophisticated aesthetic.
"""

import pygame
from .board import Board
from .piece import Piece
from .scoring import Scoring

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

    def __init__(self, screen: pygame.Surface, block_size: int = 30):
        self.screen = screen
        self.block_size = block_size
        self.board_offset = (50, 50)
        
        self.current_theme_name = 'NEON'
        self._apply_theme('NEON')
        
        # Initialize fonts
        try:
            self.font_title = pygame.font.Font(None, 60)
            self.font_label = pygame.font.Font(None, 36)
            self.font_value = pygame.font.Font(None, 48)
        except:
            self.font_title = pygame.font.SysFont('Arial', 60, bold=True)
            self.font_label = pygame.font.SysFont('Arial', 30)
            self.font_value = pygame.font.SysFont('Arial', 40, bold=True)

    def _apply_theme(self, theme_name):
        """Apply the selected theme colors."""
        theme = self.THEMES[theme_name]
        self.COLOR_BG = theme['BG']
        self.COLOR_GRID = theme['GRID']
        self.COLOR_PANEL = theme['PANEL']
        self.COLOR_TEXT = theme['TEXT']
        self.COLOR_TEXT_WHITE = theme['TEXT_WHITE']
        self.PIECE_COLORS = theme['PIECES']

    def cycle_theme(self):
        """Switch to the next theme."""
        theme_names = list(self.THEMES.keys())
        idx = theme_names.index(self.current_theme_name)
        new_idx = (idx + 1) % len(theme_names)
        self.current_theme_name = theme_names[new_idx]
        self._apply_theme(self.current_theme_name)
        return self.current_theme_name

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

    def draw_board(self, board: Board):
        """Draw the game board with grid and locked pieces."""
        board_rect = pygame.Rect(
            self.board_offset[0], 
            self.board_offset[1], 
            board.WIDTH * self.block_size, 
            board.HEIGHT * self.block_size
        )
        pygame.draw.rect(self.screen, (20, 20, 35) if self.current_theme_name == 'NEON' else self.COLOR_PANEL, board_rect)
        pygame.draw.rect(self.screen, self.COLOR_TEXT, board_rect, 2)

        for x in range(board.WIDTH):
            start = (self.board_offset[0] + x * self.block_size, self.board_offset[1])
            end = (self.board_offset[0] + x * self.block_size, self.board_offset[1] + board.HEIGHT * self.block_size)
            pygame.draw.line(self.screen, self.COLOR_GRID, start, end, 1)
        
        for y in range(board.HEIGHT):
            start = (self.board_offset[0], self.board_offset[1] + y * self.block_size)
            end = (self.board_offset[0] + board.WIDTH * self.block_size, self.board_offset[1] + y * self.block_size)
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
                    
                    draw_x = self.board_offset[0] + x * self.block_size
                    draw_y = self.board_offset[1] + y * self.block_size
                    self._draw_block(draw_x, draw_y, color)

    def draw_piece(self, piece: Piece, offset_x: int = 0, offset_y: int = 0, ghost: bool = False):
        """Draw a piece."""
        color = self.PIECE_COLORS.get(piece.shape_type, piece.color)
        
        for x, y in piece.get_positions():
            draw_x = self.board_offset[0] + (x + offset_x) * self.block_size
            draw_y = self.board_offset[1] + (y + offset_y) * self.block_size
            
            if draw_y < self.board_offset[1]:
                continue
                
            self._draw_block(draw_x, draw_y, color, ghost=ghost)

    def draw_ui(self, scoring: Scoring, next_piece: Piece):
        """Draw the User Interface."""
        panel_x = 400
        
        title_surf = self.font_title.render("TETRIX", True, self.COLOR_TEXT)
        self.screen.blit(title_surf, (panel_x, 30))

        self._draw_info_box("SCORE", str(scoring.score), panel_x, 100)
        self._draw_info_box("BEST", str(scoring.high_score), panel_x, 200)
        self._draw_info_box("LEVEL", str(scoring.level), panel_x, 300)
        self._draw_info_box("LINES", str(scoring.lines_cleared), panel_x, 400)

        label_surf = self.font_label.render("NEXT", True, self.COLOR_TEXT_WHITE)
        self.screen.blit(label_surf, (panel_x, 500))
        
        preview_rect = pygame.Rect(panel_x, 540, 150, 150)
        pygame.draw.rect(self.screen, self.COLOR_PANEL, preview_rect, 0, 10)
        pygame.draw.rect(self.screen, self.COLOR_GRID, preview_rect, 2, 10)

        center_x = panel_x + 75
        center_y = 540 + 75
        prev_block_size = self.block_size 

        shape = next_piece.shape
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
            
            color = self.PIECE_COLORS.get(next_piece.shape_type, next_piece.color)
            
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

    def draw_game_over(self):
        """Draw game over overlay."""
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        go_surf = self.font_title.render("GAME OVER", True, self.COLOR_TEXT)
        go_rect = go_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 40))
        self.screen.blit(go_surf, go_rect)

        restart_surf = self.font_label.render("Press 'R' to Restart", True, self.COLOR_TEXT_WHITE)
        restart_rect = restart_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 40))
        self.screen.blit(restart_surf, restart_rect)
        
        menu_surf = self.font_label.render("Press 'ESC' for Menu", True, self.COLOR_TEXT_WHITE)
        menu_rect = menu_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 80))
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