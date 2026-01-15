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

    # Color Palette
    COLOR_BG = (26, 26, 46)        # Dark Midnight Blue
    COLOR_GRID = (30, 30, 60)      # Slightly lighter for grid
    COLOR_PANEL = (22, 33, 62)     # Dark Blue for UI Panel
    COLOR_TEXT = (233, 69, 96)     # Red/Pink accent
    COLOR_TEXT_WHITE = (240, 240, 240)
    
    # Piece Colors (Redefined for vibrancy)
    PIECE_COLORS = {
        'I': (0, 240, 240),    # Cyan
        'O': (240, 240, 0),    # Yellow
        'T': (160, 0, 240),    # Purple
        'S': (0, 240, 0),      # Green
        'Z': (240, 0, 0),      # Red
        'J': (0, 0, 240),      # Blue
        'L': (240, 160, 0)     # Orange
    }

    def __init__(self, screen: pygame.Surface, block_size: int = 30):
        self.screen = screen
        self.block_size = block_size
        self.board_offset = (50, 50)
        
        # Initialize fonts
        try:
            self.font_title = pygame.font.Font(None, 60)
            self.font_label = pygame.font.Font(None, 36)
            self.font_value = pygame.font.Font(None, 48)
        except:
            self.font_title = pygame.font.SysFont('Arial', 60, bold=True)
            self.font_label = pygame.font.SysFont('Arial', 30)
            self.font_value = pygame.font.SysFont('Arial', 40, bold=True)

    def _draw_block(self, x, y, color, alpha=255, ghost=False):
        """Helper to draw a single block with 3D effect."""
        rect = pygame.Rect(x, y, self.block_size, self.block_size)
        
        if ghost:
            # Draw outline only for ghost piece
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)
            # Optional: Fill with very low opacity if pygame supported it easily on main surface,
            # but outline is standard for ghost pieces.
            return

        # 1. Base color
        pygame.draw.rect(self.screen, color, rect)

        # 2. Highlights (Top and Left) - Lighter
        highlight_points = [
            (x, y + self.block_size),
            (x, y),
            (x + self.block_size, y)
        ]
        # Make a lighter version of the color
        lighter = tuple(min(255, c + 100) for c in color)
        pygame.draw.lines(self.screen, lighter, False, highlight_points, 2)

        # 3. Shadows (Bottom and Right) - Darker
        shadow_points = [
            (x, y + self.block_size),
            (x + self.block_size, y + self.block_size),
            (x + self.block_size, y)
        ]
        # Make a darker version of the color
        darker = tuple(max(0, c - 80) for c in color)
        pygame.draw.lines(self.screen, darker, False, shadow_points, 2)

        # 4. Inner "gloss" rect (optional, subtle)
        inset = 4
        gloss_rect = pygame.Rect(x + inset, y + inset, self.block_size - inset*2, self.block_size - inset*2)
        # Slightly lighter center
        mid_color = tuple(min(255, c + 30) for c in color)
        pygame.draw.rect(self.screen, mid_color, gloss_rect)

    def draw_board(self, board: Board):
        """Draw the game board with grid and locked pieces."""
        # Draw Board Background
        board_rect = pygame.Rect(
            self.board_offset[0], 
            self.board_offset[1], 
            board.WIDTH * self.block_size, 
            board.HEIGHT * self.block_size
        )
        pygame.draw.rect(self.screen, (20, 20, 35), board_rect)
        pygame.draw.rect(self.screen, self.COLOR_TEXT, board_rect, 2) # Border

        # Draw Grid Lines
        for x in range(board.WIDTH):
            start = (self.board_offset[0] + x * self.block_size, self.board_offset[1])
            end = (self.board_offset[0] + x * self.block_size, self.board_offset[1] + board.HEIGHT * self.block_size)
            pygame.draw.line(self.screen, self.COLOR_GRID, start, end, 1)
        
        for y in range(board.HEIGHT):
            start = (self.board_offset[0], self.board_offset[1] + y * self.block_size)
            end = (self.board_offset[0] + board.WIDTH * self.block_size, self.board_offset[1] + y * self.block_size)
            pygame.draw.line(self.screen, self.COLOR_GRID, start, end, 1)

        # Draw Locked Pieces
        for y, row in enumerate(board.grid):
            for x, val in enumerate(row):
                if val:
                    # Use the color stored in the board's color grid
                    color = board.colors[y][x]
                    if not color:
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
            
            # Don't draw if above the board (hidden area)
            if draw_y < self.board_offset[1]:
                continue
                
            self._draw_block(draw_x, draw_y, color, ghost=ghost)

    def draw_ui(self, scoring: Scoring, next_piece: Piece):
        """Draw the User Interface."""
        # Right Side Panel Area
        panel_x = 400
        panel_y = 50
        
        # 1. Title
        title_surf = self.font_title.render("TETRIX", True, self.COLOR_TEXT)
        self.screen.blit(title_surf, (panel_x, 30))

        # 2. Score Box
        self._draw_info_box("SCORE", str(scoring.score), panel_x, 100)
        
        # New: High Score Box
        self._draw_info_box("BEST", str(scoring.high_score), panel_x, 200)
        
        # 3. Level Box
        self._draw_info_box("LEVEL", str(scoring.level), panel_x, 300)
        
        # 4. Lines Box
        self._draw_info_box("LINES", str(scoring.lines_cleared), panel_x, 400)

        # 5. Next Piece Box
        label_surf = self.font_label.render("NEXT", True, self.COLOR_TEXT_WHITE)
        self.screen.blit(label_surf, (panel_x, 500))
        
        # Next Piece Preview Background
        preview_rect = pygame.Rect(panel_x, 540, 150, 150)
        pygame.draw.rect(self.screen, self.COLOR_PANEL, preview_rect, 0, 10) # Rounded corners
        pygame.draw.rect(self.screen, self.COLOR_GRID, preview_rect, 2, 10)

        # Draw Next Piece centered
        # Calculate center of preview box
        center_x = panel_x + 75
        center_y = 540 + 75  # Updated to match new box Y position (was 440)
        
        # Get piece dimensions to center it
        # This is a rough centering, can be improved based on exact shape bounding box
        # Standard block size in preview is usually same or slightly smaller
        prev_block_size = self.block_size 
        
        for x, y in next_piece.get_positions():
            # Adjust local coordinates (piece positions are absolute usually, need relative to piece 'center')
            # But get_positions() returns absolute board coords based on piece.position.
            # We need the relative shape coordinates.
            pass

        # Use raw shape data for preview rendering to avoid position artifacts
        shape = next_piece.shape
        # Find bounds of the shape
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
                        
                        # Use a simpler draw for preview or same block style
                        rect = pygame.Rect(draw_x, draw_y, prev_block_size, prev_block_size)
                        pygame.draw.rect(self.screen, color, rect)
                        pygame.draw.rect(self.screen, (255,255,255), rect, 1)


    def _draw_info_box(self, label, value, x, y):
        """Helper to draw a standardized info box."""
        # Label
        label_surf = self.font_label.render(label, True, self.COLOR_TEXT_WHITE)
        self.screen.blit(label_surf, (x, y))
        
        # Value Background
        val_rect = pygame.Rect(x, y + 30, 150, 50)
        pygame.draw.rect(self.screen, self.COLOR_PANEL, val_rect, 0, 8)
        
        # Value Text
        val_surf = self.font_value.render(value, True, self.COLOR_TEXT)
        val_rect_text = val_surf.get_rect(center=val_rect.center)
        self.screen.blit(val_surf, val_rect_text)

    def draw_game_over(self):
        """Draw game over overlay."""
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((20, 20, 30, 220))  # Dark semi-transparent
        self.screen.blit(overlay, (0, 0))

        # Game Over Text
        go_surf = self.font_title.render("GAME OVER", True, self.COLOR_TEXT)
        go_rect = go_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 40))
        
        # Shadow for text
        shadow_surf = self.font_title.render("GAME OVER", True, (0, 0, 0))
        shadow_rect = shadow_surf.get_rect(center=(self.screen.get_width() // 2 + 2, self.screen.get_height() // 2 - 38))
        self.screen.blit(shadow_surf, shadow_rect)
        self.screen.blit(go_surf, go_rect)

        # Restart Text
        restart_surf = self.font_label.render("Press 'R' to Restart", True, self.COLOR_TEXT_WHITE)
        restart_rect = restart_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 40))
        self.screen.blit(restart_surf, restart_rect)

    def draw_pause(self):
        """Draw pause overlay."""
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Black semi-transparent
        self.screen.blit(overlay, (0, 0))

        # Pause Text
        pause_surf = self.font_title.render("PAUSED", True, (255, 255, 255))
        pause_rect = pause_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        
        # Shadow
        shadow_surf = self.font_title.render("PAUSED", True, (0, 0, 0))
        shadow_rect = shadow_surf.get_rect(center=(self.screen.get_width() // 2 + 2, self.screen.get_height() // 2 + 2))
        
        self.screen.blit(shadow_surf, shadow_rect)
        self.screen.blit(pause_surf, pause_rect)
