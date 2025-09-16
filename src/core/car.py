# Car module containing the player's vehicle logic and rendering.
import math
import pygame
from ..utils.constants import *

class Car:
    # Represents the player's car in the game.
    
    def __init__(self, x: float = 100, y: float = 100):
        # Initialize the car with default position and properties
        # Position and movement
        self.x = x
        self.y = y
        self.angle = 0  # in radians
        self.speed = 0
        self.max_speed = 10
        self.acceleration = 0.2
        self.rotation_speed = 0.05
        self.friction = 0.95  # Friction coefficient (0-1)
        
        # Car dimensions
        self.width = 40
        self.height = 20
        
        # Create a simple car surface
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self._create_car_surface()
    
    def _create_car_surface(self):
        # Create the car's visual representation
        # Draw a simple rectangle for the car body
        pygame.draw.rect(self.surface, (255, 0, 0), (0, 0, self.width, self.height))
        # Add some details
        pygame.draw.rect(self.surface, (200, 200, 200), (5, 5, 10, 10))  # Window
        pygame.draw.rect(self.surface, (200, 200, 200), (25, 5, 10, 10))  # Window
    
    def update(self, throttle: float, steering: float, dt: float):
        # Update the car's position and rotation based on input
        # Args:
        #   throttle: Value between -1 (reverse) and 1 (forward)
        #   steering: Value between -1 (left) and 1 (right)
        #   dt: Delta time since last frame in seconds
        # Apply throttle
        if abs(throttle) > 0.1:  # Dead zone for keyboard input
            self.speed += throttle * self.acceleration * dt * 60
        
        # Apply friction
        self.speed *= self.friction
        
        # Limit speed
        self.speed = max(-self.max_speed/2, min(self.speed, self.max_speed))
        
        # Apply steering (only when moving)
        if abs(self.speed) > 0.5:
            # Reverse steering when going backwards
            steering_direction = -1 if self.speed < 0 else 1
            self.angle += steering * self.rotation_speed * steering_direction * dt * 60
        
        # Update position based on angle and speed
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed  # Negative because y increases downward
        
        # Keep angle between 0 and 2*PI
        self.angle = self.angle % (2 * math.pi)
    
    def render(self, screen: pygame.Surface, camera_x: float, camera_y: float):
        # Draw the car on the screen
        # Args:
        #   screen: The surface to draw the car on
        #   camera_x: Camera x offset
        #   camera_y: Camera y offset
        # Rotate the car surface
        rotated_car = pygame.transform.rotate(self.surface, -math.degrees(self.angle))
        
        # Get the rect of the rotated surface
        car_rect = rotated_car.get_rect(center=(self.x - camera_x, self.y - camera_y))
        
        # Draw the car
        screen.blit(rotated_car, car_rect.topleft)
