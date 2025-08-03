"""
Concrete Audio Player Implementation - Following Single Responsibility Principle (SOLID)
This class only handles the core audio playback functionality.
"""
import pygame
import os
from typing import Optional
from .interfaces import AudioPlayerInterface, TrackInfo, PlaybackState


class PygameAudioPlayer(AudioPlayerInterface):
    """Concrete implementation of audio player using pygame (Single Responsibility)"""
    
    def __init__(self):
        self._current_track: Optional[TrackInfo] = None
        self._state = PlaybackState.STOPPED
        self._volume = 0.7
        self._pygame_ready = False
        self._init_pygame()
    
    def _init_pygame(self) -> None:
        """Initialize pygame mixer"""
        try:
            pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=1024)
            pygame.mixer.init()
            self._pygame_ready = True
            print("🎵 Pygame audio player initialized")
        except Exception as e:
            print(f"❌ Failed to initialize pygame audio: {e}")
            self._pygame_ready = False
    
    def load_track(self, track: TrackInfo) -> bool:
        """Load a track for playback (Single Responsibility)"""
        if not self._pygame_ready:
            print("❌ Pygame not ready")
            return False
        
        if not os.path.exists(track.path):
            print(f"❌ Track file not found: {track.path}")
            return False
        
        try:
            pygame.mixer.music.load(track.path)
            self._current_track = track
            print(f"✅ Loaded track: {track.title}")
            return True
        except Exception as e:
            print(f"❌ Failed to load track {track.path}: {e}")
            return False
    
    def play(self) -> bool:
        """Start playback of loaded track (Single Responsibility)"""
        if not self._pygame_ready or not self._current_track:
            print("❌ No track loaded or pygame not ready")
            return False
        
        try:
            pygame.mixer.music.set_volume(self._volume)
            pygame.mixer.music.play()
            self._state = PlaybackState.PLAYING
            print(f"▶️ Playing: {self._current_track.title}")
            return True
        except Exception as e:
            print(f"❌ Playback error: {e}")
            return False
    
    def pause(self) -> bool:
        """Pause playback (Single Responsibility)"""
        if not self._pygame_ready or self._state != PlaybackState.PLAYING:
            return False
        
        try:
            pygame.mixer.music.pause()
            self._state = PlaybackState.PAUSED
            print("⏸️ Paused")
            return True
        except Exception as e:
            print(f"❌ Pause error: {e}")
            return False
    
    def resume(self) -> bool:
        """Resume paused playback (Single Responsibility)"""
        if not self._pygame_ready or self._state != PlaybackState.PAUSED:
            return False
        
        try:
            pygame.mixer.music.unpause()
            self._state = PlaybackState.PLAYING
            print("▶️ Resumed")
            return True
        except Exception as e:
            print(f"❌ Resume error: {e}")
            return False
    
    def stop(self) -> bool:
        """Stop playback (Single Responsibility)"""
        if not self._pygame_ready:
            return False
        
        try:
            pygame.mixer.music.stop()
            self._state = PlaybackState.STOPPED
            print("⏹️ Stopped")
            return True
        except Exception as e:
            print(f"❌ Stop error: {e}")
            return False
    
    def set_volume(self, volume: float) -> bool:
        """Set volume (Single Responsibility)"""
        if not 0.0 <= volume <= 1.0:
            print(f"❌ Invalid volume: {volume}. Must be between 0.0 and 1.0")
            return False
        
        self._volume = volume
        
        if self._pygame_ready:
            try:
                pygame.mixer.music.set_volume(self._volume)
                print(f"🔊 Volume: {int(self._volume * 100)}%")
                return True
            except Exception as e:
                print(f"❌ Volume error: {e}")
                return False
        
        return True  # Volume stored for when pygame becomes ready
    
    def get_state(self) -> PlaybackState:
        """Get current playback state (Single Responsibility)"""
        return self._state
    
    def is_track_finished(self) -> bool:
        """Check if current track has finished playing (Single Responsibility)"""
        if not self._pygame_ready:
            return False
        
        try:
            # Track is finished if not busy and not paused
            return not pygame.mixer.music.get_busy() and self._state != PlaybackState.PAUSED
        except Exception:
            return False
    
    def get_current_track(self) -> Optional[TrackInfo]:
        """Get currently loaded track"""
        return self._current_track
    
    def cleanup(self) -> None:
        """Clean up resources"""
        if self._pygame_ready:
            try:
                pygame.mixer.music.stop()
                pygame.mixer.quit()
                print("🧹 Audio player cleaned up")
            except Exception as e:
                print(f"⚠️ Cleanup warning: {e}")