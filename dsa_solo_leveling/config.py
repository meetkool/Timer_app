"""
Configuration settings for DSA Solo Leveling Application
"""

# Application settings
APP_NAME = "DSA Solo Leveling"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "A gamified DSA learning experience"

# Display settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60
FULLSCREEN = False

# File paths
DATA_FILE = "dsa_queastions.json"
PROGRESS_FILE = "progress.json"
PLAYER_STATS_FILE = "player_stats.json"
ICON_FILE = "icon.ico"

# Game mechanics
BASE_EXP_PER_LEVEL = 100
EXP_MULTIPLIER = 1.2
EXP_REWARDS = {
    0: 10,  # Beginner
    1: 15,  # Easy
    2: 25,  # Medium
    3: 40,  # Hard
}

# UI settings
SCROLL_SPEED = 30
ANIMATION_SPEED = 0.05
CARD_WIDTH = 350
CARD_HEIGHT = 120
COMPONENT_PADDING = 10
COMPONENT_MARGIN = 5

# Theme settings
ENABLE_ANIMATIONS = True
ENABLE_SOUND_EFFECTS = False  # For future implementation
DEBUG_MODE = False

# Rank thresholds
RANK_THRESHOLDS = {
    'E-Rank Hunter': 0,
    'D-Rank Hunter': 10,
    'C-Rank Hunter': 20,
    'B-Rank Hunter': 30,
    'A-Rank Hunter': 40,
    'S-Rank Hunter': 50,
}

# Color themes (for future theme switching)
THEMES = {
    'dark': {
        'primary_bg': (15, 15, 25),
        'secondary_bg': (25, 25, 35),
        'text_primary': (220, 220, 220),
        'accent': (100, 150, 255),
    },
    'light': {
        'primary_bg': (240, 240, 245),
        'secondary_bg': (230, 230, 235),
        'text_primary': (50, 50, 50),
        'accent': (70, 120, 200),
    }
}

DEFAULT_THEME = 'dark'