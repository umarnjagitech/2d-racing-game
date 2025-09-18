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

class Direction(Enum):
    LEFT = -1
    RIGHT = 1

class Car:
    # Represents the player's car in the game.
    
    def __init__(self, x: float, y: float):
        # Initialize the car with default position and properties
        # Position and movement
        self.x = x  # Starting x position (left side of screen)
        self.y = y  # Starting y position (middle of screen)
        self.target_y = y  # Target y position for lane changes
        self.lane = 2  # Current lane (1-4)
        self.lane_width = 80  # Width of each lane in pixels
        self.lane_change_speed = 0.1  # Speed of lane changes (lower = smoother)
        
        # Track following
        self.distance_along_track = 0  # Start at the beginning of the track
        self.look_ahead = 150  # How far ahead to look for steering (pixels)
        
        # Lane changing state
        self.is_changing_lanes = False
        self.lane_change_direction = None
        
        # Car properties
        self.speed = 0
        self.max_speed = 8  # Maximum speed
        self.min_speed = 0.5  # Reduced minimum speed for better control
        self.acceleration = 0.1  # Base acceleration rate
        self.braking = 0.15  # Braking/deceleration rate
        self.friction = 0.98  # Increased friction for more controlled stopping
        self.rotation = 0  # Start facing right (0 degrees)
        self.max_rotation = 30  # Maximum rotation when turning
        self.rotation_speed = 0.08  # How fast the car rotates (lower = smoother)
        
        # Car dimensions
        self.width = 60
        self.height = 100
        
        # Create a simple car surface
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self._create_car_surface()
        
        # Store the original surface for rotation
        self.original_surface = self.surface.copy()
        
        # Debug info
        self.debug_info = {
            'speed': 0,
            'distance': 0,
            'rotation': 0
        }
    
    def _create_car_surface(self):
        # Create a more detailed car sprite
        # Car body
        car_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Car body (sportier shape)
        pygame.draw.ellipse(car_surface, (255, 0, 0), (5, 10, self.width-10, self.height-20))  # Main body
        
        # Windows
        pygame.draw.ellipse(car_surface, (150, 200, 255, 200), 
                          (15, 15, self.width-30, 30))  # Windshield
        
        # Details
        pygame.draw.line(car_surface, (0, 0, 0), (10, 30), (self.width-10, 30), 2)  # Window line
        pygame.draw.line(car_surface, (100, 100, 100), (self.width//2, 25), (self.width//2, self.height-15), 2)  # Middle line
        
        # Wheels
        pygame.draw.ellipse(car_surface, (20, 20, 20), (5, self.height-25, 20, 15))  # Back wheel
        pygame.draw.ellipse(car_surface, (20, 20, 20), (self.width-25, self.height-25, 20, 15))  # Front wheel
        
        # Headlights
        pygame.draw.circle(car_surface, (255, 255, 150), (15, 15), 5)  # Left headlight
        pygame.draw.circle(car_surface, (255, 255, 150), (self.width-15, 15), 5)  # Right headlight
        
        self.original_surface = car_surface
        self.surface = car_surface
    
    def change_lane(self, direction: Direction):
        """Initiate a lane change in the specified direction."""
        if self.is_changing_lanes:
            return
            
        new_lane = self.lane + direction.value
        if 1 <= new_lane <= 4:  # Assuming 4 lanes
            self.lane = new_lane
            self.is_changing_lanes = True
            self.lane_change_direction = direction
    
    def update(self, throttle: float, steering: float, dt: float, track=None):
        # Store previous state for recovery if needed
        prev_distance = self.distance_along_track
        prev_lane = self.lane
        
        try:
            # Handle throttle input
            if abs(throttle) > 0.1:
                # Update car speed based on throttle (positive for accelerate, negative for brake)
                if throttle > 0:
                    self.speed += throttle * self.acceleration * dt * 60
                else:
                    # Apply stronger braking when slowing down
                    self.speed += throttle * self.braking * dt * 60 * 2
            
            # Apply friction and limit speed
            self.speed = max(self.min_speed, min(self.speed, self.max_speed))
            
            # If no throttle input, apply gradual deceleration
            if abs(throttle) < 0.1 and self.speed > self.min_speed:
                self.speed *= 0.99  # Gentle deceleration
            
            # Handle steering for lane changes (only when not already changing lanes)
            if not self.is_changing_lanes and abs(steering) > 0.1:
                direction = Direction.LEFT if steering < 0 else Direction.RIGHT
                new_lane = self.lane + direction.value
                if 1 <= new_lane <= 4:  # Check if new lane is valid
                    self.change_lane(direction)
            
            # Update car's position along the track
            if track and hasattr(track, 'get_path_point'):
                # Move forward along the track at a constant rate
                self.distance_along_track += self.speed * dt * 60
                
                # Get current track point
                current_point = track.get_path_point(self.distance_along_track)
                
                # Calculate lookahead distance based on speed (further lookahead at higher speeds)
                look_ahead = max(10, abs(self.speed) * 2)
                next_point = track.get_path_point((self.distance_along_track + look_ahead) % track.track_length)
                
                # Calculate direction vector
                dx = next_point[0] - current_point[0]
                dy = next_point[1] - current_point[1]
                
                # Calculate target rotation based on direction of travel
                target_angle = math.degrees(math.atan2(dy, dx))
                
                # Smoothly interpolate rotation
                angle_diff = (target_angle - self.rotation + 180) % 360 - 180
                self.rotation += angle_diff * self.rotation_speed * dt * 5
                
                # Calculate target y position based on lane
                lane_offset = (self.lane - 2.5) * self.lane_width
                target_y = current_point[1] + lane_offset
                
                # Smoothly move to target y position
                y_diff = target_y - self.y
                if abs(y_diff) > 1.0:  # Only update if we need to move
                    # Scale movement speed based on distance to target (easing)
                    move_speed = min(1.0, abs(y_diff) / (self.lane_width * 0.5))
                    self.y += y_diff * move_speed * 0.2  # Reduced from 0.3 to 0.2 for smoother movement
                    self.rotation = y_diff * 0.1  # Simple rotation based on y difference
                else:
                    self.y = target_y
                    self.rotation = 0
                    self.is_changing_lanes = False
                
                # Update x position to follow the track exactly
                self.x = current_point[0]
                
                # Update debug info
                self.debug_info = {
                    'speed': round(self.speed, 2),
                    'distance': round(self.distance_along_track, 2),
                    'rotation': round(self.rotation, 2),
                    'position': (round(self.x, 2), round(self.y, 2)),
                    'lane': self.lane,
                    'target_y': round(target_y, 2)
                }
                
        except Exception as e:
            # If any error occurs, revert to previous state
            print(f"Error updating car position: {e}")
            self.distance_along_track = prev_distance
            self.lane = prev_lane
        
        # Fallback for when there's no track (shouldn't normally happen)
        if not track or not hasattr(track, 'get_path_point'):
            # Simple movement without track following (for testing)
            self.x += self.speed * dt * 60
            
            # Handle lane changes with simple movement
            if self.is_changing_lanes:
                target_y = (self.screen_height // 2) + (self.lane - 2.5) * self.lane_width
                y_diff = target_y - self.y
                
                if abs(y_diff) > 1.0:
                    # Move towards target y position
                    move_speed = min(1.0, abs(y_diff) / (self.lane_width * 0.5))
                    self.y += y_diff * move_speed * 0.2
                    self.rotation = y_diff * 0.1
                else:
                    self.y = target_y
                    self.rotation = 0
                    self.is_changing_lanes = False
        
        # Update car surface with rotation
        self._update_car_rotation()
        
    def _update_car_rotation(self):
        """Update the car's surface with the current rotation."""
        # Create a new surface to hold the rotated car
        rotated_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Rotate the original surface
        rotated = pygame.transform.rotate(self.original_surface, -self.rotation)
        
        # Get the rect of the rotated surface and center it
        rect = rotated.get_rect(center=(self.width//2, self.height//2))
        rotated_surface.blit(rotated, rect.topleft)
        
        # Update the car's surface
        self.surface = rotated_surface
    
    def render(self, screen: pygame.Surface, camera_x: float, camera_y: float):
        # Calculate screen position
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        # Update debug info
        self.debug_info['speed'] = self.speed
        self.debug_info['distance'] = self.distance_along_track
        self.debug_info['rotation'] = self.rotation
        
        # Get rotated car surface (negative rotation because Pygame's y-axis is inverted)
        rotated_car = pygame.transform.rotate(self.original_surface, -self.rotation)
        
        # Get new rect for the rotated car (centered)
        rotated_rect = rotated_car.get_rect(center=(screen_x, screen_y))
        
        # Draw the rotated car
        screen.blit(rotated_car, rotated_rect.topleft)
        
        # Draw debug info
        font = pygame.font.Font(None, 24)
        debug_text = [
            f"Speed: {self.speed:.1f}",
            f"Distance: {self.distance_along_track:.0f}",
            f"Rotation: {self.rotation:.1f}°",
            f"Position: ({self.x:.0f}, {self.y:.0f})",
            f"Lane: {self.lane}"
        ]
        
        for i, text in enumerate(debug_text):
            text_surface = font.render(text, True, (255, 255, 255))
            screen.blit(text_surface, (10, 10 + i * 25))
