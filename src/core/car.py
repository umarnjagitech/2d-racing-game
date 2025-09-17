# Car module containing the player's vehicle logic and rendering.
import math
import pygame
from enum import Enum
from typing import Tuple, Optional
from ..utils.constants import *

class Direction(Enum):
    LEFT = -1
    RIGHT = 1

class Car:
    # Represents the player's car in the game.
    
    def __init__(self, x: float, screen_height: int):
        # Initialize the car with default position and properties
        # Position and movement
        self.x = x  # Current x position
        self.y = screen_height - 100  # Fixed y position (bottom of screen)
        self.target_x = x  # Target x position for smooth movement
        self.lane = 2  # Current lane (1-4)
        self.lane_width = 120  # Width of each lane in pixels
        self.lane_change_speed = 0.1  # Speed of lane changes (lower = smoother)
        
        # Track following
        self.distance_along_track = 0  # Current distance along the track
        self.look_ahead = 100  # How far ahead to look for steering (pixels)
        
        # Lane changing state
        self.is_changing_lanes = False
        self.lane_change_direction = None
        
        # Car properties
        self.speed = 0
        self.max_speed = 5
        self.acceleration = 0.05
        self.friction = 0.98  # Friction coefficient (0-1)
        self.rotation = 0  # Current rotation in degrees
        self.max_rotation = 25  # Maximum rotation when turning
        self.rotation_speed = 0.1  # How fast the car rotates (lower = smoother)
        
        # Car dimensions
        self.width = 60
        self.height = 100
        
        # Create a simple car surface
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self._create_car_surface()
        
        # Track following
        self.path_points = []  # Will store points along the track
        self.current_path_index = 0
        self.look_ahead_distance = 150  # How far ahead to look for steering
        self.turn_smoothing = 0.1  # Lower = smoother turns
    
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
            # Calculate target x position based on lane number and screen width
            lane_width = self.lane_width
            screen_center = self.surface.get_width() // 2
            self.target_x = screen_center + (self.lane - 2.5) * lane_width
            self.is_changing_lanes = True
            self.lane_change_direction = direction
    
    def update(self, throttle: float, steering: float, dt: float, track=None):
        # Only move if there's throttle input
        if abs(throttle) < 0.1:
            self.speed = 0
        else:
            # Update car speed based on throttle (forward/backward)
            self.speed += throttle * self.acceleration * dt * 60
            
            # Apply friction
            self.speed *= self.friction
            
            # Limit speed
            self.speed = max(-self.max_speed/2, min(self.speed, self.max_speed))
        
        # Handle lane changes only when moving
        if abs(self.speed) > 0.1 and abs(steering) > 0.1 and not self.is_changing_lanes:
            direction = Direction.LEFT if steering < 0 else Direction.RIGHT
            self.change_lane(direction)
        
        # Update car's position along the track
        if track and hasattr(track, 'get_path_point'):
            # Store previous position in case we need to revert
            prev_distance = self.distance_along_track
            prev_lane = self.lane
            
            # Only move if there's speed
            if abs(self.speed) > 0.1:
                # Move car forward/backward along the track
                self.distance_along_track += self.speed * dt * 100
            
            # Get current and next path points for direction
            current_point = track.get_path_point(self.distance_along_track)
            look_ahead = max(10, abs(self.speed) * 2)
            next_point = track.get_path_point(self.distance_along_track + look_ahead)
            
            # Calculate direction vector
            dx = next_point[0] - current_point[0]
            dy = next_point[1] - current_point[1]
            
            # Calculate target rotation (in degrees)
            target_angle = math.degrees(math.atan2(-dx, dy))
            
            # Smoothly interpolate to target rotation
            angle_diff = (target_angle - self.rotation + 180) % 360 - 180
            self.rotation += angle_diff * self.rotation_speed * dt * 5
            
            # Calculate lane offset based on current rotation
            lane_offset = (self.lane - 2.5) * self.lane_width
            
            # Calculate new position
            new_x = current_point[0] + math.sin(math.radians(self.rotation)) * lane_offset
            new_y = current_point[1] - math.cos(math.radians(self.rotation)) * lane_offset
            
            # Check if new position is within track bounds
            road_left = (track.screen_width - track.num_lanes * track.lane_width) // 2
            road_right = road_left + track.num_lanes * track.lane_width
            
            if road_left <= new_x <= road_right:
                self.x = new_x
                self.y = new_y
            else:
                # Revert to previous position if out of bounds
                self.distance_along_track = prev_distance
                self.lane = prev_lane
        else:
            # Fallback to lane-based movement if no track
            if abs(steering) > 0.1 and not self.is_changing_lanes:
                direction = Direction.LEFT if steering < 0 else Direction.RIGHT
                self.change_lane(direction)
            
            # Move towards target x position (for lane changes)
            if abs(self.x - self.target_x) > 0.5:
                self.x += (self.target_x - self.x) * self.lane_change_speed
                
                # Calculate rotation based on movement direction and speed
                rotation_target = ((self.target_x - self.x) / self.lane_width) * self.max_rotation
                self.rotation += (rotation_target - self.rotation) * self.rotation_speed * dt * 60
            else:
                # Gradually return to straight when not turning
                self.rotation *= 0.95
        
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
        # Draw the car on the screen with proper centering and rotation
        # Calculate screen position based on camera
        screen_x = self.x - self.width // 2 - camera_x
        screen_y = self.y - self.height // 2 - camera_y
        
        # Get rotated car surface
        rotated_car = pygame.transform.rotate(self.surface, self.rotation)
        # Get new rect for the rotated car
        rotated_rect = rotated_car.get_rect(center=(self.x - camera_x, self.y - camera_y))
        
        # Draw the rotated car
        screen.blit(rotated_car, rotated_rect.topleft)
