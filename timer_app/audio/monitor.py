"""
Playback Monitor - Following Single Responsibility Principle (SOLID)
This class only handles monitoring playback and coordinating loop events.
"""
import threading
import time
from typing import Optional, Callable
from .interfaces import AudioPlayerInterface, PlaylistInterface, LoopControlInterface, PlaybackEventInterface, PlaybackState


class PlaybackMonitor:
    """Monitors playback and coordinates loop events (Single Responsibility)"""
    
    def __init__(self, 
                 player: AudioPlayerInterface,
                 playlist: PlaylistInterface, 
                 loop_controller: LoopControlInterface,
                 event_handler: Optional[PlaybackEventInterface] = None):
        self._player = player
        self._playlist = playlist
        self._loop_controller = loop_controller
        self._event_handler = event_handler
        
        # Threading control
        self._monitor_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._is_monitoring = False
        self._monitor_interval = 0.1  # Check every 100ms for better responsiveness
    
    def start_monitoring(self) -> None:
        """Start monitoring playback (Single Responsibility)"""
        if self._is_monitoring:
            print("⚠️ Monitor already running")
            return
        
        self.stop_monitoring()  # Ensure clean state
        
        self._stop_event.clear()
        self._is_monitoring = True
        self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()
        print("👁️ Playback monitor started")
    
    def stop_monitoring(self) -> None:
        """Stop monitoring playback (Single Responsibility)"""
        if not self._is_monitoring:
            return
        
        self._is_monitoring = False
        self._stop_event.set()
        
        if self._monitor_thread and self._monitor_thread.is_alive():
            self._monitor_thread.join(timeout=1.0)
        
        print("🛑 Playback monitor stopped")
    
    def _monitor_loop(self) -> None:
        """Main monitoring loop - THE CRITICAL FIX FOR LOOPING (Single Responsibility)"""
        print("🔍 Monitor loop started")
        
        while not self._stop_event.is_set() and self._is_monitoring:
            try:
                if self._player.get_state() == PlaybackState.PLAYING:
                    # Check if track finished
                    if self._player.is_track_finished():
                        print("🎵 Track finished - handling loop logic")
                        self._handle_track_finished()
                
                # Sleep with interruption check for responsiveness
                for _ in range(int(self._monitor_interval * 10)):  # 10ms increments
                    if self._stop_event.is_set():
                        break
                    time.sleep(0.01)
                    
            except Exception as e:
                print(f"❌ Monitor error: {e}")
                break
        
        print("🔍 Monitor loop ended")
    
    def _handle_track_finished(self) -> None:
        """
        Handle when a track finishes - THE KEY TO FIXING SINGLE TRACK LOOP
        This method solves the threading issue by handling everything in the monitor thread
        """
        current_track = self._playlist.get_current_track()
        current_index = self._playlist.get_current_index()
        
        if current_track and self._event_handler:
            self._event_handler.on_track_finished(current_track, current_index)
        
        # Get next action from loop controller
        next_index = self._loop_controller.handle_track_finished()
        
        if next_index is not None:
            # Load and play next track (or same track for single repeat)
            next_track = self._playlist.get_track(next_index)
            if next_track:
                print(f"🔄 Loading next track: {next_track.title}")
                
                # THE CRITICAL FIX: Load and play directly in monitor thread
                # This avoids the threading conflicts that caused single-loop failure
                if self._player.load_track(next_track):
                    if self._player.play():
                        if self._event_handler:
                            self._event_handler.on_track_started(next_track, next_index)
                        print(f"✅ Successfully looped to: {next_track.title}")
                    else:
                        print(f"❌ Failed to play: {next_track.title}")
                        self._stop_playback()
                else:
                    print(f"❌ Failed to load: {next_track.title}")
                    self._stop_playback()
            else:
                print("❌ Next track not found")
                self._stop_playback()
        else:
            # No more tracks to play
            print("⏹️ Playback completed")
            self._stop_playback()
    
    def _stop_playback(self) -> None:
        """Stop playback and monitoring"""
        self._player.stop()
        if self._event_handler:
            self._event_handler.on_playback_stopped()
        self.stop_monitoring()
    
    def set_event_handler(self, handler: PlaybackEventInterface) -> None:
        """Set event handler for callbacks"""
        self._event_handler = handler
    
    def is_monitoring(self) -> bool:
        """Check if monitoring is active"""
        return self._is_monitoring
    
    def set_monitor_interval(self, interval: float) -> None:
        """Set monitoring interval in seconds (for performance tuning)"""
        if 0.01 <= interval <= 1.0:  # Reasonable bounds
            self._monitor_interval = interval
            print(f"⏱️ Monitor interval set to {interval}s")
        else:
            print(f"❌ Invalid interval: {interval}. Must be between 0.01 and 1.0 seconds")
    
    def get_status(self) -> dict:
        """Get monitor status"""
        return {
            'is_monitoring': self._is_monitoring,
            'monitor_interval': self._monitor_interval,
            'thread_alive': self._monitor_thread.is_alive() if self._monitor_thread else False
        }