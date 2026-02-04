"""
Audio module for Tetrix.
Handles loading and playing sound effects.
"""

import pygame
import os

class SoundManager:
    """
    Manages game sound effects.
    """
    
    def __init__(self):
        self.sounds = {}
        self.enabled = True
        try:
            pygame.mixer.init()
            self._load_sounds()
        except Exception as e:
            print(f"Warning: Audio system failed to initialize. {e}")
            self.enabled = False

    def _load_sounds(self):
        """Load sound files from assets directory."""
        sound_files = {
            'move': 'move.wav',
            'rotate': 'rotate.wav',
            'drop': 'drop.wav',
            'clear': 'clear.wav',
            'gameover': 'gameover.wav',
            'combo': 'combo.wav',
            'levelup': 'levelup.wav',
            'tetris': 'tetris.wav',
            'hold': 'move.wav'  # Reuse move sound for hold
        }
        
        base_path = os.path.join('assets', 'sounds')
        
        for name, filename in sound_files.items():
            path = os.path.join(base_path, filename)
            if os.path.exists(path):
                try:
                    self.sounds[name] = pygame.mixer.Sound(path)
                    # Adjust volumes
                    if name == 'move':
                        self.sounds[name].set_volume(0.4)
                    elif name == 'rotate':
                        self.sounds[name].set_volume(0.5)
                    elif name == 'clear':
                        self.sounds[name].set_volume(0.6)
                    elif name == 'combo':
                        self.sounds[name].set_volume(0.7)
                    elif name == 'levelup':
                        self.sounds[name].set_volume(0.8)
                    elif name == 'tetris':
                        self.sounds[name].set_volume(0.8)
                except Exception as e:
                    print(f"Failed to load sound {filename}: {e}")
            else:
                print(f"Sound file not found: {path}")

    def play(self, sound_name: str):
        """Play a sound effect by name."""
        if not self.enabled:
            return
            
        sound = self.sounds.get(sound_name)
        if sound:
            try:
                sound.play()
            except:
                pass
