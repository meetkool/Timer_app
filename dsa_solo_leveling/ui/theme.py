"""
Theme and styling configuration for DSA Solo Leveling

Solo Leveling-inspired color schemes and visual effects
"""

import pygame
from typing import Tuple, Dict, List
from dataclasses import dataclass


@dataclass
class ColorScheme:
    """Color scheme for the solo leveling theme"""
    # Primary colors (dark theme base)
    primary_bg: Tuple[int, int, int] = (15, 15, 25)
    secondary_bg: Tuple[int, int, int] = (25, 25, 35)
    tertiary_bg: Tuple[int, int, int] = (35, 35, 45)
    
    # Text colors
    primary_text: Tuple[int, int, int] = (220, 220, 220)
    secondary_text: Tuple[int, int, int] = (180, 180, 180)
    accent_text: Tuple[int, int, int] = (100, 200, 255)
    
    # Status colors
    success: Tuple[int, int, int] = (0, 220, 120)
    warning: Tuple[int, int, int] = (255, 180, 0)
    danger: Tuple[int, int, int] = (255, 80, 80)
    info: Tuple[int, int, int] = (100, 150, 255)
    
    # Interactive elements
    button_normal: Tuple[int, int, int] = (40, 40, 55)
    button_hover: Tuple[int, int, int] = (60, 60, 75)
    button_pressed: Tuple[int, int, int] = (80, 80, 95)
    
    # Borders and accents
    border_normal: Tuple[int, int, int] = (80, 80, 100)
    border_accent: Tuple[int, int, int] = (120, 180, 255)
    border_active: Tuple[int, int, int] = (150, 200, 255)
    
    # Special effects
    glow_color: Tuple[int, int, int] = (0, 150, 255)
    shadow_color: Tuple[int, int, int] = (0, 0, 0)


class SoloLevelingTheme:
    """Main theme class with solo leveling aesthetics"""
    
    def __init__(self):
        self.colors = ColorScheme()
        self._fonts = None  # Lazy initialization
        self.rank_colors = self._setup_rank_colors()
    
    @property
    def fonts(self):
        """Lazy initialization of fonts"""
        if self._fonts is None:
            self._fonts = self._setup_fonts()
        return self._fonts
    
    def _setup_fonts(self) -> Dict[str, pygame.font.Font]:
        """Setup font hierarchy"""
        fonts = {}
        
        # Try to load custom fonts, fall back to system fonts
        try:
            fonts['title'] = pygame.font.Font(None, 36)
            fonts['subtitle'] = pygame.font.Font(None, 28)
            fonts['body'] = pygame.font.Font(None, 20)
            fonts['small'] = pygame.font.Font(None, 16)
            fonts['large'] = pygame.font.Font(None, 48)
        except:
            # Fallback to system fonts
            fonts['title'] = pygame.font.Font(None, 36)
            fonts['subtitle'] = pygame.font.Font(None, 28)
            fonts['body'] = pygame.font.Font(None, 20)
            fonts['small'] = pygame.font.Font(None, 16)
            fonts['large'] = pygame.font.Font(None, 48)
        
        return fonts
    
    def _setup_rank_colors(self) -> Dict[str, Tuple[int, int, int]]:
        """Setup colors for different hunter ranks"""
        return {
            'S-Rank Hunter': (255, 215, 0),    # Gold
            'A-Rank Hunter': (255, 100, 100),  # Red
            'B-Rank Hunter': (100, 255, 100),  # Green
            'C-Rank Hunter': (100, 150, 255),  # Blue
            'D-Rank Hunter': (200, 200, 200),  # Silver
            'E-Rank Hunter': (139, 69, 19),    # Brown
        }
    
    def get_rank_color(self, rank: str) -> Tuple[int, int, int]:
        """Get color for a specific rank"""
        return self.rank_colors.get(rank, self.colors.primary_text)
    
    def draw_glow_effect(self, surface: pygame.Surface, rect: pygame.Rect, 
                        color: Tuple[int, int, int], intensity: int = 10):
        """Draw a glow effect around a rectangle"""
        for i in range(intensity):
            alpha = max(0, 255 - (i * 25))
            glow_color = (*color, alpha)
            
            # Create a surface with per-pixel alpha
            glow_surface = pygame.Surface((rect.width + i * 2, rect.height + i * 2), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, glow_color, glow_surface.get_rect(), 2)
            
            # Blit the glow surface
            glow_rect = glow_surface.get_rect(center=rect.center)
            surface.blit(glow_surface, glow_rect)
    
    def draw_gradient_rect(self, surface: pygame.Surface, rect: pygame.Rect,
                          start_color: Tuple[int, int, int], end_color: Tuple[int, int, int],
                          vertical: bool = True):
        """Draw a gradient-filled rectangle"""
        if vertical:
            for y in range(rect.height):
                ratio = y / rect.height
                color = [
                    int(start_color[i] + (end_color[i] - start_color[i]) * ratio)
                    for i in range(3)
                ]
                pygame.draw.line(surface, color, 
                               (rect.x, rect.y + y), (rect.right, rect.y + y))
        else:
            for x in range(rect.width):
                ratio = x / rect.width
                color = [
                    int(start_color[i] + (end_color[i] - start_color[i]) * ratio)
                    for i in range(3)
                ]
                pygame.draw.line(surface, color,
                               (rect.x + x, rect.y), (rect.x + x, rect.bottom))
    
    def draw_animated_border(self, surface: pygame.Surface, rect: pygame.Rect,
                           color: Tuple[int, int, int], width: int = 2, 
                           animation_offset: float = 0):
        """Draw an animated border effect"""
        import math
        
        # Create border segments with animated alpha
        segments = 8
        segment_length = (rect.width * 2 + rect.height * 2) // segments
        
        for i in range(segments):
            alpha_multiplier = (math.sin(animation_offset + i * 0.5) + 1) / 2
            segment_color = (
                int(color[0] * alpha_multiplier),
                int(color[1] * alpha_multiplier),
                int(color[2] * alpha_multiplier)
            )
            
            # Calculate segment position (simplified version)
            if i < 2:  # Top edge
                start_x = rect.x + i * segment_length
                pygame.draw.line(surface, segment_color,
                               (start_x, rect.y), 
                               (min(start_x + segment_length, rect.right), rect.y), width)
    
    def draw_tech_grid(self, surface: pygame.Surface, rect: pygame.Rect,
                      grid_size: int = 50, alpha: int = 30):
        """Draw a technological grid background"""
        grid_color = (*self.colors.border_normal, alpha)
        
        # Create grid surface with alpha
        grid_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        
        # Draw vertical lines
        for x in range(0, rect.width, grid_size):
            pygame.draw.line(grid_surface, grid_color,
                           (x, 0), (x, rect.height))
        
        # Draw horizontal lines
        for y in range(0, rect.height, grid_size):
            pygame.draw.line(grid_surface, grid_color,
                           (0, y), (rect.width, y))
        
        surface.blit(grid_surface, rect.topleft)
    
    def create_progress_bar_gradient(self, width: int, height: int,
                                   progress: float) -> pygame.Surface:
        """Create a gradient progress bar surface"""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Background
        pygame.draw.rect(surface, self.colors.tertiary_bg, surface.get_rect())
        
        # Progress fill with gradient
        if progress > 0:
            fill_width = int(width * progress)
            fill_rect = pygame.Rect(0, 0, fill_width, height)
            
            # Choose colors based on progress
            if progress >= 1.0:
                start_color = self.colors.success
                end_color = (0, 255, 0)
            elif progress >= 0.7:
                start_color = self.colors.info
                end_color = self.colors.success
            elif progress >= 0.3:
                start_color = self.colors.warning
                end_color = self.colors.info
            else:
                start_color = self.colors.danger
                end_color = self.colors.warning
            
            self.draw_gradient_rect(surface, fill_rect, start_color, end_color, False)
        
        # Border
        pygame.draw.rect(surface, self.colors.border_normal, surface.get_rect(), 2)
        
        return surface


# Global theme instance (lazy initialization)
_theme_instance = None

def get_theme() -> SoloLevelingTheme:
    """Get the global theme instance"""
    global _theme_instance
    if _theme_instance is None:
        _theme_instance = SoloLevelingTheme()
    return _theme_instance

# Create theme instance when accessed
theme = get_theme