# Car module for the racing game.
import os
import sys
import math
import pygame
from enum import Enum
from typing import Tuple, Optional

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.utils.constants import *

class Car:
    """Represents the player's car in the top-down racing game."""
    
    def __init__(self, x: float, y: float):
        # Initialize the car with default position and properties
        self.x = x
        self.y = y
        self.speed = 0
        self.max_speed = 15
        self.acceleration = 0.2
        self.braking = 0.4
        self.friction = 0.98
        self.rotation = 0
        self.rotation_speed = 3
        
        # Car dimensions
        self.width = 40
        self.height = 80
        
        # Create a simple car surface
        self.original_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self._create_car_surface()
        self.surface = self.original_surface
        
        # Distance traveled
        self.distance_traveled = 0

    def _create_car_surface(self):
        # Create a more detailed car sprite (top-down view)
        car_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Car body (red)
        pygame.draw.rect(car_surface, (200, 0, 0), (0, 5, self.width, self.height - 10), border_radius=10)
        
        # Windshield (light blue)
        pygame.draw.rect(car_surface, (150, 200, 255), (5, 10, self.width - 10, 25), border_radius=5)
        
        # Roof (darker red)
        pygame.draw.rect(car_surface, (150, 0, 0), (5, 35, self.width - 10, 30), border_radius=5)
        
        # Headlights (yellow)
        pygame.draw.circle(car_surface, (255, 255, 0), (10, 10), 5)
        pygame.draw.circle(car_surface, (255, 255, 0), (self.width - 10, 10), 5)
        
        self.original_surface = car_surface

    def update(self, throttle: float, steering: float, dt: float, track):
        # Handle throttle and braking
        if throttle > 0:
            self.speed += self.acceleration * throttle
        elif throttle < 0:
            self.speed += self.braking * throttle
        
        # Apply friction
        self.speed *= self.friction
        self.speed = max(0, min(self.speed, self.max_speed))
        
        # Handle steering
        if self.speed > 0.1:
            self.rotation += steering * self.rotation_speed * (self.speed / self.max_speed)
            self.rotation = max(-45, min(45, self.rotation))
        else:
            self.rotation *= 0.9 # Straighten out when stopped

        # Update position
        angle_rad = math.radians(self.rotation)
        self.x += self.speed * math.sin(angle_rad) * dt * 60
        self.distance_traveled += self.speed * math.cos(angle_rad) * dt * 60

        # Keep car within road bounds
        road_left = (track.screen_width - track.road_width) // 2
        road_right = road_left + track.road_width
        self.x = max(road_left + self.width / 2, min(self.x, road_right - self.width / 2))

        # Update car surface with rotation
        self._update_car_rotation()

    def _update_car_rotation(self):
        """Update the car's surface with the current rotation."""
        self.surface = pygame.transform.rotate(self.original_surface, -self.rotation)
    
    def render(self, screen: pygame.Surface):
        # Get new rect for the rotated car (centered)
        rotated_rect = self.surface.get_rect(center=(self.x, self.y))
        
        # Draw the rotated car
        screen.blit(self.surface, rotated_rect.topleft)
        
        # Draw debug info
        font = pygame.font.Font(None, 24)
        debug_text = [
            f"Speed: {self.speed:.1f}",
            f"Distance: {self.distance_traveled:.0f}",
            f"Rotation: {self.rotation:.1f}°",
            f"Position: ({self.x:.0f}, {self.y:.0f})"
        ]
        
        for i, text in enumerate(debug_text):
            text_surface = font.render(text, True, (255, 255, 255))
            screen.blit(text_surface, (10, 10 + i * 25))