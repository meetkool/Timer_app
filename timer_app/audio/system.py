"""
Main Audio System - Facade Pattern coordinating all audio components (SOLID)
This class follows Dependency Inversion Principle by depending on interfaces, not concrete classes.
"""
import os
from typing import Optional, Dict, Any
from .interfaces import (
    AudioSystemInterface, TrackInfo, RepeatMode, PlaybackState,
    AudioPlayerInterface, PlaylistInterface, LoopControlInterface, PlaybackEventInterface
)
from .monitor import PlaybackMonitor


class ModularAudioSystem(AudioSystemInterface, PlaybackEventInterface):
    """
    Main audio system that coordinates all components (Facade + Dependency Inversion)
    Also implements PlaybackEventInterface to handle its own events
    """
    
    def __init__(self, 
                 player: AudioPlayerInterface,
                 playlist: PlaylistInterface,
                 loop_controller: LoopControlInterface):
        # Dependency Inversion: Depend on interfaces, not concrete classes
        self._player = player
        self._playlist = playlist
        self._loop_controller = loop_controller
        
        # Create monitor with all dependencies
        self._monitor = PlaybackMonitor(player, playlist, loop_controller, self)
        
        # State tracking
        self._current_status = {
            'is_playing': False,
            'current_track': None,
            'repeat_mode': RepeatMode.OFF,
            'volume': 0.7,
            'shuffle_enabled': False
        }
    
    # AudioSystemInterface implementation (Facade Pattern)
    
    def load_and_play_track(self, index: int) -> bool:
        """Load and play track at index (Facade Pattern)"""
        track = self._playlist.get_track(index)
        if not track:
            print(f"❌ Track at index {index} not found")
            return False
        
        # Update playlist current index
        self._playlist.set_current_index(index)
        
        # Load and play track
        if self._player.load_track(track):
            if self._player.play():
                self._current_status['is_playing'] = True
                self._current_status['current_track'] = track
                
                # Start monitoring for automatic progression
                self._monitor.start_monitoring()
                
                # Trigger event
                self.on_track_started(track, index)
                return True
        
        return False
    
    def pause_playback(self) -> bool:
        """Pause current playback (Facade Pattern)"""
        if self._player.pause():
            self._current_status['is_playing'] = False
            current_track = self._playlist.get_current_track()
            if current_track:
                self.on_playback_paused(current_track, self._playlist.get_current_index())
            return True
        return False
    
    def resume_playback(self) -> bool:
        """Resume current playback (Facade Pattern)"""
        if self._player.resume():
            self._current_status['is_playing'] = True
            current_track = self._playlist.get_current_track()
            if current_track:
                self.on_playback_resumed(current_track, self._playlist.get_current_index())
            return True
        return False
    
    def stop_playback(self) -> bool:
        """Stop current playback (Facade Pattern)"""
        self._monitor.stop_monitoring()
        if self._player.stop():
            self._current_status['is_playing'] = False
            self._current_status['current_track'] = None
            self.on_playback_stopped()
            return True
        return False
    
    def next_track(self) -> bool:
        """Move to next track (Facade Pattern)"""
        next_index = self._loop_controller.get_next_track_index()
        if next_index is not None:
            return self.load_and_play_track(next_index)
        return False
    
    def previous_track(self) -> bool:
        """Move to previous track (Facade Pattern)"""
        prev_index = self._loop_controller.get_previous_track_index()
        if prev_index is not None:
            return self.load_and_play_track(prev_index)
        return False
    
    def set_volume(self, volume: float) -> bool:
        """Set playback volume (Facade Pattern)"""
        if self._player.set_volume(volume):
            self._current_status['volume'] = volume
            return True
        return False
    
    def cycle_repeat_mode(self) -> RepeatMode:
        """Cycle through repeat modes (Facade Pattern)"""
        new_mode = self._loop_controller.cycle_repeat_mode()
        self._current_status['repeat_mode'] = new_mode
        self.on_repeat_mode_changed(new_mode)
        return new_mode
    
    def add_track(self, track: TrackInfo) -> None:
        """Add track to playlist (Facade Pattern)"""
        self._playlist.add_track(track)
    
    def add_track_from_path(self, file_path: str) -> bool:
        """Add track from file path with metadata extraction"""
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return False
        
        # Extract basic info from filename
        filename = os.path.basename(file_path)
        name_without_ext = os.path.splitext(filename)[0]
        
        # Try to parse title - artist from filename
        if " - " in name_without_ext:
            parts = name_without_ext.split(" - ", 1)
            artist, title = parts[0].strip(), parts[1].strip()
        else:
            title, artist = name_without_ext, "Unknown Artist"
        
        track = TrackInfo(path=file_path, title=title, artist=artist)
        self.add_track(track)
        return True
    
    def get_current_track(self) -> Optional[TrackInfo]:
        """Get current track info (Facade Pattern)"""
        return self._playlist.get_current_track()
    
    def get_status(self) -> Dict[str, Any]:
        """Get current system status (Facade Pattern)"""
        current_track = self.get_current_track()
        return {
            'is_playing': self._current_status['is_playing'],
            'playback_state': self._player.get_state().value,
            'current_track': {
                'title': current_track.title if current_track else None,
                'artist': current_track.artist if current_track else None,
                'path': current_track.path if current_track else None
            } if current_track else None,
            'current_index': self._playlist.get_current_index(),
            'playlist_size': self._playlist.get_playlist_size(),
            'repeat_mode': self._loop_controller.get_repeat_mode().value,
            'repeat_display': self._loop_controller.get_repeat_mode_display(),
            'volume': self._current_status['volume'],
            'shuffle_enabled': self.is_shuffle_enabled(),
            'monitor_status': self._monitor.get_status()
        }
    
    def start_monitoring(self) -> None:
        """Start monitoring playback (Facade Pattern)"""
        self._monitor.start_monitoring()
    
    def stop_monitoring(self) -> None:
        """Stop monitoring playback (Facade Pattern)"""
        self._monitor.stop_monitoring()
    
    # PlaybackEventInterface implementation (Observer Pattern)
    
    def on_track_started(self, track: TrackInfo, index: int) -> None:
        """Called when a track starts playing"""
        print(f"🎵 Started: {track.title} by {track.artist}")
    
    def on_track_finished(self, track: TrackInfo, index: int) -> None:
        """Called when a track finishes playing"""
        print(f"🏁 Finished: {track.title}")
    
    def on_playback_paused(self, track: TrackInfo, index: int) -> None:
        """Called when playback is paused"""
        print(f"⏸️ Paused: {track.title}")
    
    def on_playback_resumed(self, track: TrackInfo, index: int) -> None:
        """Called when playback is resumed"""
        print(f"▶️ Resumed: {track.title}")
    
    def on_playback_stopped(self) -> None:
        """Called when playback is stopped"""
        print("⏹️ Playback stopped")
    
    def on_repeat_mode_changed(self, mode: RepeatMode) -> None:
        """Called when repeat mode changes"""
        print(f"🔄 Repeat mode changed: {mode.value}")
    
    # Additional utility methods
    
    def get_playlist_tracks(self) -> list:
        """Get all tracks in playlist for UI display"""
        tracks = []
        for i in range(self._playlist.get_playlist_size()):
            track = self._playlist.get_track(i)
            if track:
                tracks.append({
                    'index': i,
                    'title': track.title,
                    'artist': track.artist,
                    'path': track.path,
                    'is_current': i == self._playlist.get_current_index()
                })
        return tracks
    
    def remove_track(self, index: int) -> bool:
        """Remove track from playlist"""
        return self._playlist.remove_track(index)
    
    def clear_playlist(self) -> None:
        """Clear entire playlist"""
        self.stop_playback()
        self._playlist.clear_playlist()
    
    def toggle_shuffle(self) -> bool:
        """Toggle shuffle mode on/off"""
        if hasattr(self._playlist, 'is_shuffle_enabled'):
            current_shuffle = self._playlist.is_shuffle_enabled()
            if current_shuffle:
                self._playlist.disable_shuffle()
                self._current_status['shuffle_enabled'] = False
                print("🔀 ➡️ Shuffle disabled")
                return False
            else:
                self._playlist.enable_shuffle()
                self._current_status['shuffle_enabled'] = True
                print("➡️ 🔀 Shuffle enabled")
                return True
        return False
    
    def is_shuffle_enabled(self) -> bool:
        """Check if shuffle is currently enabled"""
        if hasattr(self._playlist, 'is_shuffle_enabled'):
            return self._playlist.is_shuffle_enabled()
        return False
    
    def cleanup(self) -> None:
        """Clean up resources"""
        self.stop_playback()
        if hasattr(self._player, 'cleanup'):
            self._player.cleanup()
        print("🧹 Audio system cleaned up")