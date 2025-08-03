"""
Modular Audio System - Following SOLID Principles
- Single Responsibility: Each class has one reason to change
- Open/Closed: Open for extension, closed for modification  
- Liskov Substitution: Implementations are substitutable
- Interface Segregation: Clients depend only on what they need
- Dependency Inversion: Depend on abstractions, not concretions
"""

from .factory import AudioSystemFactory
from .interfaces import TrackInfo, RepeatMode, PlaybackState
from .system import ModularAudioSystem

# Public API
__all__ = [
    'AudioSystemFactory',
    'TrackInfo', 
    'RepeatMode',
    'PlaybackState',
    'ModularAudioSystem'
]