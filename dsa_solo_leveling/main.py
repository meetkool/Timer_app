"""
DSA Solo Leveling - Main Application

A gamified DSA learning application inspired by Solo Leveling
where users progress through different "dungeons" (topics) and
level up their programming skills.

Following SOLID principles throughout the application architecture.
"""

import pygame
import sys
import os
from typing import Optional, Dict, Any
from enum import Enum

# Add the project root to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.data_models import (
    JSONDataLoader, ProgressTracker, PlayerStats, Step, Topic, QuestStatus
)
from ui.views import MainDashboard, QuestView, TopicDetailView


class GameState(Enum):
    """Game states for navigation"""
    MAIN_DASHBOARD = "main_dashboard"
    QUEST_VIEW = "quest_view"
    TOPIC_DETAIL = "topic_detail"


class DSASoloLevelingApp:
    """Main application class for DSA Solo Leveling"""
    
    def __init__(self, data_file_path: str):
        # Initialize Pygame
        pygame.init()
        
        # Screen settings
        self.SCREEN_WIDTH = 1200
        self.SCREEN_HEIGHT = 800
        self.FPS = 60
        
        # Setup display
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("DSA Solo Leveling - Conquer Your Programming Journey")
        
        # Load icon if available
        try:
            icon = pygame.image.load("icon.ico")
            pygame.display.set_icon(icon)
        except:
            pass  # Ignore if icon not found
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game state management
        self.current_state = GameState.MAIN_DASHBOARD
        self.state_stack = []
        
        # Data management
        self.data_loader = JSONDataLoader(data_file_path)
        self.progress_tracker = ProgressTracker()
        self.player_stats = PlayerStats()
        
        # Load data
        self.steps = self.data_loader.load_data()
        self.progress_tracker.load_progress()
        self._apply_progress_to_steps()
        
        # Views
        self.views: Dict[GameState, Any] = {}
        self.current_view = None
        
        # Initialize views
        self._setup_views()
        
        # Selected data for navigation
        self.selected_step: Optional[Step] = None
        self.selected_topic: Optional[Topic] = None
    
    def _setup_views(self):
        """Initialize all views"""
        # Main dashboard
        self.views[GameState.MAIN_DASHBOARD] = MainDashboard(
            width=self.SCREEN_WIDTH,
            height=self.SCREEN_HEIGHT,
            steps=self.steps,
            player_stats=self.player_stats,
            on_step_selected=self._on_step_selected
        )
        
        self.current_view = self.views[GameState.MAIN_DASHBOARD]
    
    def _apply_progress_to_steps(self):
        """Apply saved progress to loaded steps"""
        for step in self.steps:
            for sub_step in step.sub_steps:
                for topic in sub_step.topics:
                    topic.status = self.progress_tracker.get_topic_status(topic.id)
    
    def _on_step_selected(self, step: Step):
        """Handle step selection from main dashboard"""
        self.selected_step = step
        self._change_state(GameState.QUEST_VIEW)
    
    def _on_topic_selected(self, topic: Topic):
        """Handle topic selection from quest view"""
        self.selected_topic = topic
        self._change_state(GameState.TOPIC_DETAIL)
    
    def _on_topic_status_changed(self, topic: Topic):
        """Handle topic status change"""
        # Update progress tracker
        self.progress_tracker.update_topic_status(topic.id, topic.status)
        
        # Update player stats
        if topic.status == QuestStatus.COMPLETED:
            self.player_stats.gain_experience(10 + topic.difficulty * 5)
            self.player_stats.total_completed += 1
        
        # Save progress
        self.progress_tracker.save_progress()
        self._save_player_stats()
    
    def _change_state(self, new_state: GameState):
        """Change application state and setup corresponding view"""
        self.state_stack.append(self.current_state)
        self.current_state = new_state
        
        if new_state == GameState.QUEST_VIEW and self.selected_step:
            self.views[GameState.QUEST_VIEW] = QuestView(
                width=self.SCREEN_WIDTH,
                height=self.SCREEN_HEIGHT,
                step=self.selected_step,
                on_back=self._go_back,
                on_topic_status_changed=self._on_topic_status_changed
            )
            self.current_view = self.views[GameState.QUEST_VIEW]
        
        elif new_state == GameState.TOPIC_DETAIL and self.selected_topic:
            self.views[GameState.TOPIC_DETAIL] = TopicDetailView(
                width=self.SCREEN_WIDTH,
                height=self.SCREEN_HEIGHT,
                topic=self.selected_topic,
                on_back=self._go_back
            )
            self.current_view = self.views[GameState.TOPIC_DETAIL]
    
    def _go_back(self):
        """Go back to previous state"""
        if self.state_stack:
            previous_state = self.state_stack.pop()
            self.current_state = previous_state
            
            if previous_state in self.views:
                self.current_view = self.views[previous_state]
                
                # Refresh main dashboard if returning to it
                if previous_state == GameState.MAIN_DASHBOARD:
                    self._setup_views()  # Refresh to update progress
    
    def _save_player_stats(self):
        """Save player statistics"""
        stats_data = {
            'level': self.player_stats.level,
            'experience': self.player_stats.experience,
            'total_completed': self.player_stats.total_completed,
            'streak': self.player_stats.streak,
            'rank': self.player_stats.rank
        }
        
        try:
            import json
            with open('player_stats.json', 'w') as f:
                json.dump(stats_data, f, indent=2)
        except Exception as e:
            print(f"Error saving player stats: {e}")
    
    def _load_player_stats(self):
        """Load player statistics"""
        try:
            import json
            with open('player_stats.json', 'r') as f:
                stats_data = json.load(f)
                
            self.player_stats.level = stats_data.get('level', 1)
            self.player_stats.experience = stats_data.get('experience', 0)
            self.player_stats.total_completed = stats_data.get('total_completed', 0)
            self.player_stats.streak = stats_data.get('streak', 0)
            self.player_stats.rank = stats_data.get('rank', 'E-Rank Hunter')
        except FileNotFoundError:
            pass  # Use default stats
        except Exception as e:
            print(f"Error loading player stats: {e}")
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            # Handle keyboard shortcuts
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.current_state != GameState.MAIN_DASHBOARD:
                        self._go_back()
                    else:
                        self.running = False
                elif event.key == pygame.K_F11:
                    # Toggle fullscreen
                    pygame.display.toggle_fullscreen()
            
            # Let current view handle the event
            if self.current_view and self.current_view.handle_event(event):
                continue  # Event was handled by view
    
    def update(self, dt: float):
        """Update game state"""
        if self.current_view:
            self.current_view.update(dt)
    
    def draw(self):
        """Draw everything"""
        if self.current_view:
            self.current_view.draw(self.screen)
        
        # Draw FPS counter in debug mode
        if hasattr(self, 'debug_mode') and self.debug_mode:
            fps_text = f"FPS: {int(self.clock.get_fps())}"
            debug_font = pygame.font.Font(None, 24)
            fps_surface = debug_font.render(fps_text, True, (255, 255, 255))
            self.screen.blit(fps_surface, (10, 10))
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        # Load player stats
        self._load_player_stats()
        
        print("🎮 DSA Solo Leveling - Starting your programming journey!")
        print(f"📊 Loaded {len(self.steps)} steps with {sum(step.total_topics for step in self.steps)} total topics")
        print(f"🏆 Current Rank: {self.player_stats.rank} (Level {self.player_stats.level})")
        print("🎯 Use ESC to go back/quit, F11 to toggle fullscreen")
        
        while self.running:
            # Calculate delta time
            dt = self.clock.tick(self.FPS) / 1000.0
            
            # Handle events
            self.handle_events()
            
            # Update
            self.update(dt)
            
            # Draw
            self.draw()
        
        # Cleanup
        self._save_player_stats()
        self.progress_tracker.save_progress()
        pygame.quit()
        
        print("👋 Thanks for using DSA Solo Leveling! Keep grinding those algorithms!")


def main():
    """Entry point for the application"""
    # Check if data file exists
    data_file = "dsa_queastions.json"
    if not os.path.exists(data_file):
        print(f"❌ Error: Data file '{data_file}' not found!")
        print("📁 Please ensure the DSA questions JSON file is in the same directory.")
        return
    
    try:
        # Create and run the application
        app = DSASoloLevelingApp(data_file)
        app.run()
    
    except KeyboardInterrupt:
        print("\n👋 Application interrupted by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()