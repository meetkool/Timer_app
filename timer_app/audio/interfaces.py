"""
Audio System Interfaces - Following Interface Segregation Principle (SOLID)
Each interface has a specific responsibility and clients only depend on what they need.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Callable
from enum import Enum


class RepeatMode(Enum):
    """Enum for different repeat modes"""
    OFF = "off"
    SINGLE = "single"  # Repeat current track
    PLAYLIST = "playlist"  # Repeat entire playlist


class PlaybackState(Enum):
    """Enum for playback states"""
    STOPPED = "stopped"
    PLAYING = "playing"
    PAUSED = "paused"


class TrackInfo:
    """Data class for track information"""
    def __init__(self, path: str, title: str = "", artist: str = "", duration: float = 0.0):
        self.path = path
        self.title = title or "Unknown"
        self.artist = artist or "Unknown"
        self.duration = duration
        self.metadata = {}


class AudioPlayerInterface(ABC):
    """Interface for basic audio playback operations (Single Responsibility)"""
    
    @abstractmethod
    def load_track(self, track: TrackInfo) -> bool:
        """Load a track for playback"""
        pass
    
    @abstractmethod
    def play(self) -> bool:
        """Start playback of loaded track"""
        pass
    
    @abstractmethod
    def pause(self) -> bool:
        """Pause playback"""
        pass
    
    @abstractmethod
    def resume(self) -> bool:
        """Resume paused playback"""
        pass
    
    @abstractmethod
    def stop(self) -> bool:
        """Stop playback"""
        pass
    
    @abstractmethod
    def set_volume(self, volume: float) -> bool:
        """Set volume (0.0 to 1.0)"""
        pass
    
    @abstractmethod
    def get_state(self) -> PlaybackState:
        """Get current playback state"""
        pass
    
    @abstractmethod
    def is_track_finished(self) -> bool:
        """Check if current track has finished playing"""
        pass


class PlaylistInterface(ABC):
    """Interface for playlist management (Single Responsibility)"""
    
    @abstractmethod
    def add_track(self, track: TrackInfo) -> None:
        """Add track to playlist"""
        pass
    
    @abstractmethod
    def remove_track(self, index: int) -> bool:
        """Remove track at index"""
        pass
    
    @abstractmethod
    def get_track(self, index: int) -> Optional[TrackInfo]:
        """Get track at index"""
        pass
    
    @abstractmethod
    def get_current_index(self) -> int:
        """Get current track index"""
        pass
    
    @abstractmethod
    def set_current_index(self, index: int) -> bool:
        """Set current track index"""
        pass
    
    @abstractmethod
    def get_playlist_size(self) -> int:
        """Get total number of tracks"""
        pass
    
    @abstractmethod
    def clear_playlist(self) -> None:
        """Clear all tracks"""
        pass


class LoopControlInterface(ABC):
    """Interface for loop control operations (Single Responsibility)"""
    
    @abstractmethod
    def set_repeat_mode(self, mode: RepeatMode) -> None:
        """Set repeat mode"""
        pass
    
    @abstractmethod
    def get_repeat_mode(self) -> RepeatMode:
        """Get current repeat mode"""
        pass
    
    @abstractmethod
    def handle_track_finished(self) -> Optional[int]:
        """Handle track finished event, return next track index or None to stop"""
        pass


class PlaybackEventInterface(ABC):
    """Interface for playback event handling (Single Responsibility)"""
    
    @abstractmethod
    def on_track_started(self, track: TrackInfo, index: int) -> None:
        """Called when a track starts playing"""
        pass
    
    @abstractmethod
    def on_track_finished(self, track: TrackInfo, index: int) -> None:
        """Called when a track finishes playing"""
        pass
    
    @abstractmethod
    def on_playback_paused(self, track: TrackInfo, index: int) -> None:
        """Called when playback is paused"""
        pass
    
    @abstractmethod
    def on_playback_resumed(self, track: TrackInfo, index: int) -> None:
        """Called when playback is resumed"""
        pass
    
    @abstractmethod
    def on_playback_stopped(self) -> None:
        """Called when playback is stopped"""
        pass
    
    @abstractmethod
    def on_repeat_mode_changed(self, mode: RepeatMode) -> None:
        """Called when repeat mode changes"""
        pass


class AudioSystemInterface(ABC):
    """Main interface that coordinates all audio operations (Facade Pattern)"""
    
    @abstractmethod
    def load_and_play_track(self, index: int) -> bool:
        """Load and play track at index"""
        pass
    
    @abstractmethod
    def pause_playback(self) -> bool:
        """Pause current playback"""
        pass
    
    @abstractmethod
    def resume_playback(self) -> bool:
        """Resume current playback"""
        pass
    
    @abstractmethod
    def stop_playback(self) -> bool:
        """Stop current playback"""
        pass
    
    @abstractmethod
    def next_track(self) -> bool:
        """Move to next track"""
        pass
    
    @abstractmethod
    def previous_track(self) -> bool:
        """Move to previous track"""
        pass
    
    @abstractmethod
    def set_volume(self, volume: float) -> bool:
        """Set playback volume"""
        pass
    
    @abstractmethod
    def cycle_repeat_mode(self) -> RepeatMode:
        """Cycle through repeat modes"""
        pass
    
    @abstractmethod
    def add_track(self, track: TrackInfo) -> None:
        """Add track to playlist"""
        pass
    
    @abstractmethod
    def get_current_track(self) -> Optional[TrackInfo]:
        """Get current track info"""
        pass
    
    @abstractmethod
    def get_status(self) -> Dict:
        """Get current system status"""
        pass
    
    @abstractmethod
    def start_monitoring(self) -> None:
        """Start monitoring playback for automatic progression"""
        pass
    
    @abstractmethod
    def stop_monitoring(self) -> None:
        """Stop monitoring playback"""
        pass
    
    @abstractmethod
    def toggle_shuffle(self) -> bool:
        """Toggle shuffle mode on/off"""
        pass
    
    @abstractmethod
    def is_shuffle_enabled(self) -> bool:
        """Check if shuffle is currently enabled"""
        pass