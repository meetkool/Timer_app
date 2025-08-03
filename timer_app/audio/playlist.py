"""
Playlist Management - Following Single Responsibility Principle (SOLID)
This class only handles playlist operations and track management.
"""
from typing import List, Optional
from .interfaces import PlaylistInterface, TrackInfo


class AudioPlaylist(PlaylistInterface):
    """Concrete implementation of playlist management (Single Responsibility)"""
    
    def __init__(self):
        self._tracks: List[TrackInfo] = []
        self._current_index = 0
        self._shuffle_enabled = False
        self._shuffle_history: List[int] = []  # Track shuffle history to avoid immediate repeats
    
    def add_track(self, track: TrackInfo) -> None:
        """Add track to playlist (Single Responsibility)"""
        self._tracks.append(track)
        print(f"➕ Added to playlist: {track.title}")
    
    def remove_track(self, index: int) -> bool:
        """Remove track at index (Single Responsibility)"""
        if not self._is_valid_index(index):
            print(f"❌ Invalid track index: {index}")
            return False
        
        removed_track = self._tracks.pop(index)
        print(f"➖ Removed from playlist: {removed_track.title}")
        
        # Adjust current index if necessary
        if index < self._current_index:
            self._current_index -= 1
        elif index == self._current_index and self._current_index >= len(self._tracks):
            self._current_index = max(0, len(self._tracks) - 1)
        
        return True
    
    def get_track(self, index: int) -> Optional[TrackInfo]:
        """Get track at index (Single Responsibility)"""
        if self._is_valid_index(index):
            return self._tracks[index]
        return None
    
    def get_current_index(self) -> int:
        """Get current track index (Single Responsibility)"""
        return self._current_index
    
    def set_current_index(self, index: int) -> bool:
        """Set current track index (Single Responsibility)"""
        if self._is_valid_index(index):
            self._current_index = index
            return True
        return False
    
    def get_playlist_size(self) -> int:
        """Get total number of tracks (Single Responsibility)"""
        return len(self._tracks)
    
    def clear_playlist(self) -> None:
        """Clear all tracks (Single Responsibility)"""
        self._tracks.clear()
        self._current_index = 0
        print("🗑️ Playlist cleared")
    
    def get_current_track(self) -> Optional[TrackInfo]:
        """Get current track"""
        return self.get_track(self._current_index)
    
    def next_index(self) -> Optional[int]:
        """Get next track index, None if at end"""
        if self._current_index < len(self._tracks) - 1:
            return self._current_index + 1
        return None
    
    def previous_index(self) -> Optional[int]:
        """Get previous track index, None if at beginning"""
        if self._current_index > 0:
            return self._current_index - 1
        return None
    
    def first_index(self) -> Optional[int]:
        """Get first track index, None if empty"""
        return 0 if self._tracks else None
    
    def last_index(self) -> Optional[int]:
        """Get last track index, None if empty"""
        return len(self._tracks) - 1 if self._tracks else None
    
    def is_empty(self) -> bool:
        """Check if playlist is empty"""
        return len(self._tracks) == 0
    
    def is_at_end(self) -> bool:
        """Check if current index is at the last track"""
        return self._current_index >= len(self._tracks) - 1
    
    def is_at_beginning(self) -> bool:
        """Check if current index is at the first track"""
        return self._current_index == 0
    
    def _is_valid_index(self, index: int) -> bool:
        """Check if index is valid for current playlist"""
        return 0 <= index < len(self._tracks)
    
    def get_all_tracks(self) -> List[TrackInfo]:
        """Get copy of all tracks for display purposes"""
        return self._tracks.copy()
    
    def move_track(self, from_index: int, to_index: int) -> bool:
        """Move track from one position to another (Open/Closed - can extend functionality)"""
        if not (self._is_valid_index(from_index) and 0 <= to_index < len(self._tracks)):
            return False
        
        # Remove track from original position
        track = self._tracks.pop(from_index)
        
        # Insert at new position
        self._tracks.insert(to_index, track)
        
        # Update current index if affected
        if from_index == self._current_index:
            self._current_index = to_index
        elif from_index < self._current_index <= to_index:
            self._current_index -= 1
        elif to_index <= self._current_index < from_index:
            self._current_index += 1
        
        print(f"📦 Moved '{track.title}' from position {from_index} to {to_index}")
        return True
    
    def enable_shuffle(self) -> None:
        """Enable shuffle mode"""
        self._shuffle_enabled = True
        self._shuffle_history.clear()
        print("🔀 Shuffle enabled")
    
    def disable_shuffle(self) -> None:
        """Disable shuffle mode"""
        self._shuffle_enabled = False
        self._shuffle_history.clear()
        print("➡️ Shuffle disabled")
    
    def is_shuffle_enabled(self) -> bool:
        """Check if shuffle is enabled"""
        return self._shuffle_enabled
    
    def get_next_shuffle_index(self) -> Optional[int]:
        """Get next random track index for shuffle mode"""
        if not self._shuffle_enabled or len(self._tracks) <= 1:
            return None
        
        import random
        
        # If we've played all tracks, reset history
        if len(self._shuffle_history) >= len(self._tracks):
            self._shuffle_history.clear()
        
        # Find available tracks (not in recent history)
        available_indices = []
        for i in range(len(self._tracks)):
            if i not in self._shuffle_history[-min(3, len(self._tracks)-1):]:  # Avoid last 3 or total-1 tracks
                available_indices.append(i)
        
        if not available_indices:
            # If no available tracks, just pick any except current
            available_indices = [i for i in range(len(self._tracks)) if i != self._current_index]
        
        if available_indices:
            next_index = random.choice(available_indices)
            self._shuffle_history.append(next_index)
            return next_index
        
        return None