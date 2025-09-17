# Heads-Up Display (HUD) for the racing game.
import pygame
import math

class HUD:
    # Manages the display of game information on screen.
    
    def __init__(self, screen):
        # Initialize the HUD with the game screen
        self.screen = screen
        
        # Try to load system fonts, fall back to default font if not available
        try:
            self.font = pygame.font.SysFont('Arial', 24)
            self.small_font = pygame.font.SysFont('Arial', 18)
        except Exception as e:
            print(f"Warning: Could not load system fonts: {e}")
            print("Falling back to default font.")
            # Use pygame's default font
            self.font = pygame.font.Font(None, 36)
            self.small_font = pygame.font.Font(None, 24)
        
        # Colors
        self.text_color = (255, 255, 255)  # White
        self.speed_color = (0, 255, 0)     # Green
        self.warning_color = (255, 0, 0)   # Red
        
    def render(self, lap_time, best_lap, lap_count, speed):
        # Render the HUD elements
        # Args:
        #   lap_time: Current lap time in seconds
        #   best_lap: Best lap time in seconds
        #   lap_count: Current lap number
        #   speed: Current speed of the car
        # Convert speed to km/h (assuming speed is in pixels/frame)
        speed_kmh = abs(speed) * 10
        
        # Format time strings
        lap_time_str = self._format_time(lap_time)
        best_lap_str = self._format_time(best_lap) if best_lap != float('inf') else "--:--.---"
        
        # Draw speedometer
        self._draw_speedometer(speed_kmh)
        
        # Draw lap info
        self._draw_text(f"Lap: {lap_count}", 10, 10)
        self._draw_text(f"Time: {lap_time_str}", 10, 40)
        self._draw_text(f"Best: {best_lap_str}", 10, 70)
        
        # Draw controls help (only show for first few seconds)
        self._draw_controls_help()
    
    def _draw_speedometer(self, speed):
        # Draw the speedometer on the screen
        # Draw speed number
        speed_text = f"{int(speed)} km/h"
        speed_surface = self.font.render(speed_text, True, self.speed_color)
        self.screen.blit(speed_surface, (self.screen.get_width() - 150, 10))
        
        # Draw speed bar
        bar_width = 150
        bar_height = 20
        bar_x = self.screen.get_width() - bar_width - 10
        bar_y = 50
        
        # Background
        pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        
        # Speed indicator (green to red)
        speed_ratio = min(speed / 200.0, 1.0)  # Cap at 200 km/h for display
        indicator_width = int(bar_width * speed_ratio)
        
        # Color gradient from green to red
        r = int(min(255, speed_ratio * 2 * 255))
        g = int(min(255, (1 - speed_ratio) * 2 * 255))
        
        pygame.draw.rect(self.screen, (r, g, 0), (bar_x, bar_y, indicator_width, bar_height))
        
        # Draw border
        pygame.draw.rect(self.screen, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height), 2)
    
    def _draw_text(self, text, x, y, color=None):
        # Helper method to draw text on the screen
        if color is None:
            color = self.text_color
            
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
    
    def _draw_controls_help(self):
        # Display the controls help text
        controls = [
            "Controls:",
            "↑/W - Accelerate",
            "↓/S - Brake/Reverse",
            "←→/AD - Steer",
            "ESC - Quit"
        ]
        
        y_pos = self.screen.get_height() - 120
        for i, line in enumerate(controls):
            color = (200, 200, 0) if i == 0 else (150, 150, 150)
            text_surface = self.small_font.render(line, True, color)
            self.screen.blit(text_surface, (10, y_pos + i * 20))
    
    @staticmethod
    def _format_time(seconds):
        # Format time in seconds to MM:SS.mmm format
        if seconds == float('inf'):
            return "--:--.---"
            
        minutes = int(seconds // 60)
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:06.3f}"
