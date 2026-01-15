"""
Settings module for Tetrix.
Handles persistence of game configuration (themes, audio, etc).
"""

import os
import json

class Settings:
    """
    Manages game settings persistence.
    """
    
    SETTINGS_FILE = os.path.join('data', 'settings.json')
    
    DEFAULTS = {
        'theme': 'NEON',
        'sound_volume': 1.0,
        'music_volume': 0.5
    }

    def __init__(self):
        self.config = self._load_settings()

    def _load_settings(self):
        """Load settings from disk or use defaults."""
        if os.path.exists(self.SETTINGS_FILE):
            try:
                with open(self.SETTINGS_FILE, 'r') as f:
                    data = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    config = self.DEFAULTS.copy()
                    config.update(data)
                    return config
            except:
                return self.DEFAULTS.copy()
        return self.DEFAULTS.copy()

    def save_settings(self):
        """Save current settings to disk."""
        if not os.path.exists('data'):
            os.makedirs('data')
            
        try:
            with open(self.SETTINGS_FILE, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def get(self, key):
        """Get a setting value."""
        return self.config.get(key, self.DEFAULTS.get(key))

    def set(self, key, value):
        """Set a setting value and save."""
        self.config[key] = value
        self.save_settings()
