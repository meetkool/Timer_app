"""
Loop Control Buttons - UI for audio looping functionality
Provides buttons for different loop modes and integrates with AudioLoopManager
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from timer_app.audio import AudioSystemFactory, TrackInfo, RepeatMode
from timer_app.audio.interfaces import AudioSystemInterface
import os

class LoopControlPanel:
    """UI panel for loop controls"""
    
    def __init__(self, parent, audio_system: AudioSystemInterface):
        self.parent = parent
        self.audio_system = audio_system
        self.control_window = None
        
        # UI elements
        self.track_info_label = None
        self.loop_mode_button = None
        self.single_loop_button = None
        self.playlist_loop_button = None
        self.status_label = None
    
    def create_loop_button(self):
        """Create a floating loop button"""
        loop_btn = tk.Button(
            self.parent,
            text="Loop",
            font=("Arial", 10, "bold"),
            bg="#2A2A2C",
            fg="#FFFFFF",
            activebackground="#3A3A3C",
            activeforeground="#00FF88",
            relief="flat",
            bd=0,
            width=3,
            height=1,
            command=self._show_loop_controls
        )
        return loop_btn
    
    def _show_loop_controls(self):
        """Show the loop control panel"""
        if self.control_window and self.control_window.winfo_exists():
            self.control_window.lift()
            return
        
        self._create_control_window()
    
    def _create_control_window(self):
        """Create the loop control window"""
        self.control_window = tk.Toplevel(self.parent)
        self.control_window.title("🔄 Audio Loop Controls")
        self.control_window.geometry("400x600")
        self.control_window.configure(bg="#1A1A1C")
        self.control_window.resizable(True, True)
        self.control_window.minsize(350, 500)
        
        # Header
        header_frame = tk.Frame(self.control_window, bg="#2A2A2C", height=60)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🔄 Loop Controls",
            font=("Arial", 16, "bold"),
            bg="#2A2A2C",
            fg="#FFFFFF"
        )
        title_label.pack(expand=True)
        
        # Current track info
        self._create_track_info_section()
        
        # Loop mode buttons
        self._create_loop_mode_section()
        
        # Playback controls
        self._create_playback_controls()
        
        # Playlist section
        self._create_playlist_section()
        
        # Status section
        self._create_status_section()
        
        # Update initial state
        self._update_ui()
    
    def _create_track_info_section(self):
        """Create track information display"""
        info_frame = tk.Frame(self.control_window, bg="#2A2A2C")
        info_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(
            info_frame,
            text="🎵 Current Track",
            font=("Arial", 12, "bold"),
            bg="#2A2A2C",
            fg="#00FF88"
        ).pack(anchor="w")
        
        self.track_info_label = tk.Label(
            info_frame,
            text="No track loaded",
            font=("Arial", 10),
            bg="#2A2A2C",
            fg="#FFFFFF",
            wraplength=350,
            justify="left"
        )
        self.track_info_label.pack(anchor="w", pady=(5, 0))
    
    def _create_loop_mode_section(self):
        """Create loop mode control buttons"""
        loop_frame = tk.Frame(self.control_window, bg="#1A1A1C")
        loop_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(
            loop_frame,
            text="🔄 Loop Modes",
            font=("Arial", 12, "bold"),
            bg="#1A1A1C",
            fg="#00FF88"
        ).pack(anchor="w")
        
        buttons_frame = tk.Frame(loop_frame, bg="#1A1A1C")
        buttons_frame.pack(fill="x", pady=(10, 0))
        
        # Loop Off Button
        self.loop_off_button = self._create_loop_button(
            buttons_frame, "■ No Loop", RepeatMode.OFF, 0
        )
        
        # Single Track Loop Button
        self.single_loop_button = self._create_loop_button(
            buttons_frame, "1 Loop Song", RepeatMode.SINGLE, 1
        )
        
        # Playlist Loop Button
        self.playlist_loop_button = self._create_loop_button(
            buttons_frame, "∞ Loop Playlist", RepeatMode.PLAYLIST, 2
        )
    
    def _create_loop_button(self, parent, text, mode, row):
        """Create a styled loop mode button"""
        button = tk.Button(
            parent,
            text=text,
            font=("Arial", 11, "bold"),
            bg="#333335",
            fg="#FFFFFF",
            activebackground="#00FF88",
            activeforeground="#000000",
            relief="flat",
            bd=0,
            height=2,
            command=lambda: self._set_loop_mode(mode)
        )
        button.pack(fill="x", pady=2)
        return button
    
    def _create_playback_controls(self):
        """Create playback control buttons"""
        control_frame = tk.Frame(self.control_window, bg="#1A1A1C")
        control_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(
            control_frame,
            text="🎮 Playback Controls",
            font=("Arial", 12, "bold"),
            bg="#1A1A1C",
            fg="#00FF88"
        ).pack(anchor="w")
        
        buttons_frame = tk.Frame(control_frame, bg="#1A1A1C")
        buttons_frame.pack(fill="x", pady=(10, 0))
        
        # Control buttons
        controls = [
            ("<<", self.audio_system.previous_track),
            ("||", self._toggle_pause),
            (">", self._play_current),
            ("Stop", self.audio_system.stop_playback),
            (">>", self.audio_system.next_track),
        ]
        
        for i, (symbol, command) in enumerate(controls):
            btn = tk.Button(
                buttons_frame,
                text=symbol,
                font=("Arial", 14, "bold"),
                bg="#333335",
                fg="#FFFFFF",
                activebackground="#00FF88",
                activeforeground="#000000",
                relief="flat",
                bd=0,
                width=4,
                height=2,
                command=command
            )
            btn.grid(row=0, column=i, padx=2, sticky="ew")
        
        # Configure grid weights
        for i in range(5):
            buttons_frame.columnconfigure(i, weight=1)
    
    def _create_playlist_section(self):
        """Create playlist management section"""
        playlist_frame = tk.Frame(self.control_window, bg="#1A1A1C")
        playlist_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(
            playlist_frame,
            text="📝 Playlist",
            font=("Arial", 12, "bold"),
            bg="#1A1A1C",
            fg="#00FF88"
        ).pack(anchor="w")
        
        # Add track button
        add_btn = tk.Button(
            playlist_frame,
            text="➕ Add Track",
            font=("Arial", 10, "bold"),
            bg="#333335",
            fg="#FFFFFF",
            activebackground="#00FF88",
            activeforeground="#000000",
            relief="flat",
            bd=0,
            command=self._add_track
        )
        add_btn.pack(fill="x", pady=(5, 10))
        
        # Playlist display
        list_frame = tk.Frame(playlist_frame, bg="#2A2A2C")
        list_frame.pack(fill="both", expand=True)
        
        self.playlist_listbox = tk.Listbox(
            list_frame,
            bg="#2A2A2C",
            fg="#FFFFFF",
            selectbackground="#00FF88",
            selectforeground="#000000",
            font=("Arial", 9),
            bd=0,
            highlightthickness=0
        )
        
        scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        self.playlist_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.playlist_listbox.yview)
        
        self.playlist_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind double-click to play track
        self.playlist_listbox.bind("<Double-Button-1>", self._play_selected_track)
    
    def _create_status_section(self):
        """Create status display"""
        status_frame = tk.Frame(self.control_window, bg="#2A2A2C")
        status_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.status_label = tk.Label(
            status_frame,
            text="Status: Ready",
            font=("Arial", 9),
            bg="#2A2A2C",
            fg="#CCCCCC",
            anchor="w"
        )
        self.status_label.pack(fill="x", padx=5, pady=5)
    
    def _set_loop_mode(self, mode: RepeatMode):
        """Set the loop mode"""
        # Update the audio system's repeat mode
        current_mode = self.audio_system.get_status()['repeat_mode']
        if current_mode != mode.value:
            self.audio_system.cycle_repeat_mode()  # For now, cycle until we get the right mode
            # Better approach would be to have a direct setter
        self._update_loop_buttons()
    
    def _toggle_pause(self):
        """Toggle pause/resume"""
        status = self.audio_system.get_status()
        if status['playback_state'] == 'paused':
            self.audio_system.resume_playback()
        elif status['playback_state'] == 'playing':
            self.audio_system.pause_playback()
        self._update_ui()
    
    def _add_track(self):
        """Add a track to the playlist"""
        file_path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[
                ("Audio Files", "*.mp3 *.wav *.ogg *.m4a *.flac"),
                ("MP3 Files", "*.mp3"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            # Extract basic info from filename
            filename = os.path.basename(file_path)
            name_without_ext = os.path.splitext(filename)[0]
            
            # Create TrackInfo object for the new system
            track_info = TrackInfo(
                path=file_path,
                title=name_without_ext,
                artist='Unknown'
            )
            
            self.audio_system.add_track(track_info)
            self._update_playlist_display()
    
    def _play_selected_track(self, event):
        """Play the selected track from the playlist"""
        selection = self.playlist_listbox.curselection()
        if selection:
            index = selection[0]
            self.audio_system.load_and_play_track(index)
            self._update_ui()
    
    def _play_current(self):
        """Play current track"""
        status = self.audio_system.get_status()
        current_index = status['current_index']
        self.audio_system.load_and_play_track(current_index)
    
    def _update_ui(self):
        """Update all UI elements"""
        self._update_track_info()
        self._update_loop_buttons()
        self._update_playlist_display()
        self._update_status()
    
    def _update_track_info(self):
        """Update current track information"""
        if self.track_info_label:
            track = self.audio_system.get_current_track()
            if track:
                info = f"🎵 {track.title}\n👤 {track.artist}"
            else:
                info = "No track loaded"
            self.track_info_label.config(text=info)
    
    def _update_loop_buttons(self):
        """Update loop button appearances"""
        if not hasattr(self, 'loop_off_button'):
            return
        
        status = self.audio_system.get_status()
        current_mode = RepeatMode(status['repeat_mode'])
        
        buttons = [
            (self.loop_off_button, RepeatMode.OFF),
            (self.single_loop_button, RepeatMode.SINGLE),
            (self.playlist_loop_button, RepeatMode.PLAYLIST)
        ]
        
        for button, mode in buttons:
            if current_mode == mode:
                button.config(bg="#00FF88", fg="#000000")
            else:
                button.config(bg="#333335", fg="#FFFFFF")
    
    def _update_playlist_display(self):
        """Update the playlist display"""
        if hasattr(self, 'playlist_listbox'):
            self.playlist_listbox.delete(0, tk.END)
            
            tracks = self.audio_system.get_playlist_tracks()
            for track_info in tracks:
                i = track_info['index']
                title = track_info['title']
                artist = track_info['artist']
                display_text = f"{i+1:2d}. {artist} - {title}"
                
                self.playlist_listbox.insert(tk.END, display_text)
                
                # Highlight current track
                if track_info['is_current']:
                    self.playlist_listbox.selection_set(i)
    
    def _update_status(self):
        """Update status display"""
        if self.status_label:
            status = self.audio_system.get_status()
            playback_state = status['playback_state']
            
            if playback_state == 'playing':
                state = "> Playing"
            elif playback_state == 'paused':
                state = "|| Paused"
            else:
                state = "Stop Stopped"
            
            repeat_display = status['repeat_display']
            playlist_size = status['playlist_size']
            
            status_text = f"{state} | {repeat_display} | {playlist_size} tracks"
            self.status_label.config(text=status_text)
    
    def _on_track_change(self, track, index, total):
        """Callback when track changes - not needed with new system"""
        # New modular system handles events internally
        pass
    
    def _on_loop_mode_change(self, mode):
        """Callback when loop mode changes - not needed with new system"""
        # New modular system handles events internally
        if self.control_window and self.control_window.winfo_exists():
            self._update_loop_buttons()
            self._update_status()