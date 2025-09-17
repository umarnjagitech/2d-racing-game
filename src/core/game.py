# Main game module containing the game loop and core game logic.
import pygame
import sys
from typing import Tuple
from ..utils.constants import *
from .car import Car
from .track import Track
from ..ui.hud import HUD

class RacingGame:
    # Main game class that handles initialization, game loop, and cleanup.
    
    def __init__(self, title: str, width: int, height: int):
        # Initialize the game window and resources
        pygame.init()
        pygame.display.set_caption(title)
        
        # Set up the display
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = False
        self.fps = 60
        self.width = width
        self.height = height
        
        # Game state
        self.car = Car(width // 2, height)
        self.track = Track(width, height, num_lanes=4)
        self.hud = HUD(self.screen)
        
        # Camera settings (for scrolling background)
        self.camera_y = 0
        
        # Game metrics
        self.lap_time = 0
        self.best_lap = float('inf')
        self.lap_count = 0
        self.distance = 0
        self.speed = 0
        
    def handle_events(self):
        # Process all events in the event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self, dt: float):
        # Get keyboard input
        keys = pygame.key.get_pressed()
        
        # Handle car controls - car won't move until player presses up/down
        throttle = 0.0  # Start with no throttle
        steering = 0.0
        
        # Only allow steering when moving forward/backward
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            throttle = 1.0  # Move forward
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                steering = -1.0  # Turn left
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                steering = 1.0   # Turn right
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            throttle = -0.5  # Move backward (slower than forward)
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                steering = 1.0   # Reverse steering when going backward
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                steering = -1.0  # Reverse steering when going backward
            
        # Update car with track for path following
        self.car.update(throttle, steering, dt, self.track)
        
        # Update game state
        self.speed = self.car.speed
        self.distance += self.speed * dt * 10  # Scale factor for better distance tracking
        
        # Update camera to follow car's y-position (with some smoothing)
        target_camera_y = self.car.y - self.height * 0.7  # Keep car in upper part of screen
        self.camera_y += (target_camera_y - self.camera_y) * 0.1  # Smooth camera follow
        
        # Ensure camera doesn't go above track start
        self.camera_y = max(0, self.camera_y)
        
        # Update lap time
        self.lap_time += dt
    
    def _draw_background(self):
        """Draw the scrolling background based on current biome."""
        # The track class now handles biome-specific background drawing
        pass
    
    def render(self):
        # Clear the screen
        self.screen.fill((0, 0, 0))
        
        # Render track with camera offset for scrolling
        self.track.render(self.screen, 0, self.camera_y)
        
        # Draw car (centered at the bottom of the screen)
        self.car.render(self.screen, 0, 0)
        
        # Draw HUD
        self.hud.render(
            self.lap_time, 
            self.best_lap, 
            self.lap_count, 
            abs(self.speed) * 10  # Use absolute value of speed for display
        )
        
        # Update the display
        pygame.display.flip()
    
    def run(self):
        # Run the main game loop
        self.running = True
        last_time = pygame.time.get_ticks() / 1000.0
        
        while self.running:
            # Calculate delta time
            current_time = pygame.time.get_ticks() / 1000.0
            dt = current_time - last_time
            last_time = current_time
            
            # Cap delta time to avoid spiral of death
            dt = min(dt, 0.1)
            
            # Update game state
            self.handle_events()
            self.update(dt)
            self.render()
            
            # Cap the frame rate
            self.clock.tick(self.fps)
        
        # Clean up
        self.cleanup()
    
    def cleanup(self):
        # Clean up resources
        pygame.quit()
        sys.exit()
