"""
Menu module for Tetrix.
Handles the main menu interface and logic.
"""

import pygame

class MainMenu:
    """
    Handles the game's main menu.
    """
    
    OPTIONS = ["START GAME", "HIGH SCORES", "THEME: NEON", "EXIT"]

    def __init__(self, screen, renderer, scoring, sound_manager):
        self.screen = screen
        self.renderer = renderer
        self.scoring = scoring
        self.audio = sound_manager
        
        self.selected_index = 0
        self.font_large = pygame.font.SysFont('Arial', 80, bold=True)
        self.font_option = pygame.font.SysFont('Arial', 40)
        self.font_small = pygame.font.SysFont('Arial', 24)
        
        self.showing_scores = False
        
        # Animation
        self.pulse_timer = 0

    def update(self):
        """Update menu state (animations)."""
        self.pulse_timer += 0.1

    def handle_input(self, events):
        """Handle menu input."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.showing_scores:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        self.showing_scores = False
                        self.audio.play('move')
                    return None

                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.OPTIONS)
                    self.audio.play('move')
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.OPTIONS)
                    self.audio.play('move')
                elif event.key == pygame.K_RETURN:
                    self.audio.play('drop') # Confirm sound
                    return self._trigger_option()
        return None

    def _trigger_option(self):
        """Execute the selected option."""
        selection = self.OPTIONS[self.selected_index]
        
        if selection == "START GAME":
            return "START"
        elif selection == "HIGH SCORES":
            self.showing_scores = True
            return None
        elif selection.startswith("THEME"):
            # Cycle theme
            new_theme = self.renderer.cycle_theme()
            self.OPTIONS[2] = f"THEME: {new_theme}"
            return "THEME_CHANGED"
        elif selection == "EXIT":
            return "EXIT"
            
    def draw(self):
        """Render the menu."""
        # Draw background (using current theme bg)
        self.screen.fill(self.renderer.COLOR_BG)
        
        if self.showing_scores:
            self._draw_high_scores()
        else:
            self._draw_main_menu()

    def _draw_main_menu(self):
        # Title
        title_surf = self.font_large.render("TETRIX", True, self.renderer.COLOR_TEXT)
        title_rect = title_surf.get_rect(center=(self.screen.get_width() // 2, 150))
        
        # Simple pulsing effect for title
        scale = 1.0 + 0.05 * abs(pygame.math.Vector2(0, 0).distance_to((0, 0.5 * self.pulse_timer % 10))) 
        # (Simplified pulse logic for now)
        
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

    def _draw_high_scores(self):
        """Draw the high scores screen."""
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        title_surf = self.font_large.render("HIGH SCORE", True, self.renderer.COLOR_TEXT)
        title_rect = title_surf.get_rect(center=(self.screen.get_width() // 2, 150))
        self.screen.blit(title_surf, title_rect)

        score_val = self.font_large.render(str(self.scoring.high_score), True, self.renderer.COLOR_TEXT_WHITE)
        score_rect = score_val.get_rect(center=(self.screen.get_width() // 2, 300))
        self.screen.blit(score_val, score_rect)
        
        back_text = self.font_option.render("Press ENTER to Return", True, (150, 150, 150))
        back_rect = back_text.get_rect(center=(self.screen.get_width() // 2, 500))
        self.screen.blit(back_text, back_rect)
