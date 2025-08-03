"""
Audio Loop Manager - Dedicated system for handling audio looping
Handles playlist looping, single track repeat, and queue management
"""
import pygame
import threading
import time
import json
import os
from typing import List, Dict, Optional, Callable
from enum import Enum

class LoopMode(Enum):
    OFF = "off"
    SINGLE_TRACK = "single_track"  # Loop current song
    PLAYLIST = "playlist"          # Loop entire playlist

class AudioLoopManager:
    """Dedicated audio loop management system"""
    
    def __init__(self, settings_file: str = "audio_loop_settings.json"):
        self.settings_file = settings_file
        
        # Playlist and playback state
        self.playlist: List[Dict] = []
        self.current_index: int = 0
        self.is_playing: bool = False
        self.is_paused: bool = False
        
        # Loop settings
        self.loop_mode: LoopMode = LoopMode.OFF
        self.volume: float = 0.7
        
        # Threading
        self.loop_thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()
        
        # Callbacks for UI updates
        self.on_track_change: Optional[Callable] = None
        self.on_loop_mode_change: Optional[Callable] = None
        
        # Initialize pygame mixer
        self._init_audio()
        self._load_settings()
    
    def _init_audio(self):
        """Initialize pygame mixer for audio playback"""
        try:
            pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=1024)
            pygame.mixer.init()
            print("🎵 Audio Loop Manager initialized successfully")
        except Exception as e:
            print(f"❌ Audio initialization error: {e}")
    
    def _load_settings(self):
        """Load settings from file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.playlist = data.get('playlist', [])
                    self.volume = data.get('volume', 0.7)
                    loop_mode_str = data.get('loop_mode', 'off')
                    self.loop_mode = LoopMode(loop_mode_str)
                    self.current_index = data.get('current_index', 0)
                    
                    # Ensure current_index is valid
                    if self.current_index >= len(self.playlist):
                        self.current_index = 0
                        
                    print(f"🔄 Loaded {len(self.playlist)} tracks, loop mode: {self.loop_mode.value}")
        except Exception as e:
            print(f"⚠️ Settings load error: {e}")
    
    def _save_settings(self):
        """Save current settings to file"""
        try:
            data = {
                'playlist': self.playlist,
                'volume': self.volume,
                'loop_mode': self.loop_mode.value,
                'current_index': self.current_index
            }
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Settings save error: {e}")
    
    def add_track(self, track_info: Dict):
        """Add a track to the playlist"""
        if track_info not in self.playlist:
            self.playlist.append(track_info)
            self._save_settings()
            print(f"➕ Added track: {track_info.get('title', 'Unknown')}")
    
    def set_loop_mode(self, mode: LoopMode):
        """Set the loop mode"""
        self.loop_mode = mode
        self._save_settings()
        print(f"🔄 Loop mode set to: {mode.value}")
        
        if self.on_loop_mode_change:
            self.on_loop_mode_change(mode)
    
    def cycle_loop_mode(self):
        """Cycle through loop modes: OFF -> SINGLE_TRACK -> PLAYLIST -> OFF"""
        modes = [LoopMode.OFF, LoopMode.SINGLE_TRACK, LoopMode.PLAYLIST]
        current_idx = modes.index(self.loop_mode)
        next_mode = modes[(current_idx + 1) % len(modes)]
        self.set_loop_mode(next_mode)
        return next_mode
    
    def play_current(self):
        """Play the current track"""
        if not self.playlist or self.current_index >= len(self.playlist):
            print("❌ No track to play")
            return False
        
        track = self.playlist[self.current_index]
        track_path = track.get('path', '')
        
        if not os.path.exists(track_path):
            print(f"❌ Track file not found: {track_path}")
            return False
        
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(track_path)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play()
            
            self.is_playing = True
            self.is_paused = False
            
            print(f"▶️ Playing: {track.get('title', 'Unknown')} - {track.get('artist', 'Unknown')}")
            
            # Start loop monitoring thread
            self._start_loop_monitor()
            
            if self.on_track_change:
                self.on_track_change(track, self.current_index, len(self.playlist))
            
            return True
            
        except Exception as e:
            print(f"❌ Playback error: {e}")
            return False
    
    def _start_loop_monitor(self):
        """Start the loop monitoring thread"""
        # Stop existing thread
        self.stop_event.set()
        if self.loop_thread and self.loop_thread.is_alive():
            self.loop_thread.join(timeout=1.0)
        
        # Start new monitoring thread
        self.stop_event.clear()
        self.loop_thread = threading.Thread(target=self._loop_monitor, daemon=True)
        self.loop_thread.start()
    
    def _loop_monitor(self):
        """Monitor playback and handle looping"""
        while not self.stop_event.is_set() and self.is_playing:
            try:
                # Check if track finished
                if not pygame.mixer.music.get_busy() and not self.is_paused:
                    print(f"🎵 Track finished - Loop mode: {self.loop_mode.value}")
                    
                    if self.loop_mode == LoopMode.SINGLE_TRACK:
                        print("🔂 Looping current track")
                        self.play_current()
                        
                    elif self.loop_mode == LoopMode.PLAYLIST:
                        print("🔁 Playlist loop - moving to next track")
                        self._next_track_in_loop()
                        
                    else:  # LoopMode.OFF
                        if self.current_index < len(self.playlist) - 1:
                            print("▶️ Playing next track (no loop)")
                            self._next_track_in_loop()
                        else:
                            print("⏹️ Playlist finished - stopping")
                            self.stop()
                    
                    break  # Exit monitor, new one will start if needed
                    
            except Exception as e:
                print(f"❌ Loop monitor error: {e}")
                break
            
            time.sleep(0.5)
    
    def _next_track_in_loop(self):
        """Move to next track with proper looping logic"""
        if not self.playlist:
            return
        
        old_index = self.current_index
        
        if self.loop_mode == LoopMode.PLAYLIST:
            # Always loop in playlist mode
            self.current_index = (self.current_index + 1) % len(self.playlist)
            if old_index == len(self.playlist) - 1 and self.current_index == 0:
                print("🔄 Playlist looped back to first track!")
        else:
            # Only advance if not at end
            if self.current_index < len(self.playlist) - 1:
                self.current_index += 1
            else:
                self.stop()
                return
        
        self._save_settings()
        self.play_current()
    
    def next_track(self):
        """Manually skip to next track"""
        if not self.playlist:
            return
        
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self._save_settings()
        self.play_current()
    
    def previous_track(self):
        """Manually skip to previous track"""
        if not self.playlist:
            return
        
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self._save_settings()
        self.play_current()
    
    def pause(self):
        """Pause playback"""
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
            print("⏸️ Paused")
    
    def resume(self):
        """Resume playback"""
        if self.is_playing and self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            print("▶️ Resumed")
    
    def stop(self):
        """Stop playback"""
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.stop_event.set()
        print("⏹️ Stopped")
    
    def set_volume(self, volume: float):
        """Set volume (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)
        self._save_settings()
        print(f"🔊 Volume: {int(self.volume * 100)}%")
    
    def get_current_track(self) -> Optional[Dict]:
        """Get current track info"""
        if self.playlist and 0 <= self.current_index < len(self.playlist):
            return self.playlist[self.current_index]
        return None
    
    def get_status(self) -> Dict:
        """Get current status"""
        return {
            'is_playing': self.is_playing,
            'is_paused': self.is_paused,
            'loop_mode': self.loop_mode.value,
            'current_index': self.current_index,
            'playlist_size': len(self.playlist),
            'volume': self.volume
        }