"""
Animation system for Tetrix game.
Handles visual effects like line clears, combos, level ups, and floating text.
"""

import pygame
import time
from typing import List, Tuple, Optional

class FloatingText:
    """Represents floating score text that moves upward and fades."""

    def __init__(self, text: str, x: int, y: int, color: Tuple[int, int, int], duration: float = 1.5):
        self.text = text
        self.x = x
        self.y = y
        self.start_y = y
        self.color = color
        self.duration = duration
        self.start_time = time.time()
        self.alpha = 255

    def update(self) -> bool:
        """Update animation. Returns False when animation is complete."""
        elapsed = time.time() - self.start_time
        if elapsed >= self.duration:
            return False

        progress = elapsed / self.duration
        self.y = self.start_y - (progress * 80)  # Move up 80 pixels
        self.alpha = int(255 * (1 - progress))  # Fade out
        return True

    def draw(self, screen: pygame.Surface, font: pygame.font.Font):
        """Draw the floating text."""
        surf = font.render(self.text, True, self.color)
        surf.set_alpha(self.alpha)
        rect = surf.get_rect(center=(self.x, self.y))
        screen.blit(surf, rect)


class LineClearAnimation:
    """Animation for clearing lines with flash effect."""

    def __init__(self, lines: List[int], is_tetris: bool = False):
        self.lines = lines
        self.is_tetris = is_tetris
        self.start_time = time.time()
        self.duration = 0.4 if is_tetris else 0.3
        self.flash_count = 3 if is_tetris else 2

    def update(self) -> bool:
        """Update animation. Returns False when animation is complete."""
        elapsed = time.time() - self.start_time
        return elapsed < self.duration

    def get_alpha(self) -> int:
        """Get current alpha for flash effect."""
        elapsed = time.time() - self.start_time
        flash_period = self.duration / self.flash_count
        flash_progress = (elapsed % flash_period) / flash_period

        # Create pulsing effect
        if flash_progress < 0.5:
            return int(255 * flash_progress * 2)
        else:
            return int(255 * (1 - (flash_progress - 0.5) * 2))

    def draw(self, screen: pygame.Surface, board_offset: Tuple[int, int], block_size: int, board_width: int):
        """Draw the line clear animation."""
        alpha = self.get_alpha()
        color = (255, 255, 255) if self.is_tetris else (255, 255, 255)

        for line_y in self.lines:
            rect = pygame.Rect(
                board_offset[0],
                board_offset[1] + line_y * block_size,
                board_width * block_size,
                block_size
            )

            overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            overlay.fill((*color, alpha))
            screen.blit(overlay, rect.topleft)


class ScreenShake:
    """Screen shake effect for Tetris clears."""

    def __init__(self, intensity: int = 8, duration: float = 0.4):
        self.intensity = intensity
        self.duration = duration
        self.start_time = time.time()

    def update(self) -> bool:
        """Update shake. Returns False when complete."""
        elapsed = time.time() - self.start_time
        return elapsed < self.duration

    def get_offset(self) -> Tuple[int, int]:
        """Get current shake offset."""
        import random
        elapsed = time.time() - self.start_time
        progress = elapsed / self.duration

        # Reduce intensity over time
        current_intensity = self.intensity * (1 - progress)

        offset_x = random.randint(-int(current_intensity), int(current_intensity))
        offset_y = random.randint(-int(current_intensity), int(current_intensity))

        return offset_x, offset_y


class LevelUpAnimation:
    """Animation for level up with flash and text."""

    def __init__(self, level: int):
        self.level = level
        self.start_time = time.time()
        self.duration = 2.0

    def update(self) -> bool:
        """Update animation. Returns False when complete."""
        elapsed = time.time() - self.start_time
        return elapsed < self.duration

    def draw(self, screen: pygame.Surface, font_title: pygame.font.Font, font_label: pygame.font.Font, color: Tuple[int, int, int]):
        """Draw level up animation."""
        elapsed = time.time() - self.start_time

        # Flash effect for first 0.5 seconds
        if elapsed < 0.5:
            alpha = int(100 * (1 - (elapsed / 0.5)))
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, alpha))
            screen.blit(overlay, (0, 0))

        # Fade in text
        if elapsed < 1.0:
            alpha = int(255 * (elapsed / 1.0))
        # Hold
        elif elapsed < 1.5:
            alpha = 255
        # Fade out
        else:
            alpha = int(255 * (1 - (elapsed - 1.5) / 0.5))

        # Draw text
        level_surf = font_title.render("LEVEL UP!", True, color)
        level_surf.set_alpha(alpha)
        level_rect = level_surf.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 40))
        screen.blit(level_surf, level_rect)

        num_surf = font_label.render(f"Level {self.level}", True, (255, 255, 255))
        num_surf.set_alpha(alpha)
        num_rect = num_surf.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 20))
        screen.blit(num_surf, num_rect)


class ComboAnimation:
    """Animation for displaying combo streak."""

    def __init__(self, combo: int, x: int, y: int):
        self.combo = combo
        self.x = x
        self.y = y
        self.start_time = time.time()
        self.duration = 1.0

    def update(self) -> bool:
        """Update animation. Returns False when complete."""
        elapsed = time.time() - self.start_time
        return elapsed < self.duration

    def draw(self, screen: pygame.Surface, font: pygame.font.Font):
        """Draw combo text."""
        elapsed = time.time() - self.start_time

        # Scale effect
        if elapsed < 0.2:
            scale = 1.0 + (elapsed / 0.2) * 0.5  # Grow to 1.5x
        elif elapsed < 0.4:
            scale = 1.5 - ((elapsed - 0.2) / 0.2) * 0.25  # Shrink to 1.25x
        else:
            scale = 1.25

        # Fade out at the end
        if elapsed > 0.7:
            alpha = int(255 * (1 - (elapsed - 0.7) / 0.3))
        else:
            alpha = 255

        # Create scaled font
        size = int(font.get_height() * scale)
        scaled_font = pygame.font.Font(None, size)

        # Rainbow color based on combo
        if self.combo >= 5:
            color = (255, 0, 255)  # Purple
        elif self.combo >= 3:
            color = (255, 165, 0)  # Orange
        else:
            color = (255, 255, 0)  # Yellow

        text = f"COMBO x{self.combo}!"
        surf = scaled_font.render(text, True, color)
        surf.set_alpha(alpha)
        rect = surf.get_rect(center=(self.x, self.y))
        screen.blit(surf, rect)


class AnimationManager:
    """Manages all active animations."""

    def __init__(self):
        self.floating_texts: List[FloatingText] = []
        self.line_clear: Optional[LineClearAnimation] = None
        self.screen_shake: Optional[ScreenShake] = None
        self.level_up: Optional[LevelUpAnimation] = None
        self.combo: Optional[ComboAnimation] = None

    def add_floating_text(self, text: str, x: int, y: int, color: Tuple[int, int, int] = (255, 255, 255)):
        """Add floating score text."""
        self.floating_texts.append(FloatingText(text, x, y, color))

    def add_line_clear(self, lines: List[int], is_tetris: bool = False):
        """Add line clear animation."""
        self.line_clear = LineClearAnimation(lines, is_tetris)

    def add_screen_shake(self, intensity: int = 8):
        """Add screen shake effect."""
        self.screen_shake = ScreenShake(intensity)

    def add_level_up(self, level: int):
        """Add level up animation."""
        self.level_up = LevelUpAnimation(level)

    def add_combo(self, combo: int, x: int, y: int):
        """Add combo animation."""
        self.combo = ComboAnimation(combo, x, y)

    def update(self):
        """Update all animations."""
        # Update floating texts
        self.floating_texts = [ft for ft in self.floating_texts if ft.update()]

        # Update line clear
        if self.line_clear and not self.line_clear.update():
            self.line_clear = None

        # Update screen shake
        if self.screen_shake and not self.screen_shake.update():
            self.screen_shake = None

        # Update level up
        if self.level_up and not self.level_up.update():
            self.level_up = None

        # Update combo
        if self.combo and not self.combo.update():
            self.combo = None

    def has_line_clear(self) -> bool:
        """Check if line clear animation is active."""
        return self.line_clear is not None

    def get_screen_offset(self) -> Tuple[int, int]:
        """Get screen shake offset."""
        if self.screen_shake:
            return self.screen_shake.get_offset()
        return (0, 0)

    def draw(self, screen: pygame.Surface, board_offset: Tuple[int, int], block_size: int,
             board_width: int, font_title: pygame.font.Font, font_label: pygame.font.Font,
             font_value: pygame.font.Font, text_color: Tuple[int, int, int]):
        """Draw all animations."""
        # Draw line clear animation
        if self.line_clear:
            self.line_clear.draw(screen, board_offset, block_size, board_width)

        # Draw floating texts
        for ft in self.floating_texts:
            ft.draw(screen, font_value)

        # Draw combo
        if self.combo:
            self.combo.draw(screen, font_label)

        # Draw level up (drawn on top of everything)
        if self.level_up:
            self.level_up.draw(screen, font_title, font_label, text_color)
