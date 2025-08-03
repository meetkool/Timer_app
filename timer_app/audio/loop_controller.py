"""
Loop Control Management - Following Single Responsibility and Open/Closed Principles (SOLID)
This class only handles loop logic and repeat mode operations.
"""
from typing import Optional
from .interfaces import LoopControlInterface, PlaylistInterface, RepeatMode


class LoopController(LoopControlInterface):
    """Concrete implementation of loop control (Single Responsibility, Open/Closed)"""
    
    def __init__(self, playlist: PlaylistInterface):
        self._playlist = playlist
        self._repeat_mode = RepeatMode.OFF
    
    def set_repeat_mode(self, mode: RepeatMode) -> None:
        """Set repeat mode (Single Responsibility)"""
        self._repeat_mode = mode
        print(f"🔄 Repeat mode: {mode.value.upper()}")
    
    def get_repeat_mode(self) -> RepeatMode:
        """Get current repeat mode (Single Responsibility)"""
        return self._repeat_mode
    
    def handle_track_finished(self) -> Optional[int]:
        """
        Handle track finished event and return next track index (Single Responsibility)
        
        Returns:
            int: Next track index to play
            None: Stop playback
        """
        current_index = self._playlist.get_current_index()
        
        if self._repeat_mode == RepeatMode.SINGLE:
            print("🔂 Single repeat - playing same track")
            return current_index  # Repeat current track
        
        elif self._repeat_mode == RepeatMode.PLAYLIST:
            return self._handle_playlist_repeat(current_index)
        
        else:  # RepeatMode.OFF
            return self._handle_no_repeat(current_index)
    
    def _handle_playlist_repeat(self, current_index: int) -> Optional[int]:
        """Handle playlist repeat logic (Open/Closed - can extend with new repeat types)"""
        if self._playlist.is_at_end():
            print("🔁 Playlist repeat - back to first track")
            first_index = self._playlist.first_index()
            if first_index is not None:
                self._playlist.set_current_index(first_index)
                return first_index
            return None
        else:
            next_index = self._playlist.next_index()
            if next_index is not None:
                print(f"🔁 Playlist repeat - next track ({next_index})")
                self._playlist.set_current_index(next_index)
                return next_index
            return None
    
    def _handle_no_repeat(self, current_index: int) -> Optional[int]:
        """Handle no repeat logic (Open/Closed - can extend with new behaviors)"""
        if not self._playlist.is_at_end():
            next_index = self._playlist.next_index()
            if next_index is not None:
                print(f"▶️ No repeat - next track ({next_index})")
                self._playlist.set_current_index(next_index)
                return next_index
        
        print("⏹️ No repeat - end of playlist, stopping")
        return None
    
    def get_next_track_index(self) -> Optional[int]:
        """Get what the next track index would be without changing state"""
        current_index = self._playlist.get_current_index()
        
        if self._repeat_mode == RepeatMode.SINGLE:
            return current_index
        
        elif self._repeat_mode == RepeatMode.PLAYLIST:
            if self._playlist.is_at_end():
                return self._playlist.first_index()
            else:
                return self._playlist.next_index()
        
        else:  # RepeatMode.OFF
            return self._playlist.next_index()
    
    def get_previous_track_index(self) -> Optional[int]:
        """Get what the previous track index would be without changing state"""
        if self._repeat_mode == RepeatMode.PLAYLIST:
            if self._playlist.is_at_beginning():
                return self._playlist.last_index()
            else:
                return self._playlist.previous_index()
        else:
            return self._playlist.previous_index()
    
    def cycle_repeat_mode(self) -> RepeatMode:
        """Cycle through repeat modes (Open/Closed - easy to add new modes)"""
        modes = [RepeatMode.OFF, RepeatMode.SINGLE, RepeatMode.PLAYLIST]
        current_idx = modes.index(self._repeat_mode)
        next_mode = modes[(current_idx + 1) % len(modes)]
        self.set_repeat_mode(next_mode)
        return next_mode
    
    def get_repeat_mode_display(self) -> str:
        """Get display string for current repeat mode"""
        display_map = {
            RepeatMode.OFF: "🔇 No Repeat",
            RepeatMode.SINGLE: "🔂 Repeat Track", 
            RepeatMode.PLAYLIST: "🔁 Repeat Playlist"
        }
        return display_map.get(self._repeat_mode, "❓ Unknown")
    
    def should_continue_playback(self) -> bool:
        """Check if playback should continue based on current state"""
        if self._playlist.is_empty():
            return False
        
        if self._repeat_mode == RepeatMode.SINGLE:
            return True  # Single repeat always continues
        
        if self._repeat_mode == RepeatMode.PLAYLIST:
            return True  # Playlist repeat always continues
        
        # RepeatMode.OFF - only continue if not at end
        return not self._playlist.is_at_end()