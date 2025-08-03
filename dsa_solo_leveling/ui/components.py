"""
UI Components for DSA Solo Leveling Application

Following SOLID principles for UI component design:
- Single Responsibility: Each component has a specific UI purpose
- Open/Closed: Components can be extended without modification
- Interface Segregation: Focused component interfaces
"""

import pygame
import math
import json
from typing import List, Tuple, Optional, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from models.data_models import Step, SubStep, Topic, QuestStatus, PlayerStats


class ComponentState(Enum):
    """States for interactive components"""
    NORMAL = "normal"
    HOVER = "hover"
    PRESSED = "pressed"
    DISABLED = "disabled"


@dataclass
class ComponentStyle:
    """Style configuration for UI components"""
    bg_color: Tuple[int, int, int] = (30, 30, 30)
    text_color: Tuple[int, int, int] = (255, 255, 255)
    border_color: Tuple[int, int, int] = (100, 100, 100)
    hover_color: Tuple[int, int, int] = (50, 50, 50)
    accent_color: Tuple[int, int, int] = (0, 150, 255)
    success_color: Tuple[int, int, int] = (0, 255, 100)
    warning_color: Tuple[int, int, int] = (255, 200, 0)
    danger_color: Tuple[int, int, int] = (255, 50, 50)
    font_size: int = 16
    border_width: int = 2
    padding: int = 10
    margin: int = 5


class UIComponent(ABC):
    """Abstract base class for all UI components"""
    
    def __init__(self, x: int, y: int, width: int, height: int, style: Optional[ComponentStyle] = None):
        self.rect = pygame.Rect(x, y, width, height)
        self.style = style or ComponentStyle()
        self.state = ComponentState.NORMAL
        self.visible = True
        self.enabled = True
    
    @abstractmethod
    def draw(self, surface: pygame.Surface):
        """Draw the component on the given surface"""
        pass
    
    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle pygame events. Return True if event was consumed."""
        pass
    
    def update(self, dt: float):
        """Update component state (optional override)"""
        pass
    
    def set_position(self, x: int, y: int):
        """Set component position"""
        self.rect.x = x
        self.rect.y = y
    
    def set_size(self, width: int, height: int):
        """Set component size"""
        self.rect.width = width
        self.rect.height = height
    
    def contains_point(self, pos: Tuple[int, int]) -> bool:
        """Check if point is within component bounds"""
        return self.rect.collidepoint(pos)


class Button(UIComponent):
    """Interactive button component"""
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str, 
                 callback: Optional[Callable] = None, style: Optional[ComponentStyle] = None):
        super().__init__(x, y, width, height, style)
        self.text = text
        self.callback = callback
        self._font = None  # Lazy initialization
    
    def draw(self, surface: pygame.Surface):
        if not self.visible:
            return
        
        # Choose colors based on state
        bg_color = self.style.bg_color
        text_color = self.style.text_color
        
        if self.state == ComponentState.HOVER:
            bg_color = self.style.hover_color
        elif self.state == ComponentState.PRESSED:
            bg_color = self.style.accent_color
        elif not self.enabled:
            bg_color = (50, 50, 50)
            text_color = (100, 100, 100)
        
        # Draw button background
        pygame.draw.rect(surface, bg_color, self.rect)
        pygame.draw.rect(surface, self.style.border_color, self.rect, self.style.border_width)
        
        # Draw text
        if self._font is None:
            self._font = pygame.font.Font(None, self.style.font_size)
        text_surface = self._font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        if not self.visible or not self.enabled:
            return False
        
        mouse_pos = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEMOTION:
            if self.contains_point(mouse_pos):
                self.state = ComponentState.HOVER
            else:
                self.state = ComponentState.NORMAL
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.contains_point(mouse_pos):
                self.state = ComponentState.PRESSED
                return True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.state == ComponentState.PRESSED:
                if self.contains_point(mouse_pos) and self.callback:
                    self.callback()
                self.state = ComponentState.HOVER if self.contains_point(mouse_pos) else ComponentState.NORMAL
                return True
        
        return False


class ProgressBar(UIComponent):
    """Progress bar component for showing completion status"""
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 max_value: float = 100.0, current_value: float = 0.0,
                 style: Optional[ComponentStyle] = None):
        super().__init__(x, y, width, height, style)
        self.max_value = max_value
        self.current_value = current_value
        self._font = None  # Lazy initialization
    
    def set_progress(self, current: float, maximum: float = None):
        """Update progress values"""
        self.current_value = current
        if maximum is not None:
            self.max_value = maximum
    
    def draw(self, surface: pygame.Surface):
        if not self.visible:
            return
        
        # Draw background
        pygame.draw.rect(surface, self.style.bg_color, self.rect)
        pygame.draw.rect(surface, self.style.border_color, self.rect, self.style.border_width)
        
        # Calculate progress
        progress_ratio = self.current_value / self.max_value if self.max_value > 0 else 0
        progress_width = int((self.rect.width - 2 * self.style.border_width) * progress_ratio)
        
        # Draw progress fill
        if progress_width > 0:
            progress_rect = pygame.Rect(
                self.rect.x + self.style.border_width,
                self.rect.y + self.style.border_width,
                progress_width,
                self.rect.height - 2 * self.style.border_width
            )
            
            # Color based on completion
            if progress_ratio >= 1.0:
                fill_color = self.style.success_color
            elif progress_ratio >= 0.5:
                fill_color = self.style.accent_color
            else:
                fill_color = self.style.warning_color
            
            pygame.draw.rect(surface, fill_color, progress_rect)
        
        # Draw percentage text
        percentage = f"{progress_ratio * 100:.1f}%"
        if self._font is None:
            self._font = pygame.font.Font(None, max(self.style.font_size - 4, 12))
        text_surface = self._font.render(percentage, True, self.style.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        return False  # Progress bars don't handle events


class Dropdown(UIComponent):
    """Dropdown menu component"""
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 options: List[str], selected_index: int = 0,
                 callback: Optional[Callable[[int, str], None]] = None,
                 style: Optional[ComponentStyle] = None):
        super().__init__(x, y, width, height, style)
        self.options = options
        self.selected_index = selected_index
        self.callback = callback
        self.expanded = False
        self._font = None  # Lazy initialization
        self.option_height = height
    
    def draw(self, surface: pygame.Surface):
        """Draw the dropdown (includes both base and expanded options if expanded)"""
        if not self.visible:
            return
        
        self._draw_base_only(surface)
        
        # Draw expanded options
        if self.expanded:
            self._draw_expanded_options_only(surface)
    
    def _draw_base_only(self, surface: pygame.Surface):
        """Draw only the dropdown base (without expanded options)"""
        if not self.visible:
            return
        
        # Draw main dropdown button
        bg_color = self.style.hover_color if self.state == ComponentState.HOVER else self.style.bg_color
        pygame.draw.rect(surface, bg_color, self.rect)
        pygame.draw.rect(surface, self.style.border_color, self.rect, self.style.border_width)
        
        # Draw selected option text
        if self.options and 0 <= self.selected_index < len(self.options):
            text = self.options[self.selected_index]
            if self._font is None:
                self._font = pygame.font.Font(None, self.style.font_size)
            text_surface = self._font.render(text, True, self.style.text_color)
            text_rect = text_surface.get_rect(centery=self.rect.centery)
            text_rect.x = self.rect.x + self.style.padding
            surface.blit(text_surface, text_rect)
        
        # Draw dropdown arrow
        arrow_size = 8
        arrow_x = self.rect.right - arrow_size - self.style.padding
        arrow_y = self.rect.centery
        
        if self.expanded:
            # Up arrow
            points = [
                (arrow_x, arrow_y + arrow_size // 2),
                (arrow_x + arrow_size, arrow_y + arrow_size // 2),
                (arrow_x + arrow_size // 2, arrow_y - arrow_size // 2)
            ]
        else:
            # Down arrow
            points = [
                (arrow_x, arrow_y - arrow_size // 2),
                (arrow_x + arrow_size, arrow_y - arrow_size // 2),
                (arrow_x + arrow_size // 2, arrow_y + arrow_size // 2)
            ]
        
        pygame.draw.polygon(surface, self.style.text_color, points)
    
    def _draw_expanded_options_only(self, surface: pygame.Surface):
        """Draw only the expanded dropdown options (on top layer)"""
        if not self.visible or not self.expanded:
            return
        
        for i, option in enumerate(self.options):
            option_rect = pygame.Rect(
                self.rect.x,
                self.rect.bottom + i * self.option_height,
                self.rect.width,
                self.option_height
            )
            
            # Highlight hovered option
            mouse_pos = pygame.mouse.get_pos()
            if option_rect.collidepoint(mouse_pos):
                pygame.draw.rect(surface, self.style.hover_color, option_rect)
                # Add slight border to show it's highlighted  
                pygame.draw.rect(surface, (100, 150, 255), option_rect, 2)
            else:
                pygame.draw.rect(surface, self.style.bg_color, option_rect)
            
            pygame.draw.rect(surface, self.style.border_color, option_rect, 1)
            
            # Draw option text
            if self._font is None:
                self._font = pygame.font.Font(None, self.style.font_size)
            text_surface = self._font.render(option, True, self.style.text_color)
            text_rect = text_surface.get_rect(centery=option_rect.centery)
            text_rect.x = option_rect.x + self.style.padding
            surface.blit(text_surface, text_rect)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        if not self.visible or not self.enabled:
            return False
        
        mouse_pos = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEMOTION:
            if self.contains_point(mouse_pos):
                self.state = ComponentState.HOVER
            else:
                self.state = ComponentState.NORMAL
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(mouse_pos):
                    self.expanded = not self.expanded
                    return True
                elif self.expanded:
                    # Check if clicking on an option
                    for i, option in enumerate(self.options):
                        option_rect = pygame.Rect(
                            self.rect.x,
                            self.rect.bottom + i * self.option_height,
                            self.rect.width,
                            self.option_height
                        )
                        if option_rect.collidepoint(mouse_pos):
                            self.selected_index = i
                            self.expanded = False
                            if self.callback:
                                self.callback(i, option)
                            return True
                    
                    # Clicked outside, close dropdown
                    self.expanded = False
        
        return False


class ChecklistItem(UIComponent):
    """Individual checklist item for topics"""
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 topic: Topic, callback: Optional[Callable[[Topic], None]] = None,
                 style: Optional[ComponentStyle] = None):
        super().__init__(x, y, width, height, style)
        self.topic = topic
        self.callback = callback
        self._font = None  # Lazy initialization
        self.checkbox_size = 20
        self.show_tooltip = False
        self.tooltip_buttons = []  # Store tooltip button areas
    
    def draw(self, surface: pygame.Surface):
        if not self.visible:
            return
        
        # Draw background with modern styling (matching the image hover effect)
        if self.state == ComponentState.HOVER:
            # Draw outer highlight border (like in the image)
            highlight_rect = pygame.Rect(self.rect.x - 1, self.rect.y - 1, self.rect.width + 2, self.rect.height + 2)
            pygame.draw.rect(surface, (0, 150, 255), highlight_rect, border_radius=7)  # Blue outer border
            
            bg_color = (40, 45, 60)  # Slightly lighter on hover
            border_color = (0, 180, 255)  # Brighter blue border on hover  
            border_width = 2  # Medium thickness like in the image
        else:
            bg_color = (25, 25, 35)  # Dark background
            border_color = (60, 60, 80)  # Subtle border
            border_width = 1
        
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=6)
        pygame.draw.rect(surface, border_color, self.rect, border_width, border_radius=6)
        
        # Draw checkbox
        checkbox_rect = pygame.Rect(
            self.rect.x + self.style.padding,
            self.rect.centery - self.checkbox_size // 2,
            self.checkbox_size,
            self.checkbox_size
        )
        
        # Checkbox color based on status
        if self.topic.status == QuestStatus.COMPLETED:
            pygame.draw.rect(surface, self.style.success_color, checkbox_rect)
            # Draw checkmark
            pygame.draw.lines(surface, (255, 255, 255), False, [
                (checkbox_rect.x + 4, checkbox_rect.centery),
                (checkbox_rect.x + 8, checkbox_rect.bottom - 4),
                (checkbox_rect.right - 4, checkbox_rect.y + 4)
            ], 2)
        elif self.topic.status == QuestStatus.IN_PROGRESS:
            pygame.draw.rect(surface, self.style.warning_color, checkbox_rect)
        else:
            pygame.draw.rect(surface, self.style.bg_color, checkbox_rect)
        
        pygame.draw.rect(surface, self.style.border_color, checkbox_rect, 2)
        
        # Draw topic title with difficulty label (like second screenshot)
        text_x = checkbox_rect.right + self.style.padding
        text_color = self.style.text_color
        if self.topic.status == QuestStatus.COMPLETED:
            text_color = (150, 150, 150)  # Grayed out for completed
        
        if self._font is None:
            self._font = pygame.font.Font(None, self.style.font_size)
        
        # Draw difficulty label first (like "Easy" in green in second screenshot)
        difficulty_names = ["Easy", "Medium", "Hard"]
        difficulty_colors = [(100, 255, 100), (255, 180, 0), (255, 100, 100)]
        
        if 0 <= self.topic.difficulty < len(difficulty_names):
            diff_name = difficulty_names[self.topic.difficulty]
            diff_color = difficulty_colors[self.topic.difficulty]
            
            diff_font = pygame.font.Font(None, 12)
            diff_surface = diff_font.render(diff_name, True, diff_color)
            diff_rect = diff_surface.get_rect()
            diff_rect.x = text_x
            diff_rect.y = self.rect.y + 3
            surface.blit(diff_surface, diff_rect)
            
            # Adjust title position
            title_y_offset = 12
        else:
            title_y_offset = 0
        
        # Draw main topic title
        text_surface = self._font.render(self.topic.question_title, True, text_color)
        text_rect = text_surface.get_rect()
        text_rect.x = text_x
        text_rect.y = self.rect.y + self.style.padding + title_y_offset
        
        # Truncate if too long to avoid overlap with solve button
        max_text_width = self.rect.width - text_x - 140  # Leave space for buttons
        if text_surface.get_width() > max_text_width:
            # Truncate text
            title_text = self.topic.question_title
            while text_surface.get_width() > max_text_width and len(title_text) > 10:
                title_text = title_text[:-1]
                text_surface = self._font.render(title_text + "...", True, text_color)
        
        surface.blit(text_surface, text_rect)
        
        # Draw small difficulty badge (additional indicator)
        badge_difficulty_colors = [
            (100, 255, 100),  # Easy - Green
            (255, 180, 0),    # Medium - Orange
            (255, 100, 100)   # Hard - Red
        ]
        
        difficulty_names_short = ["EZ", "MED", "HRD"]
        
        if 0 <= self.topic.difficulty < len(badge_difficulty_colors):
            difficulty_color = badge_difficulty_colors[self.topic.difficulty]
            diff_name = difficulty_names_short[self.topic.difficulty] if self.topic.difficulty < len(difficulty_names_short) else "?"
            
            # Draw small difficulty badge
            badge_width = 30
            badge_height = 14
            difficulty_rect = pygame.Rect(
                self.rect.right - badge_width - 75,  # Position left of solve button
                self.rect.bottom - badge_height - 3,
                badge_width,
                badge_height
            )
            pygame.draw.rect(surface, difficulty_color, difficulty_rect, border_radius=3)
            
            # Draw difficulty text
            diff_font = pygame.font.Font(None, 11)
            diff_surface = diff_font.render(diff_name, True, (0, 0, 0))
            diff_text_rect = diff_surface.get_rect(center=difficulty_rect.center)
            surface.blit(diff_surface, diff_text_rect)
        
        # Draw topic ID and serial number (small text)
        if hasattr(self.topic, 'sl_no') and self.topic.sl_no:
            id_font = pygame.font.Font(None, 12)
            id_text = f"#{self.topic.sl_no}"
            id_surface = id_font.render(id_text, True, (120, 120, 120))
            id_rect = id_surface.get_rect()
            id_rect.right = self.rect.right - 45
            id_rect.top = self.rect.top + 2
            surface.blit(id_surface, id_rect)
        
        # Draw action buttons: Solve (LeetCode), Solution (YouTube), Blog (Editorial)
        button_width = 50
        button_height = 18
        button_spacing = 55
        mouse_pos = pygame.mouse.get_pos()
        
        # Initialize button storage
        self.action_buttons = []
        
        # Starting position for buttons (right side)
        start_x = self.rect.right - 170
        button_y = self.rect.centery - button_height // 2
        
        # Button configurations: (text, link, color)
        buttons = [
            ("Solve", self.topic.lc_link, (255, 100, 50)),      # Orange for LeetCode
            ("Solution", self.topic.yt_link, (255, 50, 50)),    # Red for YouTube  
            ("Blog", self.topic.post_link, (50, 150, 255))      # Blue for Blog (post_link)
        ]
        
        current_x = start_x
        button_font = pygame.font.Font(None, 12)
        
        for button_text, button_link, button_color in buttons:
            if button_link:  # Only show button if link exists
                button_rect = pygame.Rect(current_x, button_y, button_width, button_height)
                
                # Hover effect
                is_hovered = button_rect.collidepoint(mouse_pos)
                display_color = tuple(min(255, c + 20) for c in button_color) if is_hovered else button_color
                
                # Draw button
                pygame.draw.rect(surface, display_color, button_rect, border_radius=3)
                pygame.draw.rect(surface, (255, 255, 255), button_rect, 1, border_radius=3)
                
                # Draw button text
                text_surface = button_font.render(button_text, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=button_rect.center)
                surface.blit(text_surface, text_rect)
                
                # Store button for click handling
                self.action_buttons.append((button_text.lower(), button_rect, button_link))
                
                current_x += button_spacing
        
        # Draw resource availability indicators
        indicator_font = pygame.font.Font(None, 10)
        indicator_x = self.rect.right - 15
        indicator_y = self.rect.top + 2
        
        # Show small icons for available resources
        available_resources = []
        if self.topic.lc_link: available_resources.append("🔗")      # LeetCode
        if self.topic.yt_link: available_resources.append("📺")      # YouTube  
        if self.topic.editorial_link: available_resources.append("📖") # Editorial
        if self.topic.post_link: available_resources.append("📝")    # Tutorial
        if self.topic.plus_link: available_resources.append("🚀")    # Practice
        
        for i, icon in enumerate(available_resources):
            icon_surface = indicator_font.render(icon, True, (200, 200, 200))
            surface.blit(icon_surface, (indicator_x - (i * 12), indicator_y))
        
        # Draw company tags indicator if available  
        if hasattr(self.topic, 'company_tags') and self.topic.company_tags:
            company_font = pygame.font.Font(None, 11)
            company_surface = company_font.render("🏢", True, (255, 200, 150))
            company_rect = company_surface.get_rect()
            company_rect.right = self.rect.right - 10
            company_rect.bottom = self.rect.bottom - 2
            surface.blit(company_surface, company_rect)
        
        # Draw tooltip if hovering
        if self.show_tooltip and self.state == ComponentState.HOVER:
            self._draw_tooltip(surface)
    
    def _draw_base_only(self, surface: pygame.Surface):
        """Draw only the checklist item base (without tooltip)"""
        if not self.visible:
            return
        
        # Draw background with modern styling (matching the image hover effect)
        if self.state == ComponentState.HOVER:
            # Draw outer highlight border (like in the image)
            highlight_rect = pygame.Rect(self.rect.x - 1, self.rect.y - 1, self.rect.width + 2, self.rect.height + 2)
            pygame.draw.rect(surface, (0, 150, 255), highlight_rect, border_radius=7)  # Blue outer border
            
            bg_color = (40, 45, 60)  # Slightly lighter on hover
            border_color = (0, 180, 255)  # Brighter blue border on hover  
            border_width = 2  # Medium thickness like in the image
        else:
            bg_color = (25, 25, 35)  # Dark background
            border_color = (60, 60, 80)  # Subtle border
            border_width = 1
        
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=6)
        pygame.draw.rect(surface, border_color, self.rect, border_width, border_radius=6)
        
        # Draw checkbox
        checkbox_rect = pygame.Rect(
            self.rect.x + self.style.padding,
            self.rect.centery - self.checkbox_size // 2,
            self.checkbox_size,
            self.checkbox_size
        )
        
        # Checkbox color based on status
        if self.topic.status == QuestStatus.COMPLETED:
            pygame.draw.rect(surface, self.style.success_color, checkbox_rect)
            # Draw checkmark
            pygame.draw.lines(surface, (255, 255, 255), False, [
                (checkbox_rect.x + 4, checkbox_rect.centery),
                (checkbox_rect.x + 8, checkbox_rect.bottom - 4),
                (checkbox_rect.right - 4, checkbox_rect.y + 4)
            ], 2)
        elif self.topic.status == QuestStatus.IN_PROGRESS:
            pygame.draw.rect(surface, self.style.warning_color, checkbox_rect)
        else:
            pygame.draw.rect(surface, self.style.bg_color, checkbox_rect)
        
        pygame.draw.rect(surface, self.style.border_color, checkbox_rect, 2)
        
        # Draw topic title with difficulty label (like second screenshot)
        text_x = checkbox_rect.right + self.style.padding
        text_color = self.style.text_color
        if self.topic.status == QuestStatus.COMPLETED:
            text_color = (150, 150, 150)  # Grayed out for completed
        
        if self._font is None:
            self._font = pygame.font.Font(None, self.style.font_size)
        
        # Draw difficulty label first (like "Easy" in green in second screenshot)
        difficulty_names = ["Easy", "Medium", "Hard"]
        difficulty_colors = [(100, 255, 100), (255, 180, 0), (255, 100, 100)]
        
        if 0 <= self.topic.difficulty < len(difficulty_names):
            diff_name = difficulty_names[self.topic.difficulty]
            diff_color = difficulty_colors[self.topic.difficulty]
            
            diff_font = pygame.font.Font(None, 12)
            diff_surface = diff_font.render(diff_name, True, diff_color)
            diff_rect = diff_surface.get_rect()
            diff_rect.x = text_x
            diff_rect.y = self.rect.y + 3
            surface.blit(diff_surface, diff_rect)
            
            # Adjust title position
            title_y_offset = 12
        else:
            title_y_offset = 0
        
        # Draw main topic title
        text_surface = self._font.render(self.topic.question_title, True, text_color)
        text_rect = text_surface.get_rect()
        text_rect.x = text_x
        text_rect.y = self.rect.y + self.style.padding + title_y_offset
        
        # Truncate if too long to avoid overlap with solve button
        max_text_width = self.rect.width - text_x - 140  # Leave space for buttons
        if text_surface.get_width() > max_text_width:
            # Truncate text
            title_text = self.topic.question_title
            while text_surface.get_width() > max_text_width and len(title_text) > 10:
                title_text = title_text[:-1]
                text_surface = self._font.render(title_text + "...", True, text_color)
        
        surface.blit(text_surface, text_rect)
        
        # Draw small difficulty badge (additional indicator)
        badge_difficulty_colors = [
            (100, 255, 100),  # Easy - Green
            (255, 180, 0),    # Medium - Orange
            (255, 100, 100)   # Hard - Red
        ]
        
        difficulty_names_short = ["EZ", "MED", "HRD"]
        
        if 0 <= self.topic.difficulty < len(badge_difficulty_colors):
            difficulty_color = badge_difficulty_colors[self.topic.difficulty]
            diff_name = difficulty_names_short[self.topic.difficulty] if self.topic.difficulty < len(difficulty_names_short) else "?"
            
            # Draw small difficulty badge
            badge_font = pygame.font.Font(None, 10)
            badge_surface = badge_font.render(diff_name, True, (255, 255, 255))
            badge_rect = pygame.Rect(self.rect.right - 35, self.rect.y + 3, 25, 12)
            pygame.draw.rect(surface, difficulty_color, badge_rect, border_radius=6)
            
            badge_text_rect = badge_surface.get_rect(center=badge_rect.center)
            surface.blit(badge_surface, badge_text_rect)
        
        # Draw serial number (like in the second screenshot)
        if hasattr(self.topic, 'sl_no'):
            id_font = pygame.font.Font(None, 10)
            id_surface = id_font.render(f"#{self.topic.sl_no}", True, (100, 100, 100))
            id_rect = id_surface.get_rect()
            id_rect.right = self.rect.right - 45
            id_rect.top = self.rect.top + 2
            surface.blit(id_surface, id_rect)
        
        # Draw action buttons: Solve (LeetCode), Solution (YouTube), Blog (Editorial)
        button_width = 50
        button_height = 18
        button_spacing = 55
        mouse_pos = pygame.mouse.get_pos()
        
        # Initialize button storage
        self.action_buttons = []
        
        # Starting position for buttons (right side)
        start_x = self.rect.right - 170
        button_y = self.rect.centery - button_height // 2
        
        # Button configurations: (text, link, color)
        buttons = [
            ("Solve", self.topic.lc_link, (255, 100, 50)),      # Orange for LeetCode
            ("Solution", self.topic.yt_link, (255, 50, 50)),    # Red for YouTube  
            ("Blog", self.topic.post_link, (50, 150, 255))      # Blue for Blog (post_link)
        ]
        
        current_x = start_x
        button_font = pygame.font.Font(None, 12)
        
        for button_text, button_link, button_color in buttons:
            if button_link:  # Only show button if link exists
                button_rect = pygame.Rect(current_x, button_y, button_width, button_height)
                
                # Hover effect
                is_hovered = button_rect.collidepoint(mouse_pos)
                display_color = tuple(min(255, c + 20) for c in button_color) if is_hovered else button_color
                
                # Draw button
                pygame.draw.rect(surface, display_color, button_rect, border_radius=3)
                pygame.draw.rect(surface, (255, 255, 255), button_rect, 1, border_radius=3)
                
                # Draw button text
                text_surface = button_font.render(button_text, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=button_rect.center)
                surface.blit(text_surface, text_rect)
                
                # Store button for click handling
                self.action_buttons.append((button_text.lower(), button_rect, button_link))
                
                current_x += button_spacing
        
        # Draw resource availability indicators
        indicator_font = pygame.font.Font(None, 10)
        indicator_x = self.rect.right - 15
        indicator_y = self.rect.top + 2
        
        # Show small icons for available resources
        available_resources = []
        if self.topic.lc_link: available_resources.append("🔗")      # LeetCode
        if self.topic.yt_link: available_resources.append("📺")      # YouTube  
        if self.topic.editorial_link: available_resources.append("📖") # Editorial
        if self.topic.post_link: available_resources.append("📝")    # Tutorial
        if self.topic.plus_link: available_resources.append("🚀")    # Practice
        
        for i, icon in enumerate(available_resources):
            icon_surface = indicator_font.render(icon, True, (200, 200, 200))
            surface.blit(icon_surface, (indicator_x - (i * 12), indicator_y))
        
        # Draw company tags indicator if available  
        if hasattr(self.topic, 'company_tags') and self.topic.company_tags:
            company_font = pygame.font.Font(None, 11)
            company_surface = company_font.render("🏢", True, (255, 200, 150))
            company_rect = company_surface.get_rect()
            company_rect.right = self.rect.right - 10
            company_rect.bottom = self.rect.bottom - 2
            surface.blit(company_surface, company_rect)
    
    def _draw_tooltip_only(self, surface: pygame.Surface):
        """Draw only the tooltip (on top layer)"""
        if not self.visible or not (self.show_tooltip and self.state == ComponentState.HOVER):
            return
        
        self._draw_tooltip(surface)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        if not self.visible or not self.enabled:
            return False
        
        mouse_pos = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEMOTION:
            if self.contains_point(mouse_pos):
                self.state = ComponentState.HOVER
            else:
                self.state = ComponentState.NORMAL
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Check if clicking on action buttons first (Solve, Solution, Blog)
                if hasattr(self, 'action_buttons') and self.action_buttons:
                    for button_type, button_rect, button_link in self.action_buttons:
                        if button_rect.collidepoint(mouse_pos):
                            self._open_link(button_link)
                            print(f"🔗 Opening {button_type}: {button_link}")
                            return True
                
                # Check if clicking on tooltip buttons (if tooltip is visible)
                if self.show_tooltip and self.state == ComponentState.HOVER and self.tooltip_buttons:
                    for button_type, button_rect, link in self.tooltip_buttons:
                        if button_rect.collidepoint(mouse_pos):
                            self._open_link(link)
                            return True
                
                # Regular topic click handling (but not if clicking on buttons area)
                if self.contains_point(mouse_pos):
                    # Don't toggle status if clicking in the button area
                    button_area_x = self.rect.right - 180  # Area where buttons are (expanded)
                    if mouse_pos[0] < button_area_x:
                        # Toggle topic status
                        if self.topic.status == QuestStatus.COMPLETED:
                            self.topic.status = QuestStatus.AVAILABLE
                        elif self.topic.status == QuestStatus.IN_PROGRESS:
                            self.topic.status = QuestStatus.COMPLETED
                        else:
                            self.topic.status = QuestStatus.IN_PROGRESS
                        
                        if self.callback:
                            self.callback(self.topic)
                        return True
        
        return False
    
    def _open_link(self, url: str):
        """Open link in browser"""
        try:
            import webbrowser
            webbrowser.open(url)
            print(f"🔗 Opening: {url}")
        except Exception as e:
            print(f"❌ Error opening link: {e}")
    
    def _calculate_topic_tags_height(self, tooltip_width: int) -> int:
        """Calculate height needed for topic tags"""
        if not (hasattr(self.topic, 'ques_topic') and self.topic.ques_topic):
            return 0
            
        try:
            topic_data = json.loads(self.topic.ques_topic)
            
            tag_font = pygame.font.Font(None, 12)
            current_width = 16  # Starting margin
            lines = 1
            
            for topic_item in topic_data:
                if isinstance(topic_item, dict) and 'label' in topic_item:
                    label = topic_item['label']
                    text_surface = tag_font.render(label, True, (255, 255, 255))
                    box_width = text_surface.get_width() + 12
                    
                    # Check if this box would exceed line width
                    if current_width + box_width > tooltip_width - 16:
                        lines += 1
                        current_width = 16 + box_width + 8
                    else:
                        current_width += box_width + 8
            
            # Each line is about 22 pixels high
            return lines * 22 + 10  # Extra padding
            
        except (json.JSONDecodeError, AttributeError):
            return 0
    
    def _draw_tooltip(self, surface: pygame.Surface):
        """Draw detailed tooltip with clickable links"""
        tooltip_width = 320
        
        # Calculate dynamic height for topic tags
        topic_tags_height = self._calculate_topic_tags_height(tooltip_width)
        tooltip_height = 180 + topic_tags_height
        
        # Position tooltip near mouse but keep it on screen
        mouse_pos = pygame.mouse.get_pos()
        tooltip_x = mouse_pos[0] + 10
        tooltip_y = mouse_pos[1] - tooltip_height - 10
        
        # Keep tooltip on screen
        if tooltip_x + tooltip_width > surface.get_width():
            tooltip_x = mouse_pos[0] - tooltip_width - 10
        if tooltip_y < 0:
            tooltip_y = mouse_pos[1] + 20
        
        tooltip_rect = pygame.Rect(tooltip_x, tooltip_y, tooltip_width, tooltip_height)
        
        # Draw tooltip background with border
        pygame.draw.rect(surface, (25, 25, 35), tooltip_rect, border_radius=8)
        pygame.draw.rect(surface, (0, 150, 255), tooltip_rect, 2, border_radius=8)
        
        # Clear previous tooltip buttons
        self.tooltip_buttons = []
        
        # Draw tooltip content
        y_offset = tooltip_y + 8
        font = pygame.font.Font(None, 16)
        small_font = pygame.font.Font(None, 14)
        button_font = pygame.font.Font(None, 13)
        
        # Topic title with solve button
        title_text = self.topic.question_title
        if len(title_text) > 30:
            title_text = title_text[:27] + "..."
        title_surface = font.render(title_text, True, (255, 255, 100))
        surface.blit(title_surface, (tooltip_x + 8, y_offset))
        
        # Solve button (like in the second image) - Only if LeetCode link exists
        if self.topic.lc_link:
            solve_button_rect = pygame.Rect(tooltip_x + tooltip_width - 60, y_offset - 2, 50, 18)
            pygame.draw.rect(surface, (255, 100, 50), solve_button_rect, border_radius=4)
            solve_text = button_font.render("Solve", True, (255, 255, 255))
            solve_text_rect = solve_text.get_rect(center=solve_button_rect.center)
            surface.blit(solve_text, solve_text_rect)
            
            # Add solve button to clickable areas
            self.tooltip_buttons.append(('solve', solve_button_rect, self.topic.lc_link))
        
        y_offset += 25
        
        # Draw topic tags as colored boxes (like in the image)
        if hasattr(self.topic, 'ques_topic') and self.topic.ques_topic:
            try:
                topic_data = json.loads(self.topic.ques_topic)
                
                # Colors for topic boxes (matching the image colors)
                tag_colors = [
                    (255, 100, 50),   # Orange
                    (255, 50, 50),    # Red  
                    (50, 150, 255),   # Blue
                    (255, 200, 100),  # Beige/Yellow
                    (255, 100, 255),  # Purple
                    (100, 255, 100),  # Green
                    (255, 150, 50),   # Orange variant
                    (150, 100, 255),  # Purple variant
                ]
                
                tag_x = tooltip_x + 8
                tag_y = y_offset
                tag_font = pygame.font.Font(None, 12)
                
                for i, topic_item in enumerate(topic_data):
                    if isinstance(topic_item, dict) and 'label' in topic_item:
                        label = topic_item['label']
                        color = tag_colors[i % len(tag_colors)]
                        
                        # Measure text to size the box
                        text_surface = tag_font.render(label, True, (255, 255, 255))
                        text_width = text_surface.get_width()
                        
                        # Box dimensions
                        box_width = text_width + 12
                        box_height = 18
                        
                        # Check if box fits on current line
                        if tag_x + box_width > tooltip_x + tooltip_width - 8:
                            tag_x = tooltip_x + 8  # New line
                            tag_y += 22
                        
                        # Draw colored box
                        box_rect = pygame.Rect(tag_x, tag_y, box_width, box_height)
                        pygame.draw.rect(surface, color, box_rect, border_radius=9)
                        
                        # Draw text in box
                        text_rect = text_surface.get_rect(center=box_rect.center)
                        surface.blit(text_surface, text_rect)
                        
                        tag_x += box_width + 8  # Spacing between boxes
                
                y_offset = tag_y + 25  # Move down after tags
                
            except (json.JSONDecodeError, AttributeError):
                pass  # Skip if parsing fails
        
        # Topic details
        details = [
            f"ID: {self.topic.id}",
            f"Step: {self.topic.step_no}.{self.topic.sub_step_no}.{self.topic.sl_no}",
            f"Difficulty: {['Easy', 'Medium', 'Hard'][self.topic.difficulty] if 0 <= self.topic.difficulty < 3 else 'Unknown'}",
            f"Status: {self.topic.status.value.replace('_', ' ').title()}"
        ]
        
        for detail in details:
            if y_offset + 15 < tooltip_y + tooltip_height - 35:  # Leave space for buttons
                detail_surface = small_font.render(detail, True, (200, 200, 200))
                surface.blit(detail_surface, (tooltip_x + 8, y_offset))
                y_offset += 15
        
        # Clickable resource buttons
        y_offset = tooltip_y + tooltip_height - 30
        button_width = 45
        button_height = 22
        button_spacing = 50
        x_offset = tooltip_x + 8
        
        # Create clickable resource buttons (matching main button scheme)
        resources = [
            ('🔗', 'Solve', self.topic.lc_link, (255, 100, 50)),      # LeetCode - Orange
            ('📺', 'Solution', self.topic.yt_link, (255, 50, 50)),    # YouTube - Red
            ('📖', 'Blog', self.topic.post_link, (50, 150, 255)),      # Blog (post_link) - Blue
            ('📝', 'Tutorial', self.topic.editorial_link, (255, 200, 100)), # Editorial - Yellow
            ('🚀', 'Striver', self.topic.plus_link, (255, 100, 255))   # Striver - Purple
        ]
        
        for icon, label, link, color in resources:
            if link and x_offset + button_width < tooltip_x + tooltip_width - 5:
                button_rect = pygame.Rect(x_offset, y_offset, button_width, button_height)
                
                # Check if mouse is hovering over this button
                mouse_in_button = button_rect.collidepoint(mouse_pos)
                button_color = color if not mouse_in_button else tuple(min(255, c + 30) for c in color)
                
                # Draw button
                pygame.draw.rect(surface, button_color, button_rect, border_radius=4)
                pygame.draw.rect(surface, (255, 255, 255), button_rect, 1, border_radius=4)
                
                # Draw icon and label
                button_text = f"{icon}"
                text_surface = button_font.render(button_text, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(button_rect.centerx, button_rect.centery - 2))
                surface.blit(text_surface, text_rect)
                
                # Label below button
                label_surface = pygame.font.Font(None, 10).render(label, True, (180, 180, 180))
                label_rect = label_surface.get_rect(center=(button_rect.centerx, button_rect.bottom + 8))
                surface.blit(label_surface, label_rect)
                
                # Add to clickable areas
                self.tooltip_buttons.append((label.lower(), button_rect, link))
                
                x_offset += button_spacing


class StepCard(UIComponent):
    """Card component for displaying step information"""
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 step: Step, callback: Optional[Callable[[Step], None]] = None,
                 style: Optional[ComponentStyle] = None):
        super().__init__(x, y, width, height, style)
        self.step = step
        self.callback = callback
        self._title_font = None  # Lazy initialization
        self._body_font = None  # Lazy initialization
    
    def draw(self, surface: pygame.Surface):
        if not self.visible:
            return
        
        # Draw card background
        bg_color = self.style.hover_color if self.state == ComponentState.HOVER else self.style.bg_color
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=10)
        pygame.draw.rect(surface, self.style.border_color, self.rect, self.style.border_width, border_radius=10)
        
        # Draw step title with text wrapping
        if self._title_font is None:
            self._title_font = pygame.font.Font(None, self.style.font_size + 2)  # Smaller font
        
        # Create shorter title to prevent overlap
        title_text = f"Step {self.step.step_no}: {self.step.step_title}"
        max_width = self.rect.width - 2 * self.style.padding
        
        # Wrap text if too long
        if self._title_font.size(title_text)[0] > max_width:
            # Try shorter version
            short_title = f"Step {self.step.step_no}:"
            second_line = self.step.step_title
            
            # Draw first line
            title_surface = self._title_font.render(short_title, True, self.style.text_color)
            title_rect = title_surface.get_rect()
            title_rect.x = self.rect.x + self.style.padding
            title_rect.y = self.rect.y + self.style.padding
            surface.blit(title_surface, title_rect)
            
            # Draw second line (truncated if still too long)
            if self._title_font.size(second_line)[0] > max_width:
                # Truncate with ellipsis
                while self._title_font.size(second_line + "...")[0] > max_width and len(second_line) > 10:
                    second_line = second_line[:-1]
                second_line += "..."
            
            second_surface = self._title_font.render(second_line, True, self.style.text_color)
            second_rect = second_surface.get_rect()
            second_rect.x = self.rect.x + self.style.padding
            second_rect.y = title_rect.bottom + 2
            surface.blit(second_surface, second_rect)
            
            # Update title_rect for subsequent positioning
            title_rect.height = second_rect.bottom - title_rect.y
        else:
            # Single line title
            title_surface = self._title_font.render(title_text, True, self.style.text_color)
            title_rect = title_surface.get_rect()
            title_rect.x = self.rect.x + self.style.padding
            title_rect.y = self.rect.y + self.style.padding
            surface.blit(title_surface, title_rect)
        
        # Draw progress information
        progress_text = f"Progress: {self.step.completed_topics}/{self.step.total_topics} topics"
        if self._body_font is None:
            self._body_font = pygame.font.Font(None, self.style.font_size)
        progress_surface = self._body_font.render(progress_text, True, self.style.text_color)
        progress_rect = progress_surface.get_rect()
        progress_rect.x = self.rect.x + self.style.padding
        progress_rect.y = title_rect.bottom + self.style.margin
        surface.blit(progress_surface, progress_rect)
        
        # Draw mini progress bar
        progress_bar_rect = pygame.Rect(
            self.rect.x + self.style.padding,
            progress_rect.bottom + self.style.margin,
            self.rect.width - 2 * self.style.padding,
            8
        )
        
        pygame.draw.rect(surface, (50, 50, 50), progress_bar_rect)
        
        # Fill progress
        if self.step.total_topics > 0:
            progress_ratio = self.step.completed_topics / self.step.total_topics
            fill_width = int(progress_bar_rect.width * progress_ratio)
            fill_rect = pygame.Rect(progress_bar_rect.x, progress_bar_rect.y, fill_width, progress_bar_rect.height)
            
            if progress_ratio >= 1.0:
                fill_color = self.style.success_color
            elif progress_ratio >= 0.5:
                fill_color = self.style.accent_color
            else:
                fill_color = self.style.warning_color
            
            pygame.draw.rect(surface, fill_color, fill_rect)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        if not self.visible or not self.enabled:
            return False
        
        mouse_pos = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEMOTION:
            if self.contains_point(mouse_pos):
                self.state = ComponentState.HOVER
            else:
                self.state = ComponentState.NORMAL
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.contains_point(mouse_pos):
                if self.callback:
                    self.callback(self.step)
                return True
        
        return False


class PlayerStatsPanel(UIComponent):
    """Panel for displaying player statistics"""
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 player_stats: PlayerStats, style: Optional[ComponentStyle] = None):
        super().__init__(x, y, width, height, style)
        self.player_stats = player_stats
        self._title_font = None  # Lazy initialization
        self._body_font = None  # Lazy initialization
    
    def draw(self, surface: pygame.Surface):
        if not self.visible:
            return
        
        # Draw panel background
        pygame.draw.rect(surface, self.style.bg_color, self.rect, border_radius=10)
        pygame.draw.rect(surface, self.style.border_color, self.rect, self.style.border_width, border_radius=10)
        
        y_offset = self.rect.y + self.style.padding
        
        # Draw rank
        if self._title_font is None:
            self._title_font = pygame.font.Font(None, self.style.font_size + 6)
        rank_surface = self._title_font.render(f"Rank: {self.player_stats.rank}", True, self.style.accent_color)
        surface.blit(rank_surface, (self.rect.x + self.style.padding, y_offset))
        y_offset += rank_surface.get_height() + self.style.margin
        
        # Draw level
        if self._body_font is None:
            self._body_font = pygame.font.Font(None, self.style.font_size)
        level_surface = self._body_font.render(f"Level: {self.player_stats.level}", True, self.style.text_color)
        surface.blit(level_surface, (self.rect.x + self.style.padding, y_offset))
        y_offset += level_surface.get_height() + self.style.margin
        
        # Draw experience bar
        exp_text = f"EXP: {self.player_stats.experience}/{self.player_stats.level * 100}"
        exp_surface = self._body_font.render(exp_text, True, self.style.text_color)
        surface.blit(exp_surface, (self.rect.x + self.style.padding, y_offset))
        y_offset += exp_surface.get_height() + self.style.margin
        
        # Experience progress bar
        exp_bar_rect = pygame.Rect(
            self.rect.x + self.style.padding,
            y_offset,
            self.rect.width - 2 * self.style.padding,
            10
        )
        pygame.draw.rect(surface, (50, 50, 50), exp_bar_rect)
        
        max_exp = self.player_stats.level * 100
        if max_exp > 0:
            exp_ratio = self.player_stats.experience / max_exp
            fill_width = int(exp_bar_rect.width * exp_ratio)
            fill_rect = pygame.Rect(exp_bar_rect.x, exp_bar_rect.y, fill_width, exp_bar_rect.height)
            pygame.draw.rect(surface, self.style.accent_color, fill_rect)
        
        y_offset += exp_bar_rect.height + self.style.margin * 2
        
        # Draw other stats
        stats_text = [
            f"Completed: {self.player_stats.total_completed}",
            f"Streak: {self.player_stats.streak}"
        ]
        
        for text in stats_text:
            text_surface = self._body_font.render(text, True, self.style.text_color)
            surface.blit(text_surface, (self.rect.x + self.style.padding, y_offset))
            y_offset += text_surface.get_height() + self.style.margin
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        return False  # Stats panel doesn't handle events


