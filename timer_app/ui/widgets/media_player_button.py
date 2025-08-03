import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import subprocess
import platform
import threading
import time
import json
from pathlib import Path
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

try:
    from mutagen import File as MutagenFile
    from mutagen.id3 import ID3NoHeaderError
    MUTAGEN_AVAILABLE = True
except ImportError:
    MUTAGEN_AVAILABLE = False

try:
    from PIL import Image, ImageTk
    import io
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

class SpotifyLikePlayer:
    """Spotify-like media player that runs in background"""
    def __init__(self):
        self.playlist = []
        self.current_track_index = 0
        self.is_playing = False
        self.is_paused = False
        self.volume = 0.7
        self.position = 0.0  # Current position in seconds
        self.duration = 0.0  # Total duration in seconds
        self.start_time = 0  # When playback started
        self.repeat_mode = "off"  # off, track, playlist
        self.shuffle = False
        self.current_track = None
        self.player_thread = None
        self.stop_event = threading.Event()
        self.sound_object = None  # For pygame.mixer.Sound (supports seeking better)
        self.sound_channel = None
        
        # Initialize pygame mixer if available
        if PYGAME_AVAILABLE:
            try:
                # Initialize pygame mixer with better settings for audio playback
                pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=1024)
                pygame.mixer.init()
                pygame.mixer.music.set_volume(self.volume)
                self.pygame_ready = True
                print("Pygame mixer initialized successfully")
            except Exception as e:
                print(f"Pygame mixer initialization failed: {e}")
                self.pygame_ready = False
        else:
            print("Pygame not available - please install pygame: pip install pygame")
            self.pygame_ready = False
        
        # Load saved playlist and settings
        self._load_settings()
    
    def _extract_metadata(self, file_path):
        """Extract metadata from audio file"""
        if not MUTAGEN_AVAILABLE:
            return {
                'title': os.path.splitext(os.path.basename(file_path))[0],
                'artist': 'Unknown Artist',
                'album': 'Unknown Album',
                'duration': '0:00',
                'genre': 'Unknown',
                'year': ''
            }
        
        try:
            audiofile = MutagenFile(file_path)
            if audiofile is None:
                raise Exception("Could not read file")
            
            # Get common metadata
            title = self._get_tag_value(audiofile, ['TIT2', 'TITLE', '\xa9nam']) or os.path.splitext(os.path.basename(file_path))[0]
            artist = self._get_tag_value(audiofile, ['TPE1', 'ARTIST', '\xa9ART']) or 'Unknown Artist'
            album = self._get_tag_value(audiofile, ['TALB', 'ALBUM', '\xa9alb']) or 'Unknown Album'
            genre = self._get_tag_value(audiofile, ['TCON', 'GENRE', '\xa9gen']) or 'Unknown'
            year = self._get_tag_value(audiofile, ['TDRC', 'DATE', '\xa9day']) or ''
            
            # Get duration
            duration = '0:00'
            if hasattr(audiofile, 'info') and audiofile.info is not None:
                length = audiofile.info.length
                minutes = int(length // 60)
                seconds = int(length % 60)
                duration = f"{minutes}:{seconds:02d}"
            
            # Extract album artwork
            artwork_data = self._extract_artwork(audiofile)
            
            return {
                'title': str(title).strip(),
                'artist': str(artist).strip(),
                'album': str(album).strip(),
                'duration': duration,
                'genre': str(genre).strip(),
                'year': str(year).strip()[:4],  # Just the year part
                'artwork': artwork_data
            }
        except Exception as e:
            print(f"Error reading metadata from {file_path}: {e}")
            return {
                'title': os.path.splitext(os.path.basename(file_path))[0],
                'artist': 'Unknown Artist',
                'album': 'Unknown Album',
                'duration': '0:00',
                'genre': 'Unknown',
                'year': '',
                'artwork': None
            }
    
    def _get_tag_value(self, audiofile, tag_keys):
        """Get tag value from multiple possible keys"""
        for key in tag_keys:
            if key in audiofile:
                value = audiofile[key]
                if isinstance(value, list) and len(value) > 0:
                    return str(value[0])
                elif value:
                    return str(value)
        return None
    
    def _extract_artwork(self, audiofile):
        """Extract album artwork from audio file"""
        if not MUTAGEN_AVAILABLE or not PIL_AVAILABLE:
            return None
            
        try:
            # Try different artwork tag formats
            artwork_data = None
            
            # ID3v2 (MP3)
            if hasattr(audiofile, 'tags') and audiofile.tags:
                # APIC frame for ID3v2
                if 'APIC:' in audiofile.tags:
                    artwork_data = audiofile.tags['APIC:'].data
                elif 'APIC' in audiofile.tags:
                    artwork_data = audiofile.tags['APIC'].data
                # Try to find any APIC frame
                else:
                    for key in audiofile.tags:
                        if key.startswith('APIC'):
                            artwork_data = audiofile.tags[key].data
                            break
            
            # MP4/M4A format
            elif hasattr(audiofile, 'get') and audiofile.get('covr'):
                artwork_data = bytes(audiofile['covr'][0])
            
            # FLAC format
            elif hasattr(audiofile, 'pictures') and audiofile.pictures:
                artwork_data = audiofile.pictures[0].data
            
            if artwork_data:
                # Convert to PIL Image
                image = Image.open(io.BytesIO(artwork_data))
                # Resize to fit in the UI (80x80 pixels)
                image = image.resize((80, 80), Image.Resampling.LANCZOS)
                # Convert to PhotoImage for tkinter
                return ImageTk.PhotoImage(image)
            
        except Exception as e:
            print(f"Error extracting artwork: {e}")
        
        return None
    
    def _extract_artwork_for_track(self, track):
        """Extract artwork for a specific track when UI is ready"""
        if not isinstance(track, dict) or not track.get('path'):
            return None
            
        if not os.path.exists(track['path']):
            return None
            
        try:
            if MUTAGEN_AVAILABLE and PIL_AVAILABLE:
                audiofile = MutagenFile(track['path'])
                if audiofile:
                    return self._extract_artwork(audiofile)
        except Exception as e:
            print(f"Error extracting artwork for {track.get('title', 'Unknown')}: {e}")
        
        return None
    
    def get_position(self):
        """Get current playback position in seconds"""
        if self.is_playing and not self.is_paused:
            elapsed = time.time() - self.start_time
            return min(self.position + elapsed, self.duration)
        return self.position
    
    def get_duration(self):
        """Get total track duration in seconds"""
        return self.duration
    
    def seek_to(self, position):
        """Seek to specific position in seconds"""
        if not self.pygame_ready:
            return False
        
        try:
            # Clamp position to valid range
            position = max(0, min(position, self.duration))
            
            # Stop current playback
            pygame.mixer.music.stop()
            
            # Restart the track
            if self.current_track:
                track_path = self.current_track['path'] if isinstance(self.current_track, dict) else self.current_track
                pygame.mixer.music.load(track_path)
                pygame.mixer.music.set_volume(self.volume)
                pygame.mixer.music.play(start=position)  # Try to start at position
                
                # Update position tracking
                self.position = position
                self.start_time = time.time()
                self.is_playing = True
                self.is_paused = False
                
                print(f"Seeking to {self._format_time(position)} / {self._format_time(self.duration)}")
                return True
        except Exception as e:
            print(f"Seek error: {e}")
            # Fallback: just update position tracking for visual feedback
            self.position = position
            self.start_time = time.time()
            return False
    
    def _parse_duration(self, duration_str):
        """Parse duration string (e.g., '3:45') to seconds"""
        try:
            if ':' in duration_str:
                parts = duration_str.split(':')
                if len(parts) == 2:
                    minutes, seconds = int(parts[0]), int(parts[1])
                    return minutes * 60 + seconds
                elif len(parts) == 3:
                    hours, minutes, seconds = int(parts[0]), int(parts[1]), int(parts[2])
                    return hours * 3600 + minutes * 60 + seconds
            return float(duration_str) if duration_str.replace('.', '').isdigit() else 0.0
        except:
            return 0.0
    
    def _format_time(self, seconds):
        """Format seconds to MM:SS format"""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes}:{seconds:02d}"
    
    def _load_settings(self):
        """Load saved settings and playlist"""
        try:
            settings_file = Path("media_player_settings.json")
            if settings_file.exists():
                with open(settings_file, 'r') as f:
                    data = json.load(f)
                    self.playlist = data.get('playlist', [])
                    self.volume = data.get('volume', 0.7)
                    self.repeat_mode = data.get('repeat_mode', 'off')
                    self.shuffle = data.get('shuffle', False)
                    
                    # Migrate old playlist format to new metadata format
                    self._migrate_playlist_format()
                    
                    # Re-extract artwork for existing tracks (since artwork isn't saved to JSON)
                    self._refresh_artwork()
        except Exception as e:
            print(f"Could not load media player settings: {e}")
    
    def _migrate_playlist_format(self):
        """Migrate old string-based playlist to new metadata format"""
        migrated = False
        new_playlist = []
        
        for track in self.playlist:
            if isinstance(track, str):
                # Old format - convert to new metadata format
                print(f"Migrating track: {os.path.basename(track)}")
                if os.path.exists(track):
                    metadata = self._extract_metadata(track)
                    track_info = {
                        'path': track,
                        'title': metadata['title'],
                        'artist': metadata['artist'],
                        'album': metadata['album'],
                        'duration': metadata['duration'],
                        'genre': metadata['genre'],
                        'year': metadata['year'],
                        'artwork': metadata.get('artwork')
                    }
                    new_playlist.append(track_info)
                    migrated = True
                    print(f"Migrated: {metadata['artist']} - {metadata['title']}")
                else:
                    print(f"Skipping missing file: {track}")
            else:
                # Already in new format
                new_playlist.append(track)
        
        if migrated:
            self.playlist = new_playlist
            self._save_settings()
            print(f"Playlist migration completed - {len(new_playlist)} tracks")
    
    def _refresh_artwork(self):
        """Re-extract artwork for all tracks in playlist (only when UI is ready)"""
        # Skip artwork extraction during initialization - will be done when UI is created
        pass
    
    def _save_settings(self):
        """Save current settings and playlist (excluding artwork)"""
        try:
            # Create a copy of playlist without artwork for JSON serialization
            playlist_for_save = []
            for track in self.playlist:
                if isinstance(track, dict):
                    track_copy = track.copy()
                    track_copy.pop('artwork', None)  # Remove artwork as it's not JSON serializable
                    playlist_for_save.append(track_copy)
                else:
                    playlist_for_save.append(track)
            
            settings_data = {
                'playlist': playlist_for_save,
                'volume': self.volume,
                'repeat_mode': self.repeat_mode,
                'shuffle': self.shuffle
            }
            with open("media_player_settings.json", 'w') as f:
                json.dump(settings_data, f, indent=2)
        except Exception as e:
            print(f"Could not save media player settings: {e}")
    
    def add_track(self, file_path):
        """Add track to playlist with metadata"""
        # Check if file exists and is a supported audio format
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return False
            
        # Check if it's a supported audio format
        supported_formats = ['.mp3', '.wav', '.ogg', '.m4a', '.flac', '.aac']
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext not in supported_formats:
            print(f"Unsupported audio format: {file_ext}")
            return False
        
        # Check if track already exists (by file path)
        existing_paths = [track['path'] if isinstance(track, dict) else track for track in self.playlist]
        if file_path in existing_paths:
            print(f"Track already in playlist: {os.path.basename(file_path)}")
            return False
        
        # Extract metadata
        metadata = self._extract_metadata(file_path)
        track_info = {
            'path': file_path,
            'title': metadata['title'],
            'artist': metadata['artist'],
            'album': metadata['album'],
            'duration': metadata['duration'],
            'genre': metadata['genre'],
            'year': metadata['year'],
            'artwork': metadata.get('artwork')
        }
        
        self.playlist.append(track_info)
        self._save_settings()
        print(f"Added to playlist: {metadata['artist']} - {metadata['title']}")
        return True
    
    def remove_track(self, index):
        """Remove track from playlist"""
        if 0 <= index < len(self.playlist):
            self.playlist.pop(index)
            if self.current_track_index >= len(self.playlist) and self.playlist:
                self.current_track_index = 0
            self._save_settings()
    
    def play(self, track_index=None):
        """Play track using pygame mixer"""
        if not self.playlist:
            print("No tracks in playlist")
            return False
        
        if track_index is not None:
            self.current_track_index = track_index
        
        # Ensure we have a valid track index
        if self.current_track_index >= len(self.playlist):
            self.current_track_index = 0
        
        if not self.pygame_ready:
            print("Pygame mixer not ready - cannot play audio internally")
            return False
        
        try:
            # Handle both old format (string) and new format (dict)
            track_item = self.playlist[self.current_track_index]
            if isinstance(track_item, dict):
                track_path = track_item['path']
                self.current_track = track_item
            else:
                track_path = track_item
                self.current_track = track_item
            
            # Stop any currently playing music
            pygame.mixer.music.stop()
            
            # Load and play the track
            print(f"Loading track: {os.path.basename(track_path)}")
            pygame.mixer.music.load(track_path)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play()
            
            self.is_playing = True
            self.is_paused = False
            self.position = 0.0
            self.start_time = time.time()
            
            # Get track duration from metadata
            if isinstance(self.current_track, dict):
                duration_str = self.current_track.get('duration', '0:00')
                self.duration = self._parse_duration(duration_str)
            else:
                self.duration = 0.0
            
            # Start background thread to track playback
            self.stop_event.clear()
            if self.player_thread and self.player_thread.is_alive():
                self.stop_event.set()
                # Don't join if we're in the same thread
                if self.player_thread != threading.current_thread():
                    self.player_thread.join(timeout=1.0)
            
            self.player_thread = threading.Thread(target=self._playback_monitor, daemon=True)
            self.player_thread.start()
            
            print(f"Now playing: {os.path.basename(track_path)}")
            return True
        except Exception as e:
            print(f"Playback error: {e}")
            # Don't fall back to system player - keep it internal
            return False
    
    def pause(self):
        """Pause playback"""
        if self.pygame_ready and self.is_playing:
            pygame.mixer.music.pause()
            self.is_paused = True
    
    def resume(self):
        """Resume playback"""
        if self.pygame_ready and self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
    
    def stop(self):
        """Stop playback"""
        if self.pygame_ready:
            pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.position = 0
        self.stop_event.set()
    
    def next_track(self):
        """Play next track"""
        if not self.playlist:
            return
        
        old_index = self.current_track_index
        
        if self.shuffle:
            import random
            self.current_track_index = random.randint(0, len(self.playlist) - 1)
            print(f"Shuffle: Moving from track {old_index} to {self.current_track_index}")
        else:
            self.current_track_index = (self.current_track_index + 1) % len(self.playlist)
            print(f"Next track: Moving from track {old_index} to {self.current_track_index} (total: {len(self.playlist)})")
            
            # If we looped back to 0, it means we reached the end
            if old_index == len(self.playlist) - 1 and self.current_track_index == 0:
                print("Playlist looped back to first track!")
        
        self.play()
    
    def previous_track(self):
        """Play previous track"""
        if not self.playlist:
            return
        
        self.current_track_index = (self.current_track_index - 1) % len(self.playlist)
        self.play()
    
    def set_volume(self, volume):
        """Set volume (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        if self.pygame_ready:
            try:
                pygame.mixer.music.set_volume(self.volume)
                print(f"Volume set to: {int(self.volume * 100)}%")
            except Exception as e:
                print(f"Error setting volume: {e}")
        self._save_settings()
    
    def _playback_monitor(self):
        """Monitor playback in background thread with better state management"""
        while not self.stop_event.is_set() and self.is_playing:
            if self.pygame_ready:
                try:
                    # Check if music is still playing
                    if not pygame.mixer.music.get_busy() and not self.is_paused:
                        print(f"Track finished - Current mode: {self.repeat_mode}, Track: {self.current_track_index}/{len(self.playlist)-1}")
                        self._handle_track_finished()
                        
                        # Continue monitoring if we're still playing
                        if not self.is_playing:
                            break
                except Exception as e:
                    print(f"Playback monitor error: {e}")
                    break
            time.sleep(0.5)
    
    def _handle_track_finished(self):
        """Handle what happens when a track finishes playing"""
        if self.repeat_mode == "track":
            print("🔂 Repeating current track")
            self.play(self.current_track_index)
        elif self.repeat_mode == "playlist":
            print("🔁 Playlist repeat mode")
            # Check if we're at the last track
            if self.current_track_index >= len(self.playlist) - 1:
                print("🔄 End of playlist - looping back to first track")
                self.current_track_index = 0
                self.play(0)
            else:
                print("▶️ Moving to next track in playlist")
                self.current_track_index += 1
                self.play(self.current_track_index)
        else:  # repeat_mode == "off"
            if self.current_track_index < len(self.playlist) - 1:
                print("▶️ Playing next track (repeat OFF)")
                self.current_track_index += 1
                self.play(self.current_track_index)
            else:
                print("⏹️ End of playlist - stopping (repeat OFF)")
                self.stop()
    
    def get_current_track_info(self):
        """Get current track information with metadata"""
        if self.playlist and self.current_track_index < len(self.playlist):
            track_item = self.playlist[self.current_track_index]
            
            # Handle both old format (string) and new format (dict)
            if isinstance(track_item, dict):
                return {
                    'title': track_item.get('title', 'Unknown Title'),
                    'artist': track_item.get('artist', 'Unknown Artist'),
                    'album': track_item.get('album', 'Unknown Album'),
                    'duration': track_item.get('duration', '0:00'),
                    'genre': track_item.get('genre', 'Unknown'),
                    'year': track_item.get('year', ''),
                    'artwork': track_item.get('artwork'),
                    'filename': os.path.basename(track_item['path']),
                    'path': track_item['path'],
                    'index': self.current_track_index,
                    'total_tracks': len(self.playlist)
                }
            else:
                # Old format - just file path
                return {
                    'title': os.path.splitext(os.path.basename(track_item))[0],
                    'artist': 'Unknown Artist',
                    'album': 'Unknown Album',
                    'duration': '0:00',
                    'genre': 'Unknown',
                    'year': '',
                    'artwork': None,
                    'filename': os.path.basename(track_item),
                    'path': track_item,
                    'index': self.current_track_index,
                    'total_tracks': len(self.playlist)
                }
        elif self.playlist:
            # If we have tracks but no current track, show first track
            track_item = self.playlist[0]
            if isinstance(track_item, dict):
                return {
                    'title': track_item.get('title', 'Unknown Title'),
                    'artist': track_item.get('artist', 'Unknown Artist'),
                    'album': track_item.get('album', 'Unknown Album'),
                    'duration': track_item.get('duration', '0:00'),
                    'genre': track_item.get('genre', 'Unknown'),
                    'year': track_item.get('year', ''),
                    'artwork': track_item.get('artwork'),
                    'filename': os.path.basename(track_item['path']),
                    'path': track_item['path'],
                    'index': 0,
                    'total_tracks': len(self.playlist)
                }
            else:
                return {
                    'title': os.path.splitext(os.path.basename(track_item))[0],
                    'artist': 'Unknown Artist',
                    'album': 'Unknown Album',
                    'duration': '0:00',
                    'genre': 'Unknown',
                    'year': '',
                    'artwork': None,
                    'filename': os.path.basename(track_item),
                    'path': track_item,
                    'index': 0,
                    'total_tracks': len(self.playlist)
                }
        return None


# Global player instance that persists across window closures
_global_player = SpotifyLikePlayer()


class MediaPlayerButton:
    """Handles media player button functionality as floating window - SRP"""
    def __init__(self, parent_root: tk.Tk, bg_color: str = "black"):
        self.parent_root = parent_root
        self.bg_color = bg_color
        self.player_window = None
        self.player = _global_player  # Use global player instance
        self.update_timer = None
        self._create_floating_button()

    def _create_floating_button(self):
        # Create a Toplevel window for the media player button
        self.media_win = tk.Toplevel(self.parent_root)
        self.media_win.overrideredirect(True)
        self.media_win.attributes("-topmost", True)
        self.media_win.config(bg=self.bg_color)
        self.media_win.geometry("30x30")
        
        # Create a canvas in the media button window
        self.media_canvas = tk.Canvas(
            self.media_win, width=30, height=30, 
            highlightthickness=0, bg=self.bg_color
        )
        self.media_canvas.pack()
        
        # Create circular button with media player icon
        self.media_canvas.create_oval(5, 5, 25, 25, fill='#FF6B35', outline='#FF6B35')
        # Add play icon (triangle)
        self.play_icon = self.media_canvas.create_polygon(12, 10, 12, 20, 20, 15, 
                                                         fill="white", outline="white")
        
        self.media_canvas.bind("<Button-1>", self._on_click)
        
        # Bind the main window's configure event to update the button's position
        self.parent_root.bind("<Configure>", lambda event: self._update_position())
        self._update_position()

    def _on_click(self, event):
        """Handle button click - show media player menu"""
        if self.player_window and self.player_window.winfo_exists():
            self.player_window.destroy()
            self.player_window = None
        else:
            self._show_media_player()

    def _update_position(self):
        """Position the media button on the right side of the octagon"""
        try:
            main_x = self.parent_root.winfo_x()
            main_y = self.parent_root.winfo_y()
            main_w = self.parent_root.winfo_width()
            main_h = self.parent_root.winfo_height()
            # Position on the right side of the octagon (middle-right)
            x = main_x + main_w + 5  # Right side of window
            y = main_y + main_h // 2 - 15  # Middle height
            self.media_win.geometry(f"+{x}+{y}")
        except tk.TclError:
            # Handle case where window is being destroyed
            pass

    def _show_media_player(self):
        """Show the Framer-style linear design media player"""
        self.player_window = tk.Toplevel(self.parent_root)
        self.player_window.title("🎵 Linear Music Player")
        self.player_window.geometry("420x700")  # Larger window
        self.player_window.configure(bg="#0A0A0B")  # Deep dark background
        self.player_window.resizable(True, True)  # Make resizable
        self.player_window.minsize(380, 600)  # Minimum size
        self.player_window.attributes('-topmost', True)
        
        # Keep window decorations for better UX (remove overrideredirect)
        # self.player_window.overrideredirect(True)
        
        # Position player window near the button
        try:
            button_x = self.media_win.winfo_x()
            button_y = self.media_win.winfo_y()
            player_x = button_x - 420 - 10  # Left of the button
            player_y = button_y - 150  # Slightly above
            self.player_window.geometry(f"420x700+{player_x}+{player_y}")
        except:
            pass
        
        # Linear gradient header effect (simulated with frames)
        gradient_frame = tk.Frame(self.player_window, bg="#0A0A0B", height=80)
        gradient_frame.pack(fill="x")
        gradient_frame.pack_propagate(False)
        
        # Create gradient effect with multiple frames
        gradient_colors = ["#1A1A1B", "#252527", "#2A2A2C", "#252527", "#1A1A1B"]
        for i, color in enumerate(gradient_colors):
            grad_strip = tk.Frame(gradient_frame, bg=color, height=16)
            grad_strip.pack(fill="x")
        
        # Modern title with subtle glow effect
        title_container = tk.Frame(gradient_frame, bg="#252527")
        title_container.place(relx=0.5, rely=0.5, anchor="center")
        
        title_label = tk.Label(title_container, text="Linear Music", 
                              font=("Inter", 18, "bold"), 
                              bg="#252527", fg="#FFFFFF")
        title_label.pack()
        
        subtitle_label = tk.Label(title_container, text="Focus Player", 
                                 font=("Inter", 10), 
                                 bg="#252527", fg="#888888")
        subtitle_label.pack()
        
        # Modern track info card with linear design
        track_card = tk.Frame(self.player_window, bg="#111113", height=120)
        track_card.pack(fill="x", padx=20, pady=20)
        track_card.pack_propagate(False)
        
        # Add subtle border effect
        border_frame = tk.Frame(track_card, bg="#222224", height=2)
        border_frame.pack(fill="x")
        
        # Track content container
        track_content = tk.Frame(track_card, bg="#111113")
        track_content.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Linear album art with gradient border
        art_container = tk.Frame(track_content, bg="#111113")
        art_container.pack(side="left")
        
        # Gradient border effect for album art
        art_border = tk.Frame(art_container, bg="#333335", width=84, height=84)
        art_border.pack()
        art_border.pack_propagate(False)
        
        art_frame = tk.Frame(art_border, bg="#1A1A1C", width=80, height=80)
        art_frame.place(relx=0.5, rely=0.5, anchor="center")
        art_frame.pack_propagate(False)
        
        # Album artwork display
        track_info = self.player.get_current_track_info()
        artwork = None
        
        # Extract artwork for current track if not already available
        if track_info and not track_info.get('artwork'):
            current_track = self.player.playlist[self.player.current_track_index] if self.player.playlist else None
            if current_track:
                artwork = self.player._extract_artwork_for_track(current_track)
                if artwork and isinstance(current_track, dict):
                    current_track['artwork'] = artwork
        elif track_info:
            artwork = track_info.get('artwork')
        
        if artwork:
            # Display actual album artwork
            self.art_label = tk.Label(art_frame, image=artwork, bg="#1A1A1C")
            self.art_label.image = artwork  # Keep a reference
        else:
            # Fallback to placeholder
            self.art_label = tk.Label(art_frame, text="🎵", font=("Segoe UI", 32), 
                                     bg="#1A1A1C", fg="#00FF88")
        self.art_label.pack(expand=True)
        
        # Track info with linear typography
        info_container = tk.Frame(track_content, bg="#111113")
        info_container.pack(side="left", fill="both", expand=True, padx=(20, 0))
        
        track_info = self.player.get_current_track_info()
        
        if track_info:
            # Display rich metadata like SpotiDownloader
            title = track_info['title'][:30] + "..." if len(track_info['title']) > 30 else track_info['title']
            artist = track_info['artist'][:25] + "..." if len(track_info['artist']) > 25 else track_info['artist']
            album = track_info['album'][:25] + "..." if len(track_info['album']) > 25 else track_info['album']
            duration = track_info['duration']
            track_position = f"{track_info['index'] + 1} of {track_info['total_tracks']}"
        else:
            title = "No track selected"
            artist = ""
            album = ""
            duration = "0:00"
            track_position = "0 of 0"
        
        # Track title with modern typography
        self.track_name_label = tk.Label(info_container, text=title, 
                                        font=("Inter", 14, "bold"), 
                                        bg="#111113", fg="#FFFFFF",
                                        anchor="w", justify="left")
        self.track_name_label.pack(anchor="w", pady=(2, 0))
        
        # Artist name with accent color
        self.artist_label = tk.Label(info_container, text=artist, 
                                    font=("Inter", 11), 
                                    bg="#111113", fg="#00FF88",
                                    anchor="w", justify="left")
        self.artist_label.pack(anchor="w", pady=(1, 0))
        
        # Album and duration info
        album_duration = f"{album} • {duration}" if album and album != "Unknown Album" else duration
        self.album_label = tk.Label(info_container, text=album_duration, 
                                   font=("Inter", 9), 
                                   bg="#111113", fg="#666668",
                                   anchor="w", justify="left")
        self.album_label.pack(anchor="w", pady=(1, 0))
        
        # Track position with subtle styling
        self.track_position_label = tk.Label(info_container, text=track_position, 
                                            font=("Inter", 9), 
                                            bg="#111113", fg="#666668")
        self.track_position_label.pack(anchor="w", pady=(3, 0))
        
        # Status indicator
        status_text = "Playing" if self.player.is_playing and not self.player.is_paused else "Paused" if self.player.is_paused else "Stopped"
        status_color = "#00FF88" if self.player.is_playing and not self.player.is_paused else "#FFB800" if self.player.is_paused else "#666668"
        
        self.status_label = tk.Label(info_container, text=f"● {status_text}", 
                                    font=("Inter", 9), 
                                    bg="#111113", fg=status_color)
        self.status_label.pack(anchor="w", pady=(8, 0))
        
        # Audio progress bar section
        progress_card = tk.Frame(self.player_window, bg="#0E0E10", height=70)
        progress_card.pack(fill="x", padx=20, pady=10)
        progress_card.pack_propagate(False)
        
        # Progress border
        progress_border = tk.Frame(progress_card, bg="#222224", height=1)
        progress_border.pack(fill="x")
        
        progress_content = tk.Frame(progress_card, bg="#0E0E10")
        progress_content.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Time labels and progress bar
        time_container = tk.Frame(progress_content, bg="#0E0E10")
        time_container.pack(fill="x")
        
        # Current time label
        self.current_time_label = tk.Label(time_container, text="0:00", 
                                          font=("Inter", 9), 
                                          bg="#0E0E10", fg="#FFFFFF")
        self.current_time_label.pack(side="left")
        
        # Total time label
        track_info = self.player.get_current_track_info()
        total_duration = track_info.get('duration', '0:00') if track_info else '0:00'
        self.total_time_label = tk.Label(time_container, text=total_duration, 
                                        font=("Inter", 9), 
                                        bg="#0E0E10", fg="#666668")
        self.total_time_label.pack(side="right")
        
        # Progress bar container
        progress_bar_container = tk.Frame(progress_content, bg="#0E0E10")
        progress_bar_container.pack(fill="x", pady=(8, 0))
        
        # Custom progress bar
        self.progress_canvas = tk.Canvas(progress_bar_container, height=6, bg="#1A1A1C", 
                                        highlightthickness=0, relief="flat")
        self.progress_canvas.pack(fill="x")
        
        # Bind click events for seeking
        self.progress_canvas.bind("<Button-1>", self._on_progress_click)
        self.progress_canvas.bind("<B1-Motion>", self._on_progress_drag)
        
        # Linear control panel with modern design
        controls_card = tk.Frame(self.player_window, bg="#0F0F11", height=80)
        controls_card.pack(fill="x", padx=20, pady=10)
        controls_card.pack_propagate(False)
        
        # Top border for controls card
        controls_border = tk.Frame(controls_card, bg="#222224", height=1)
        controls_border.pack(fill="x")
        
        # Control buttons container
        control_buttons = tk.Frame(controls_card, bg="#0F0F11")
        control_buttons.pack(expand=True)
        
        # Create modern linear buttons
        def create_linear_button(parent, text, command, is_primary=False, is_active=False):
            if is_primary:
                bg_color = "#00FF88" if not is_active else "#00DD77"
                fg_color = "#000000"
                active_bg = "#00DD77"
            elif is_active:
                bg_color = "#333335"
                fg_color = "#00FF88"
                active_bg = "#444446"
            else:
                bg_color = "#1A1A1C"
                fg_color = "#FFFFFF"
                active_bg = "#222224"
            
            btn = tk.Button(parent, text=text, command=command,
                           font=("Inter", 12, "bold"), 
                           bg=bg_color, fg=fg_color,
                           activebackground=active_bg, activeforeground=fg_color,
                           relief="flat", bd=0, highlightthickness=0,
                           width=4, height=2)
            return btn
        
        # Shuffle button with linear design
        shuffle_text = "S" if self.player.shuffle else "S"
        self.shuffle_btn = create_linear_button(control_buttons, shuffle_text, 
                                               self._toggle_shuffle, is_active=self.player.shuffle)
        self.shuffle_btn.pack(side="left", padx=8, pady=15)
        
        # Previous button
        prev_btn = create_linear_button(control_buttons, "<<", self._previous_track)
        prev_btn.pack(side="left", padx=8, pady=15)
        
        # Play/Pause button (primary button)
        play_text = "||" if self.player.is_playing and not self.player.is_paused else ">"
        self.main_play_btn = create_linear_button(control_buttons, play_text, 
                                                 self._toggle_playback, is_primary=True)
        self.main_play_btn.pack(side="left", padx=12, pady=15)
        
        # Next button
        next_btn = create_linear_button(control_buttons, ">>", self._next_track)
        next_btn.pack(side="left", padx=8, pady=15)
        
        # Repeat button
        repeat_icons = {"off": "R", "playlist": "RP", "track": "R1"}
        self.repeat_btn = create_linear_button(control_buttons, repeat_icons[self.player.repeat_mode], 
                                              self._toggle_repeat, is_active=(self.player.repeat_mode != "off"))
        self.repeat_btn.pack(side="left", padx=8, pady=15)
        
        # Linear volume control
        volume_card = tk.Frame(self.player_window, bg="#0D0D0F", height=60)
        volume_card.pack(fill="x", padx=20, pady=10)
        volume_card.pack_propagate(False)
        
        # Volume border
        volume_border = tk.Frame(volume_card, bg="#222224", height=1)
        volume_border.pack(fill="x")
        
        volume_content = tk.Frame(volume_card, bg="#0D0D0F")
        volume_content.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Modern volume icon
        volume_icon = tk.Label(volume_content, text="Vol", font=("Inter", 12), 
                              bg="#0D0D0F", fg="#666668")
        volume_icon.pack(side="left", padx=(0, 15))
        
        # Custom volume slider with linear design
        volume_container = tk.Frame(volume_content, bg="#0D0D0F")
        volume_container.pack(side="left", fill="x", expand=True)
        
        # Volume percentage label
        self.volume_label = tk.Label(volume_container, text=f"{int(self.player.volume * 100)}%", 
                                    font=("Inter", 10, "bold"), 
                                    bg="#0D0D0F", fg="#00FF88")
        self.volume_label.pack(side="right", padx=(10, 0))
        
        # Linear volume slider
        self.volume_scale = tk.Scale(volume_container, from_=0, to=100, orient="horizontal",
                                    command=self._on_volume_change, 
                                    bg="#0D0D0F", fg="#FFFFFF",
                                    highlightthickness=0, troughcolor="#1A1A1C",
                                    activebackground="#00FF88", 
                                    sliderrelief="flat", sliderlength=20)
        self.volume_scale.set(self.player.volume * 100)
        self.volume_scale.pack(side="left", fill="x", expand=True)
        
        # Modern playlist section (expandable)
        playlist_card = tk.Frame(self.player_window, bg="#0B0B0D")
        playlist_card.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Playlist header with linear design
        playlist_header = tk.Frame(playlist_card, bg="#0B0B0D", height=50)
        playlist_header.pack(fill="x")
        playlist_header.pack_propagate(False)
        
        # Header border
        header_border = tk.Frame(playlist_header, bg="#222224", height=1)
        header_border.pack(fill="x")
        
        header_content = tk.Frame(playlist_header, bg="#0B0B0D")
        header_content.pack(fill="both", expand=True, padx=20, pady=12)
        
        playlist_label = tk.Label(header_content, text="Queue", 
                                 font=("Inter", 14, "bold"), 
                                 bg="#0B0B0D", fg="#FFFFFF")
        playlist_label.pack(side="left")
        
        # Modern add button
        add_btn = tk.Button(header_content, text="+ Add", command=self._add_track,
                           font=("Inter", 10, "bold"), 
                           bg="#00FF88", fg="#000000",
                           activebackground="#00DD77", activeforeground="#000000",
                           relief="flat", bd=0, highlightthickness=0, 
                           padx=15, pady=6)
        add_btn.pack(side="right")
        
        # Linear playlist container
        playlist_container = tk.Frame(playlist_card, bg="#0B0B0D")
        playlist_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Custom scrollbar with linear design
        scrollbar_frame = tk.Frame(playlist_container, bg="#0B0B0D", width=8)
        scrollbar_frame.pack(side="right", fill="y", padx=(5, 0))
        
        scrollbar = tk.Scrollbar(scrollbar_frame, bg="#1A1A1C", troughcolor="#0B0B0D",
                                activebackground="#333335", width=6, relief="flat", bd=0)
        scrollbar.pack(fill="y")
        
        # Modern listbox design
        self.playlist_listbox = tk.Listbox(playlist_container, yscrollcommand=scrollbar.set,
                                          bg="#0B0B0D", fg="#FFFFFF", 
                                          selectbackground="#333335", selectforeground="#00FF88",
                                          font=("Inter", 10), bd=0, highlightthickness=0,
                                          activestyle="none")
        self.playlist_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.playlist_listbox.yview)
        
        # Populate playlist
        self._update_playlist_display()
        
        # Bind double-click to play track
        self.playlist_listbox.bind("<Double-Button-1>", self._on_track_double_click)
        self.playlist_listbox.bind("<Button-3>", self._on_track_right_click)  # Right-click menu
        
        # Start UI update timer
        self._start_ui_updates()
        
        # Close button (at bottom for better UX)
        close_frame = tk.Frame(self.player_window, bg="#0A0A0B")
        close_frame.pack(side="bottom", fill="x", padx=20, pady=(5, 20))
        
        close_btn = tk.Button(close_frame, text="🎵 Close (Music Continues)", 
                             command=self._close_player,
                             font=("Inter", 10, "bold"), bg="#333335", fg="#FFFFFF",
                             activebackground="#444446", activeforeground="#FFFFFF",
                             relief="flat", bd=0, highlightthickness=0,
                             padx=15, pady=12)
        close_btn.pack(fill="x")
        
        # Don't auto-close on focus out for Spotify-like experience
        self.player_window.focus_set()

    def _on_progress_click(self, event):
        """Handle click on progress bar for seeking"""
        if not self.player.playlist or self.player.duration <= 0:
            return
        
        # Calculate position based on click
        canvas_width = self.progress_canvas.winfo_width()
        if canvas_width > 0:
            # Ensure click is within bounds
            click_x = max(0, min(event.x, canvas_width))
            click_ratio = click_x / canvas_width
            seek_position = click_ratio * self.player.duration
            
            # Only seek if it's a reasonable position
            if 0 <= seek_position <= self.player.duration:
                success = self.player.seek_to(seek_position)
                if success:
                    self._update_progress_bar()
                    # Update time display immediately
                    if hasattr(self, 'current_time_label'):
                        self.current_time_label.config(text=self.player._format_time(seek_position))
    
    def _on_progress_drag(self, event):
        """Handle dragging on progress bar for seeking"""
        self._on_progress_click(event)  # Same logic as click
    
    def _update_progress_bar(self):
        """Update the visual progress bar"""
        if not hasattr(self, 'progress_canvas'):
            return
        
        try:
            canvas_width = self.progress_canvas.winfo_width()
            canvas_height = self.progress_canvas.winfo_height()
            
            if canvas_width <= 0 or canvas_height <= 0:
                return
            
            # Clear canvas
            self.progress_canvas.delete("all")
            
            # Draw background
            self.progress_canvas.create_rectangle(0, 0, canvas_width, canvas_height, 
                                                 fill="#1A1A1C", outline="")
            
            # Draw progress if playing
            if self.player.duration > 0:
                current_pos = self.player.get_position()
                progress_ratio = min(current_pos / self.player.duration, 1.0)
                progress_width = int(canvas_width * progress_ratio)
                
                if progress_width > 0:
                    # Draw progress bar
                    self.progress_canvas.create_rectangle(0, 0, progress_width, canvas_height, 
                                                         fill="#00FF88", outline="")
                    
                    # Draw progress handle
                    if progress_width > 2:
                        handle_x = progress_width
                        self.progress_canvas.create_oval(handle_x-4, canvas_height//2-4, 
                                                        handle_x+4, canvas_height//2+4, 
                                                        fill="#FFFFFF", outline="#00FF88", width=2)
        except Exception as e:
            print(f"Error updating progress bar: {e}")

    def _add_track(self):
        """Add track to playlist"""
        file_types = [
            ("Audio Files", "*.mp3 *.wav *.ogg *.m4a *.flac *.aac"),
            ("All Files", "*.*")
        ]
        
        filenames = filedialog.askopenfilenames(
            title="Select Audio Files",
            filetypes=file_types
        )
        
        for filename in filenames:
            self.player.add_track(filename)
        
        self._update_playlist_display()

    def _update_playlist_display(self):
        """Update the playlist display with rich metadata"""
        if hasattr(self, 'playlist_listbox'):
            self.playlist_listbox.delete(0, tk.END)
            for i, track in enumerate(self.player.playlist):
                # Handle both old format (string) and new format (dict)
                if isinstance(track, dict):
                    artist = track.get('artist', 'Unknown Artist')
                    title = track.get('title', 'Unknown Title')
                    duration = track.get('duration', '0:00')
                    # Format like SpotiDownloader: "Artist - Title [Duration]"
                    display_text = f"{artist} - {title} [{duration}]"
                else:
                    # Old format - just filename
                    display_text = os.path.basename(track)
                
                # Add playing indicator
                prefix = "♪ " if i == self.player.current_track_index and self.player.is_playing else "  "
                self.playlist_listbox.insert(tk.END, f"{prefix}{display_text}")
            
            # Highlight current track
            if self.player.playlist and self.player.current_track_index < len(self.player.playlist):
                self.playlist_listbox.selection_set(self.player.current_track_index)

    def _on_track_double_click(self, event):
        """Handle double-click on playlist track"""
        selection = self.playlist_listbox.curselection()
        if selection:
            track_index = selection[0]
            self.player.play(track_index)
            self._update_ui_elements()

    def _on_track_right_click(self, event):
        """Handle right-click on playlist track"""
        selection = self.playlist_listbox.curselection()
        if selection:
            track_index = selection[0]
            
            # Create context menu
            context_menu = tk.Menu(self.player_window, tearoff=0, bg="#333333", fg="white")
            context_menu.add_command(label="Play", command=lambda: self._play_track(track_index))
            context_menu.add_separator()
            context_menu.add_command(label="Remove from Playlist", 
                                   command=lambda: self._remove_track(track_index))
            
            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()

    def _play_track(self, index):
        """Play specific track"""
        self.player.play(index)
        self._update_ui_elements()

    def _remove_track(self, index):
        """Remove track from playlist"""
        self.player.remove_track(index)
        self._update_playlist_display()

    def _toggle_playback(self):
        """Toggle play/pause"""
        if not self.player.playlist:
            messagebox.showwarning("Empty Playlist", "Please add some tracks to the playlist first.")
            return
        
        if self.player.is_playing and not self.player.is_paused:
            self.player.pause()
        elif self.player.is_paused:
            self.player.resume()
        else:
            self.player.play()
        
        self._update_ui_elements()

    def _next_track(self):
        """Play next track"""
        self.player.next_track()
        self._update_ui_elements()

    def _previous_track(self):
        """Play previous track"""
        self.player.previous_track()
        self._update_ui_elements()

    def _toggle_shuffle(self):
        """Toggle shuffle mode"""
        self.player.shuffle = not self.player.shuffle
        self.player._save_settings()
        
        # Update button appearance with linear design
        if hasattr(self, 'shuffle_btn'):
            if self.player.shuffle:
                self.shuffle_btn.config(bg="#333335", fg="#00FF88")
            else:
                self.shuffle_btn.config(bg="#1A1A1C", fg="#FFFFFF")
        
        print(f"Shuffle mode: {'ON' if self.player.shuffle else 'OFF'}")

    def _toggle_repeat(self):
        """Toggle repeat mode"""
        modes = ["off", "playlist", "track"]
        current_index = modes.index(self.player.repeat_mode)
        self.player.repeat_mode = modes[(current_index + 1) % len(modes)]
        self.player._save_settings()
        
        # Update button appearance with linear design
        if hasattr(self, 'repeat_btn'):
            repeat_icons = {"off": "⟲", "playlist": "⟲", "track": "⟳"}
            if self.player.repeat_mode != "off":
                self.repeat_btn.config(
                    text=repeat_icons[self.player.repeat_mode],
                    bg="#333335", fg="#00FF88"
                )
            else:
                self.repeat_btn.config(
                    text=repeat_icons[self.player.repeat_mode],
                    bg="#1A1A1C", fg="#FFFFFF"
                )
        
        mode_descriptions = {
            "off": "🔇 Repeat OFF - Play through once",
            "playlist": "🔁 Repeat PLAYLIST - Loop entire playlist",
            "track": "🔂 Repeat TRACK - Loop current song"
        }
        print(mode_descriptions[self.player.repeat_mode])

    def _on_volume_change(self, value):
        """Handle volume slider change"""
        volume = float(value) / 100
        self.player.set_volume(volume)
        # Update volume percentage label
        if hasattr(self, 'volume_label'):
            self.volume_label.config(text=f"{int(float(value))}%")

    def _start_ui_updates(self):
        """Start periodic UI updates"""
        if self.player_window:
            self._update_ui_elements()
            self.update_timer = self.player_window.after(1000, self._start_ui_updates)

    def _update_ui_elements(self):
        """Update all UI elements with linear design"""
        if not self.player_window:
            return
        
        # Update main button icon
        self._update_main_button_icon()
        
        # Update track info with rich metadata
        track_info = self.player.get_current_track_info()
        if hasattr(self, 'track_name_label') and track_info:
            # Update title
            title = track_info['title'][:30] + "..." if len(track_info['title']) > 30 else track_info['title']
            self.track_name_label.config(text=title)
            
            # Update artist
            if hasattr(self, 'artist_label'):
                artist = track_info['artist'][:25] + "..." if len(track_info['artist']) > 25 else track_info['artist']
                self.artist_label.config(text=artist)
            
            # Update album and duration
            if hasattr(self, 'album_label'):
                album = track_info['album'][:25] + "..." if len(track_info['album']) > 25 else track_info['album']
                duration = track_info['duration']
                album_duration = f"{album} • {duration}" if album and album != "Unknown Album" else duration
                self.album_label.config(text=album_duration)
            
            # Update position
            self.track_position_label.config(text=f"{track_info['index'] + 1} of {track_info['total_tracks']}")
            
            # Update album artwork
            if hasattr(self, 'art_label'):
                artwork = track_info.get('artwork')
                
                # Extract artwork if not available
                if not artwork and self.player.playlist:
                    current_track = self.player.playlist[self.player.current_track_index]
                    if isinstance(current_track, dict):
                        artwork = self.player._extract_artwork_for_track(current_track)
                        if artwork:
                            current_track['artwork'] = artwork
                
                if artwork:
                    self.art_label.config(image=artwork, text="")
                    self.art_label.image = artwork  # Keep reference
                else:
                    self.art_label.config(image="", text="🎵", font=("Segoe UI", 32), fg="#00FF88")
                    self.art_label.image = None
        elif hasattr(self, 'track_name_label'):
            self.track_name_label.config(text="No track selected")
            if hasattr(self, 'artist_label'):
                self.artist_label.config(text="")
            if hasattr(self, 'album_label'):
                self.album_label.config(text="")
            self.track_position_label.config(text="0 of 0")
            # Reset artwork to placeholder
            if hasattr(self, 'art_label'):
                self.art_label.config(image="", text="🎵", font=("Segoe UI", 32), fg="#00FF88")
                self.art_label.image = None
        
        # Update status indicator with modern colors
        if hasattr(self, 'status_label'):
            status_text = "Playing" if self.player.is_playing and not self.player.is_paused else "Paused" if self.player.is_paused else "Stopped"
            status_color = "#00FF88" if self.player.is_playing and not self.player.is_paused else "#FFB800" if self.player.is_paused else "#666668"
            self.status_label.config(text=f"● {status_text}", fg=status_color)
        
        # Update play button with linear icons
        if hasattr(self, 'main_play_btn'):
            play_text = "⏸" if self.player.is_playing and not self.player.is_paused else "⏵"
            # Update button color based on state
            if self.player.is_playing and not self.player.is_paused:
                self.main_play_btn.config(text=play_text, bg="#00FF88", fg="#000000")
            else:
                self.main_play_btn.config(text=play_text, bg="#00FF88", fg="#000000")
        
        # Update shuffle button state
        if hasattr(self, 'shuffle_btn'):
            if self.player.shuffle:
                self.shuffle_btn.config(bg="#333335", fg="#00FF88")
            else:
                self.shuffle_btn.config(bg="#1A1A1C", fg="#FFFFFF")
        
        # Update repeat button state  
        if hasattr(self, 'repeat_btn'):
            repeat_icons = {"off": "⟲", "playlist": "⟲", "track": "⟳"}
            if self.player.repeat_mode != "off":
                self.repeat_btn.config(text=repeat_icons[self.player.repeat_mode], 
                                      bg="#333335", fg="#00FF88")
            else:
                self.repeat_btn.config(text=repeat_icons[self.player.repeat_mode], 
                                      bg="#1A1A1C", fg="#FFFFFF")
        
        # Update progress bar and time display
        self._update_progress_bar()
        if hasattr(self, 'current_time_label'):
            current_time = self.player._format_time(self.player.get_position())
            self.current_time_label.config(text=current_time)
        
        if hasattr(self, 'total_time_label') and track_info:
            self.total_time_label.config(text=track_info.get('duration', '0:00'))
        
        # Update playlist display
        self._update_playlist_display()

    def _update_main_button_icon(self):
        """Update main button icon based on playback state"""
        try:
            if self.player.is_playing and not self.player.is_paused:
                # Change to pause icon (two vertical bars)
                self.media_canvas.delete(self.play_icon)
                self.play_icon = [
                    self.media_canvas.create_rectangle(11, 10, 13, 20, fill="white", outline="white"),
                    self.media_canvas.create_rectangle(17, 10, 19, 20, fill="white", outline="white")
                ]
            else:
                # Change to play icon (triangle)
                self.media_canvas.delete("all")
                self.media_canvas.create_oval(5, 5, 25, 25, fill='#FF6B35', outline='#FF6B35')
                self.play_icon = self.media_canvas.create_polygon(12, 10, 12, 20, 20, 15, 
                                                                 fill="white", outline="white")
        except:
            pass

    def _close_player(self):
        """Close the media player window (music continues in background)"""
        if self.update_timer:
            self.player_window.after_cancel(self.update_timer)
            self.update_timer = None
        
        if self.player_window:
            self.player_window.destroy()
            self.player_window = None