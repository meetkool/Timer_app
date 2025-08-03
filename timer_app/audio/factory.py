"""
Audio System Factory - Following Dependency Inversion Principle (SOLID)
Creates the complete audio system with proper dependency injection.
"""
from .interfaces import AudioSystemInterface
from .player import PygameAudioPlayer
from .playlist import AudioPlaylist
from .loop_controller import LoopController
from .system import ModularAudioSystem


class AudioSystemFactory:
    """Factory for creating audio system with dependency injection (SOLID DIP)"""
    
    @staticmethod
    def create_audio_system() -> AudioSystemInterface:
        """
        Create complete audio system with all dependencies properly injected
        Following Dependency Inversion Principle - high-level modules don't depend on low-level modules
        """
        # Create concrete implementations (low-level modules)
        player = PygameAudioPlayer()
        playlist = AudioPlaylist()
        loop_controller = LoopController(playlist)
        
        # Inject dependencies into high-level module
        audio_system = ModularAudioSystem(player, playlist, loop_controller)
        
        print("🏭 Modular audio system created with dependency injection")
        return audio_system
    
    @staticmethod
    def create_custom_audio_system(player_impl=None, playlist_impl=None, loop_impl=None) -> AudioSystemInterface:
        """
        Create audio system with custom implementations (Open/Closed Principle)
        Allows extending functionality without modifying existing code
        """
        # Use custom implementations if provided, otherwise use defaults
        player = player_impl or PygameAudioPlayer()
        playlist = playlist_impl or AudioPlaylist()
        loop_controller = loop_impl or LoopController(playlist)
        
        audio_system = ModularAudioSystem(player, playlist, loop_controller)
        
        print("🏭 Custom audio system created")
        return audio_system