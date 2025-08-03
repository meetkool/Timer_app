"""
DSA Solo Leveling - A gamified DSA learning application

This package provides a comprehensive DSA learning experience
inspired by the Solo Leveling manhwa, featuring:

- Structured learning paths (dungeons)
- Progress tracking and achievements
- Ranking system with experience points
- Interactive UI with solo leveling theme
- SOLID principles implementation

Author: Assistant
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Assistant"
__email__ = "assistant@example.com"

# Package imports for easy access
from .models.data_models import (
    Step, SubStep, Topic, PlayerStats, 
    QuestStatus, DifficultyLevel,
    JSONDataLoader, ProgressTracker
)

from .ui.components import (
    Button, ProgressBar, Dropdown, 
    ChecklistItem, StepCard, PlayerStatsPanel,
    ComponentStyle, ComponentState
)

from .ui.views import (
    MainDashboard, QuestView, TopicDetailView
)

from .ui.theme import SoloLevelingTheme, ColorScheme, theme

__all__ = [
    # Data models
    'Step', 'SubStep', 'Topic', 'PlayerStats',
    'QuestStatus', 'DifficultyLevel',
    'JSONDataLoader', 'ProgressTracker',
    
    # UI Components
    'Button', 'ProgressBar', 'Dropdown',
    'ChecklistItem', 'StepCard', 'PlayerStatsPanel',
    'ComponentStyle', 'ComponentState',
    
    # Views
    'MainDashboard', 'QuestView', 'TopicDetailView',
    
    # Theme
    'SoloLevelingTheme', 'ColorScheme', 'theme'
]