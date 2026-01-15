"""
Menu module for Tetrix.
Handles the main menu interface and logic.
"""

import pygame

class MainMenu:
    """
    Handles the game's main menu and sub-menus.
    """
    
    OPTIONS = ["START GAME", "HIGH SCORES", "THEMES", "EXIT"]
    THEME_OPTIONS = ["NEON", "PASTEL", "RETRO"]

    def __init__(self, screen, renderer, scoring, sound_manager):
        self.screen = screen
        self.renderer = renderer
        self.scoring = scoring
        self.audio = sound_manager
        
        self.selected_index = 0
        self.selected_theme_index = 0
        
        self.font_large = pygame.font.SysFont('Arial', 80, bold=True)
        self.font_option = pygame.font.SysFont('Arial', 40)
        self.font_small = pygame.font.SysFont('Arial', 24)
        
        # State: MAIN, SCORES, THEMES
        self.menu_state = 'MAIN'
        
        # Sync selected theme index with current theme
        current = self.renderer.current_theme_name
        if current in self.THEME_OPTIONS:
            self.selected_theme_index = self.THEME_OPTIONS.index(current)
        
        # Animation
        self.pulse_timer = 0

    def update(self):
        """Update menu state (animations)."""
        self.pulse_timer += 0.1

    def handle_input(self, events):
        """Handle menu input."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                
                # --- HIGH SCORES STATE ---
                if self.menu_state == 'SCORES':
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        self.menu_state = 'MAIN'
                        self.audio.play('move')
                    return None

                # --- THEMES STATE ---
                elif self.menu_state == 'THEMES':
                    if event.key == pygame.K_ESCAPE:
                        self.menu_state = 'MAIN'
                        self.audio.play('move')
                        # Revert if not confirmed? No, let's keep it live preview
                    elif event.key == pygame.K_RETURN:
                        self.menu_state = 'MAIN'
                        self.audio.play('drop')
                    elif event.key == pygame.K_UP:
                        self.selected_theme_index = (self.selected_theme_index - 1) % len(self.THEME_OPTIONS)
                        self._apply_preview_theme()
                        self.audio.play('move')
                    elif event.key == pygame.K_DOWN:
                        self.selected_theme_index = (self.selected_theme_index + 1) % len(self.THEME_OPTIONS)
                        self._apply_preview_theme()
                        self.audio.play('move')
                    return None

                # --- MAIN MENU STATE ---
                else:
                    if event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(self.OPTIONS)
                        self.audio.play('move')
                    elif event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(self.OPTIONS)
                        self.audio.play('move')
                    elif event.key == pygame.K_RETURN:
                        self.audio.play('drop')
                        return self._trigger_option()
        return None

    def _apply_preview_theme(self):
        """Apply the currently highlighted theme."""
        theme_name = self.THEME_OPTIONS[self.selected_theme_index]
        self.renderer.set_theme(theme_name)

    def _trigger_option(self):
        """Execute the selected option."""
        selection = self.OPTIONS[self.selected_index]
        
        if selection == "START GAME":
            return "START"
        elif selection == "HIGH SCORES":
            self.menu_state = 'SCORES'
            return None
        elif selection == "THEMES":
            self.menu_state = 'THEMES'
            # Sync index again just in case
            current = self.renderer.current_theme_name
            if current in self.THEME_OPTIONS:
                self.selected_theme_index = self.THEME_OPTIONS.index(current)
            return None
        elif selection == "EXIT":
            return "EXIT"
            
    def draw(self):
        """Render the menu."""
        # Draw background (using current theme bg)
        self.screen.fill(self.renderer.COLOR_BG)
        
        if self.menu_state == 'SCORES':
            self._draw_high_scores()
        elif self.menu_state == 'THEMES':
            self._draw_themes()
        else:
            self._draw_main_menu()

    def _draw_main_menu(self):
        # Title
        title_surf = self.font_large.render("TETRIX", True, self.renderer.COLOR_TEXT)
        title_rect = title_surf.get_rect(center=(self.screen.get_width() // 2, 150))
        
        # Simple pulsing effect for title
        scale = 1.0 + 0.05 * abs(pygame.math.Vector2(0, 0).distance_to((0, 0.5 * self.pulse_timer % 10))) 
        
        self.screen.blit(title_surf, title_rect)

        # High Score Mini Display
        score_text = self.font_small.render(f"BEST: {self.scoring.high_score}", True, self.renderer.COLOR_TEXT_WHITE)
        score_rect = score_text.get_rect(center=(self.screen.get_width() // 2, 220))
        self.screen.blit(score_text, score_rect)

        # Options
        start_y = 300
        for i, option in enumerate(self.OPTIONS):
            color = self.renderer.COLOR_TEXT if i == self.selected_index else self.renderer.COLOR_TEXT_WHITE
            
            # Highlight selected
            if i == self.selected_index:
                option = f"> {option} <"
            
            text_surf = self.font_option.render(option, True, color)
            text_rect = text_surf.get_rect(center=(self.screen.get_width() // 2, start_y + i * 60))
            self.screen.blit(text_surf, text_rect)

        # Footer
        footer_text = self.font_small.render("Use ARROW KEYS and ENTER", True, (100, 100, 100))
        footer_rect = footer_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 30))
        self.screen.blit(footer_text, footer_rect)

    def _draw_themes(self):
        """Draw the theme selection screen."""
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100)) # Slight darken on top of new bg color
        self.screen.blit(overlay, (0, 0))
        
        title_surf = self.font_large.render("SELECT THEME", True, self.renderer.COLOR_TEXT)
        title_rect = title_surf.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title_surf, title_rect)

        start_y = 200
        for i, theme in enumerate(self.THEME_OPTIONS):
            is_selected = (i == self.selected_theme_index)
            color = self.renderer.COLOR_TEXT if is_selected else self.renderer.COLOR_TEXT_WHITE
            
            label = f"> {theme} <" if is_selected else theme
            text_surf = self.font_option.render(label, True, color)
            text_rect = text_surf.get_rect(center=(self.screen.get_width() // 2, start_y + i * 120))
            self.screen.blit(text_surf, text_rect)
            
            # Draw Color Preview Palettes
            if is_selected:
                self._draw_theme_preview(start_y + i * 120 + 40, theme)

        back_text = self.font_option.render("Press ENTER to Confirm", True, (150, 150, 150))
        back_rect = back_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 60))
        self.screen.blit(back_text, back_rect)

    def _draw_theme_preview(self, y_pos, theme_name):
        """Draws small blocks showing the theme's palette."""
        theme = self.renderer.THEMES[theme_name]
        pieces = ['I', 'O', 'T', 'S', 'Z']
        
        total_w = len(pieces) * 40
        start_x = (self.screen.get_width() - total_w) // 2
        
        for i, p_type in enumerate(pieces):
            color = theme['PIECES'][p_type]
            rect = pygame.Rect(start_x + i * 40, y_pos, 30, 30)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)

    def _draw_high_scores(self):
        """Draw the high scores screen with a list of top scores."""
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((10, 10, 20, 230))
        self.screen.blit(overlay, (0, 0))
        
        # Title
        title_surf = self.font_large.render("TOP SCORES", True, self.renderer.COLOR_TEXT)
        title_rect = title_surf.get_rect(center=(self.screen.get_width() // 2, 80))
        self.screen.blit(title_surf, title_rect)

        # Table Header
        header_y = 160
        header_font = pygame.font.SysFont('Arial', 24, bold=True)
        col1 = header_font.render("RANK", True, self.renderer.COLOR_TEXT)
        col2 = header_font.render("SCORE", True, self.renderer.COLOR_TEXT)
        col3 = header_font.render("LVL", True, self.renderer.COLOR_TEXT)
        col4 = header_font.render("DATE", True, self.renderer.COLOR_TEXT)
        
        self.screen.blit(col1, (80, header_y))
        self.screen.blit(col2, (180, header_y))
        self.screen.blit(col3, (320, header_y))
        self.screen.blit(col4, (400, header_y))

        # List Scores
        start_y = 200
        for i, entry in enumerate(self.scoring.scores_list):
            y = start_y + i * 35
            color = self.renderer.COLOR_TEXT_WHITE if i > 0 else (255, 215, 0) # Gold for #1
            
            rank = self.font_small.render(f"#{i+1}", True, color)
            score = self.font_small.render(str(entry['score']), True, color)
            level = self.font_small.render(str(entry.get('level', '-')), True, color)
            date = self.font_small.render(str(entry.get('date', '-')), True, color)
            
            self.screen.blit(rank, (80, y))
            self.screen.blit(score, (180, y))
            self.screen.blit(level, (320, y))
            self.screen.blit(date, (400, y))

        if not self.scoring.scores_list:
            empty_surf = self.font_option.render("NO SCORES YET", True, (100, 100, 100))
            empty_rect = empty_surf.get_rect(center=(self.screen.get_width() // 2, 300))
            self.screen.blit(empty_surf, empty_rect)
        
        back_text = self.font_option.render("Press ENTER to Return", True, self.renderer.COLOR_TEXT)
        back_rect = back_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 60))
        self.screen.blit(back_text, back_rect)