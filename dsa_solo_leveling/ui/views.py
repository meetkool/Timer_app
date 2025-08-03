"""
Views/Screens for DSA Solo Leveling Application

Main application screens with solo leveling theme:
- MainDashboard: Overview of all dungeons/steps
- QuestView: Detailed view of a specific step
- TopicDetailView: Individual topic/question view
"""

import pygame
from typing import List, Optional, Callable
from abc import ABC, abstractmethod

from models.data_models import Step, SubStep, Topic, PlayerStats, QuestStatus
from ui.components import (
    UIComponent, Button, ProgressBar, Dropdown, ChecklistItem, 
    StepCard, PlayerStatsPanel, ComponentStyle, ComponentState
)


class View(ABC):
    """Abstract base class for all views"""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.components: List[UIComponent] = []
        self.background_color = (20, 20, 30)  # Dark theme
        self._title_font = None  # Lazy initialization
        self._subtitle_font = None  # Lazy initialization
    
    @property
    def title_font(self):
        """Lazy initialization of title font"""
        if self._title_font is None:
            self._title_font = pygame.font.Font(None, 32)
        return self._title_font
    
    @property
    def subtitle_font(self):
        """Lazy initialization of subtitle font"""
        if self._subtitle_font is None:
            self._subtitle_font = pygame.font.Font(None, 24)
        return self._subtitle_font
    
    @abstractmethod
    def update(self, dt: float):
        """Update view state"""
        pass
    
    @abstractmethod
    def draw(self, surface: pygame.Surface):
        """Draw the view"""
        pass
    
    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle events. Return True if event was consumed."""
        pass
    
    def add_component(self, component: UIComponent):
        """Add a UI component to this view"""
        self.components.append(component)
    
    def remove_component(self, component: UIComponent):
        """Remove a UI component from this view"""
        if component in self.components:
            self.components.remove(component)


class MainDashboard(View):
    """Main dashboard showing all available dungeons/steps"""
    
    def __init__(self, width: int, height: int, steps: List[Step], player_stats: PlayerStats,
                 on_step_selected: Optional[Callable[[Step], None]] = None):
        super().__init__(width, height)
        self.steps = steps
        self.player_stats = player_stats
        self.on_step_selected = on_step_selected
        
        # Scroll functionality
        self.scroll_offset = 0
        self.max_scroll = 0
        
        # Create style for solo leveling theme
        self.style = ComponentStyle(
            bg_color=(25, 25, 35),
            text_color=(220, 220, 220),
            border_color=(100, 150, 200),
            hover_color=(40, 40, 55),
            accent_color=(0, 150, 255),
            success_color=(0, 200, 100),
            warning_color=(255, 180, 0),
            danger_color=(255, 80, 80)
        )
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup UI components"""
        # Player stats panel
        stats_panel = PlayerStatsPanel(
            x=self.width - 280, y=20, width=260, height=200,
            player_stats=self.player_stats, style=self.style
        )
        self.add_component(stats_panel)
        
        # Fullscreen toggle button (top-right corner)
        fullscreen_button = Button(
            x=self.width - 120, y=230, width=100, height=35,
            text="⛶ Fullscreen", callback=self._toggle_fullscreen, style=self.style
        )
        self.add_component(fullscreen_button)
        
        # Title area
        self.title_y = 20
        
        self._create_step_cards()
    
    def _create_step_cards(self):
        """Create step cards with scrolling support"""
        # Remove existing step cards
        self.components = [c for c in self.components if not isinstance(c, StepCard)]
        
        # Step cards grid - make more compact to fit all steps
        card_width = 280
        card_height = 100
        cards_per_row = 3  # More columns to fit better
        start_x = 20
        start_y = 100
        spacing_x = 15
        spacing_y = 15
        
        total_rows = (len(self.steps) + cards_per_row - 1) // cards_per_row
        total_height = total_rows * (card_height + spacing_y)
        available_height = self.height - start_y - 20
        self.max_scroll = max(0, total_height - available_height)
        
        for i, step in enumerate(self.steps):
            row = i // cards_per_row
            col = i % cards_per_row
            
            x = start_x + col * (card_width + spacing_x)
            y = start_y + row * (card_height + spacing_y) - self.scroll_offset
            
            # Only create cards that are visible
            if y > -card_height and y < self.height:
                step_card = StepCard(
                    x=x, y=y, width=card_width, height=card_height,
                    step=step, callback=self._on_step_clicked, style=self.style
                )
                self.add_component(step_card)
    
    def _on_step_clicked(self, step: Step):
        """Handle step card click"""
        if self.on_step_selected:
            self.on_step_selected(step)
    
    def update(self, dt: float):
        """Update dashboard state"""
        for component in self.components:
            component.update(dt)
    
    def draw(self, surface: pygame.Surface):
        """Draw the dashboard"""
        # Fill background with gradient effect
        surface.fill(self.background_color)
        
        # Draw animated background pattern (solo leveling style)
        self._draw_background_pattern(surface)
        
        # Draw title
        title_text = "DSA SOLO LEVELING"
        title_surface = self.title_font.render(title_text, True, (0, 200, 255))
        title_rect = title_surface.get_rect()
        title_rect.centerx = self.width // 2
        title_rect.y = self.title_y
        surface.blit(title_surface, title_rect)
        
        # Draw subtitle
        subtitle_text = "Choose Your Dungeon to Conquer"
        subtitle_surface = self.subtitle_font.render(subtitle_text, True, (150, 150, 150))
        subtitle_rect = subtitle_surface.get_rect()
        subtitle_rect.centerx = self.width // 2
        subtitle_rect.y = title_rect.bottom + 10
        surface.blit(subtitle_surface, subtitle_rect)
        
        # Draw components
        for component in self.components:
            component.draw(surface)
        
        # Draw scroll indicator if needed
        if self.max_scroll > 0:
            scroll_bar_height = max(20, int((self.height - 100) * (self.height - 100) / (self.max_scroll + self.height - 100)))
            scroll_bar_y = 100 + int((self.scroll_offset / self.max_scroll) * (self.height - 100 - scroll_bar_height))
            
            # Draw scroll track
            pygame.draw.rect(surface, (50, 50, 50), (self.width - 300, 100, 10, self.height - 120))
            # Draw scroll handle
            pygame.draw.rect(surface, (100, 100, 100), (self.width - 300, scroll_bar_y, 10, scroll_bar_height))
    
    def _draw_background_pattern(self, surface: pygame.Surface):
        """Draw animated background pattern"""
        import math
        
        # Draw subtle grid pattern
        grid_color = (30, 30, 40)
        grid_size = 50
        
        for x in range(0, self.width, grid_size):
            pygame.draw.line(surface, grid_color, (x, 0), (x, self.height))
        
        for y in range(0, self.height, grid_size):
            pygame.draw.line(surface, grid_color, (0, y), (self.width, y))
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle dashboard events"""
        # Handle scrolling
        if event.type == pygame.MOUSEWHEEL:
            scroll_speed = 30
            self.scroll_offset -= event.y * scroll_speed
            self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
            self._create_step_cards()  # Refresh visible cards
            return True
        
        for component in self.components:
            if component.handle_event(event):
                return True
        return False
    
    def _toggle_fullscreen(self):
        """Toggle fullscreen mode (same as F11)"""
        pygame.display.toggle_fullscreen()


class QuestView(View):
    """Detailed view of a specific step with sub-steps and topics"""
    
    def __init__(self, width: int, height: int, step: Step,
                 on_back: Optional[Callable[[], None]] = None,
                 on_topic_status_changed: Optional[Callable[[Topic], None]] = None):
        super().__init__(width, height)
        self.step = step
        self.on_back = on_back
        self.on_topic_status_changed = on_topic_status_changed
        self.selected_substep_index = 0
        
        # Scroll offset for topic list
        self.scroll_offset = 0
        self.max_scroll = 0
        
        self.style = ComponentStyle(
            bg_color=(25, 25, 35),
            text_color=(220, 220, 220),
            border_color=(100, 150, 200),
            hover_color=(40, 40, 55),
            accent_color=(0, 150, 255)
        )
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup UI components"""
        # Back button
        back_button = Button(
            x=20, y=20, width=100, height=40,
            text="← Back", callback=self._on_back_clicked, style=self.style
        )
        self.add_component(back_button)
        
        # Step progress bar
        progress_bar = ProgressBar(
            x=20, y=80, width=400, height=30,
            max_value=self.step.total_topics,
            current_value=self.step.completed_topics,
            style=self.style
        )
        self.add_component(progress_bar)
        
        # Sub-step dropdown
        if self.step.sub_steps:
            substep_options = [f"{ss.sub_step_title}" for ss in self.step.sub_steps]
            substep_dropdown = Dropdown(
                x=450, y=80, width=300, height=30,
                options=substep_options,
                selected_index=self.selected_substep_index,
                callback=self._on_substep_selected,
                style=self.style
            )
            self.add_component(substep_dropdown)
        
        self._update_topic_list()
    
    def _update_topic_list(self):
        """Update the topic checklist based on selected sub-step"""
        # Remove existing topic items
        self.components = [c for c in self.components if not isinstance(c, ChecklistItem)]
        
        if not self.step.sub_steps or self.selected_substep_index >= len(self.step.sub_steps):
            return
        
        selected_substep = self.step.sub_steps[self.selected_substep_index]
        
        # Create checklist items for topics
        item_height = 50
        start_y = 140
        
        for i, topic in enumerate(selected_substep.topics):
            y_pos = start_y + i * (item_height + 5) - self.scroll_offset
            
            # Only create items that are visible
            if y_pos > -item_height and y_pos < self.height:
                topic_item = ChecklistItem(
                    x=20, y=y_pos, width=self.width - 40, height=item_height,
                    topic=topic, callback=self._on_topic_clicked, style=self.style
                )
                topic_item.show_tooltip = True  # Enable tooltips by default
                self.add_component(topic_item)
        
        # Calculate max scroll
        total_height = len(selected_substep.topics) * (item_height + 5)
        self.max_scroll = max(0, total_height - (self.height - start_y - 20))
    
    def _on_back_clicked(self):
        """Handle back button click"""
        if self.on_back:
            self.on_back()
    
    def _on_substep_selected(self, index: int, option: str):
        """Handle sub-step selection"""
        self.selected_substep_index = index
        self.scroll_offset = 0  # Reset scroll
        self._update_topic_list()
    
    def _on_topic_clicked(self, topic: Topic):
        """Handle topic status change"""
        if self.on_topic_status_changed:
            self.on_topic_status_changed(topic)
        
        # Update progress bar
        for component in self.components:
            if isinstance(component, ProgressBar):
                component.set_progress(self.step.completed_topics, self.step.total_topics)
    
    def update(self, dt: float):
        """Update quest view state"""
        for component in self.components:
            component.update(dt)
    
    def draw(self, surface: pygame.Surface):
        """Draw the quest view"""
        surface.fill(self.background_color)
        
        # Draw background pattern
        self._draw_background_pattern(surface)
        
        # Draw step title
        title_text = f"Step {self.step.step_no}: {self.step.step_title}"
        title_surface = self.title_font.render(title_text, True, (0, 200, 255))
        title_rect = title_surface.get_rect()
        title_rect.x = 140
        title_rect.y = 25
        surface.blit(title_surface, title_rect)
        
        # Draw selected sub-step info
        if self.step.sub_steps and self.selected_substep_index < len(self.step.sub_steps):
            selected_substep = self.step.sub_steps[self.selected_substep_index]
            substep_text = f"Sub-step: {selected_substep.sub_step_title}"
            substep_surface = self.subtitle_font.render(substep_text, True, (150, 150, 150))
            surface.blit(substep_surface, (450, 50))
            
            # Draw sub-step progress and stats
            progress_text = f"{selected_substep.completed_topics}/{selected_substep.total_topics} completed"
            progress_font = pygame.font.Font(None, 18)
            progress_surface = progress_font.render(progress_text, True, (200, 200, 200))
            surface.blit(progress_surface, (450, 115))
            
            # Show completion percentage
            completion_pct = selected_substep.completion_percentage
            pct_text = f"({completion_pct:.1f}%)"
            pct_color = (0, 255, 100) if completion_pct >= 100 else (255, 180, 0) if completion_pct >= 50 else (255, 100, 100)
            pct_surface = progress_font.render(pct_text, True, pct_color)
            surface.blit(pct_surface, (550, 115))
            
            # Show difficulty distribution
            if selected_substep.topics:
                difficulty_counts = [0, 0, 0, 0]  # Beginner, Easy, Medium, Hard
                for topic in selected_substep.topics:
                    if 0 <= topic.difficulty <= 3:
                        difficulty_counts[topic.difficulty] += 1
                
                diff_text = f"📊 Difficulty: BGN:{difficulty_counts[0]} EZ:{difficulty_counts[1]} MED:{difficulty_counts[2]} HRD:{difficulty_counts[3]}"
                diff_surface = pygame.font.Font(None, 16).render(diff_text, True, (150, 150, 150))
                surface.blit(diff_surface, (450, 135))
        
        # Draw components in three phases to handle z-order properly
        # Phase 1: Draw all components except expanded dropdowns and tooltips
        expanded_dropdowns = []
        tooltip_items = []
        
        for component in self.components:
            if isinstance(component, Dropdown) and component.expanded:
                # Store expanded dropdowns for later
                expanded_dropdowns.append(component)
                # Draw the dropdown base (without expanded options)
                component._draw_base_only(surface)
            elif isinstance(component, ChecklistItem) and component.show_tooltip and component.state == ComponentState.HOVER:
                # Store tooltip items for later
                tooltip_items.append(component)
                # Draw the checklist item base (without tooltip)
                component._draw_base_only(surface)
            else:
                component.draw(surface)
        
        # Phase 2: Draw expanded dropdowns on top of regular components
        for dropdown in expanded_dropdowns:
            dropdown._draw_expanded_options_only(surface)
        
        # Phase 3: Draw tooltips on top of everything (highest z-order)
        for tooltip_item in tooltip_items:
            tooltip_item._draw_tooltip_only(surface)
        
        # Draw scroll indicator if needed
        if self.max_scroll > 0:
            scroll_bar_height = max(20, int((self.height - 140) * (self.height - 140) / (self.max_scroll + self.height - 140)))
            scroll_bar_y = 140 + int((self.scroll_offset / self.max_scroll) * (self.height - 140 - scroll_bar_height))
            
            pygame.draw.rect(surface, (100, 100, 100), 
                           (self.width - 15, scroll_bar_y, 10, scroll_bar_height))
    
    def _draw_background_pattern(self, surface: pygame.Surface):
        """Draw subtle background pattern"""
        grid_color = (30, 30, 40)
        grid_size = 50
        
        for x in range(0, self.width, grid_size):
            pygame.draw.line(surface, grid_color, (x, 0), (x, self.height))
        
        for y in range(0, self.height, grid_size):
            pygame.draw.line(surface, grid_color, (0, y), (self.width, y))
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle quest view events"""
        # Handle scrolling
        if event.type == pygame.MOUSEWHEEL:
            scroll_speed = 30
            self.scroll_offset -= event.y * scroll_speed
            self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
            self._update_topic_list()  # Refresh visible items
            return True
        
        # Handle tooltip toggle
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:  # Press 'T' to toggle tooltips
                for component in self.components:
                    if isinstance(component, ChecklistItem):
                        component.show_tooltip = not component.show_tooltip
                return True
        
        # Handle component events
        for component in self.components:
            if component.handle_event(event):
                return True
        
        return False


class TopicDetailView(View):
    """Detailed view of an individual topic/question"""
    
    def __init__(self, width: int, height: int, topic: Topic,
                 on_back: Optional[Callable[[], None]] = None):
        super().__init__(width, height)
        self.topic = topic
        self.on_back = on_back
        
        self.style = ComponentStyle(
            bg_color=(25, 25, 35),
            text_color=(220, 220, 220),
            border_color=(100, 150, 200),
            hover_color=(40, 40, 55),
            accent_color=(0, 150, 255)
        )
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup UI components"""
        # Back button
        back_button = Button(
            x=20, y=20, width=100, height=40,
            text="← Back", callback=self._on_back_clicked, style=self.style
        )
        self.add_component(back_button)
        
        # Action buttons with specific naming scheme
        button_y = self.height - 120  # More space for additional buttons
        button_width = 110
        button_spacing = 115
        start_x = 20
        button_row_2_y = self.height - 70
        
        # First row of buttons - Primary actions
        current_x = start_x
        
        # Solve button (LeetCode) - Orange
        if self.topic.lc_link:
            solve_button = Button(
                x=current_x, y=button_y, width=button_width, height=35,
                text="🔗 Solve", callback=lambda: self._open_link(self.topic.lc_link),
                style=self.style
            )
            self.add_component(solve_button)
            current_x += button_spacing
        
        # Solution button (YouTube) - Red  
        if self.topic.yt_link:
            solution_button = Button(
                x=current_x, y=button_y, width=button_width, height=35,
                text="📺 Solution", callback=lambda: self._open_link(self.topic.yt_link),
                style=self.style
            )
            self.add_component(solution_button)
            current_x += button_spacing
        
        # Blog button (post_link) - Blue
        if self.topic.post_link:
            blog_button = Button(
                x=current_x, y=button_y, width=button_width, height=35,
                text="📖 Blog", callback=lambda: self._open_link(self.topic.post_link),
                style=self.style
            )
            self.add_component(blog_button)
            current_x += button_spacing
        
        # Second row of buttons - Additional resources
        current_x = start_x
        
        if self.topic.editorial_link:
            tutorial_button = Button(
                x=current_x, y=button_row_2_y, width=button_width, height=35,
                text="📝 Tutorial", callback=lambda: self._open_link(self.topic.editorial_link),
                style=self.style
            )
            self.add_component(tutorial_button)
            current_x += button_spacing
        
        if self.topic.plus_link:
            striver_button = Button(
                x=current_x, y=button_row_2_y, width=button_width, height=35,
                text="🚀 Striver", callback=lambda: self._open_link(self.topic.plus_link),
                style=self.style
            )
            self.add_component(striver_button)
            current_x += button_spacing
    
    def _on_back_clicked(self):
        """Handle back button click"""
        if self.on_back:
            self.on_back()
    
    def _open_link(self, url: str):
        """Open link in browser"""
        import webbrowser
        webbrowser.open(url)
    
    def update(self, dt: float):
        """Update topic detail view"""
        for component in self.components:
            component.update(dt)
    
    def draw(self, surface: pygame.Surface):
        """Draw the topic detail view"""
        surface.fill(self.background_color)
        
        # Draw background pattern
        self._draw_background_pattern(surface)
        
        # Draw topic title with solve button (like second screenshot)
        title_surface = self.title_font.render(self.topic.question_title, True, (0, 200, 255))
        title_rect = title_surface.get_rect()
        title_rect.x = 140
        title_rect.y = 25
        surface.blit(title_surface, title_rect)
        
        # Main solve button (top-right, like in second screenshot) - LeetCode only
        main_solve_rect = pygame.Rect(self.width - 120, 25, 80, 35)
        if self.topic.lc_link:  # Only show if LeetCode link exists
            pygame.draw.rect(surface, (255, 100, 50), main_solve_rect, border_radius=6)
            pygame.draw.rect(surface, (255, 255, 255), main_solve_rect, 2, border_radius=6)
            
            solve_font = pygame.font.Font(None, 20)
            solve_text = solve_font.render("Solve", True, (255, 255, 255))
            solve_text_rect = solve_text.get_rect(center=main_solve_rect.center)
            surface.blit(solve_text, solve_text_rect)
            
            # Store for click handling
            self.main_solve_rect = main_solve_rect
            self.main_solve_link = self.topic.lc_link
        else:
            self.main_solve_rect = None
            self.main_solve_link = None
        
        # Draw topic details with all fields
        y_offset = 80
        detail_font = pygame.font.Font(None, 20)
        header_font = pygame.font.Font(None, 22)
        
        # Main details section
        details = [
            f"📚 Step {self.topic.step_no}: {self.topic.step_title}",
            f"📖 Sub-step {self.topic.sub_step_no}: {self.topic.sub_step_title}",
            f"🆔 Topic ID: {self.topic.id}",
            f"📊 Serial Number: {self.topic.sl_no}",
        ]
        
        for detail in details:
            detail_surface = detail_font.render(detail, True, (200, 200, 200))
            surface.blit(detail_surface, (30, y_offset))
            y_offset += 25
        
        y_offset += 10
        
        # Difficulty and Status
        difficulty_colors = {
            0: (100, 255, 100),  # Beginner - Green
            1: (255, 255, 100),  # Easy - Yellow  
            2: (255, 150, 100),  # Medium - Orange
            3: (255, 100, 100)   # Hard - Red
        }
        
        difficulty_names = {0: "Beginner", 1: "Easy", 2: "Medium", 3: "Hard"}
        diff_color = difficulty_colors.get(self.topic.difficulty, (200, 200, 200))
        diff_name = difficulty_names.get(self.topic.difficulty, "Unknown")
        
        difficulty_text = f"🎯 Difficulty: {diff_name}"
        difficulty_surface = detail_font.render(difficulty_text, True, diff_color)
        surface.blit(difficulty_surface, (30, y_offset))
        y_offset += 30
        
        status_text = f"✅ Status: {self.topic.status.value.replace('_', ' ').title()}"
        status_surface = detail_font.render(status_text, True, (200, 200, 200))
        surface.blit(status_surface, (30, y_offset))
        y_offset += 35
        
        # Topic tags if available
        if self.topic.ques_topic and self.topic.ques_topic.strip():
            try:
                import json
                topic_data = json.loads(self.topic.ques_topic)
                if topic_data:
                    tags_text = "🏷️  Topics: " + ", ".join([tag.get('label', tag.get('value', '')) for tag in topic_data])
                    if len(tags_text) > 80:  # Truncate if too long
                        tags_text = tags_text[:77] + "..."
                    tags_surface = detail_font.render(tags_text, True, (150, 200, 255))
                    surface.blit(tags_surface, (30, y_offset))
                    y_offset += 25
            except:
                pass  # Skip if JSON parsing fails
        
        # Company tags if available
        if self.topic.company_tags:
            company_text = f"🏢 Companies: {self.topic.company_tags}"
            if len(company_text) > 80:
                company_text = company_text[:77] + "..."
            company_surface = detail_font.render(company_text, True, (255, 200, 150))
            surface.blit(company_surface, (30, y_offset))
            y_offset += 25
        
        # Draw components
        for component in self.components:
            component.draw(surface)
    
    def _draw_background_pattern(self, surface: pygame.Surface):
        """Draw subtle background pattern"""
        grid_color = (30, 30, 40)
        grid_size = 50
        
        for x in range(0, self.width, grid_size):
            pygame.draw.line(surface, grid_color, (x, 0), (x, self.height))
        
        for y in range(0, self.height, grid_size):
            pygame.draw.line(surface, grid_color, (0, y), (self.width, y))
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle topic detail events"""
        # Handle main solve button click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if hasattr(self, 'main_solve_rect') and self.main_solve_rect and self.main_solve_rect.collidepoint(mouse_pos):
                if self.main_solve_link:
                    self._open_link(self.main_solve_link)
                    return True
        
        for component in self.components:
            if component.handle_event(event):
                return True
        return False