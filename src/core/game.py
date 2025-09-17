# Main game module containing the game loop and core game logic.
import os
import sys
import pygame
from typing import Tuple

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.utils.constants import *
from src.core.car import Car
from src.core.track import Track
from src.ui.hud import HUD

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
        self.track = Track(width, height, num_lanes=4)
        # Initialize car at the starting point of the track (left side, middle vertically)
        start_point = self.track.get_path_point(0)
        self.car = Car(100, height // 2)  # Start at x=100, middle of screen
        self.hud = HUD(self.screen)
        # Initialize camera to follow car
        self.camera_x = 0
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
        
        # Always allow steering, even when not moving
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            steering = -1.0  # Move up (since we're doing horizontal movement)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            steering = 1.0   # Move down
            
        # Throttle controls
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            throttle = 1.0  # Move forward (right)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            throttle = -0.5  # Move backward (left, slower)
        
        # Update car with track for path following
        self.car.update(throttle, steering, dt, self.track)
        
        # Update game state
        self.speed = self.car.speed
        self.distance = self.car.distance_along_track  # Use the car's distance along track
        
        # Always keep camera centered on car (smooth follow)
        target_camera_x = max(0, self.car.x - self.width * 0.3)  # Keep car at 30% from left
        self.camera_x += (target_camera_x - self.camera_x) * 0.1  # Smooth follow
        
        # Keep camera within track bounds
        self.camera_x = max(0, min(self.camera_x, self.track.track_length - self.width))
        
        # Center camera vertically (since we're doing horizontal scrolling)
        self.camera_y = 0
        
        # Update lap time
        self.lap_time += dt
    
    def _draw_background(self):
        """Draw the scrolling background based on current biome."""
        # The track class now handles biome-specific background drawing
        pass
    
    def render(self):
        # Clear the screen with sky blue background
        self.screen.fill((135, 206, 235))  # Sky blue background
        
        # Render track with camera offset for horizontal scrolling
        self.track.render(self.screen, self.camera_x, self.camera_y)
        
        # Draw car with camera offset
        self.car.render(self.screen, self.camera_x, self.camera_y)
        
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
        frame_count = 0
        
        print("Starting game loop...")
        
        while self.running:
            try:
                frame_count += 1
                
                # Calculate delta time
                current_time = pygame.time.get_ticks() / 1000.0
                dt = current_time - last_time
                last_time = current_time
                
                # Cap delta time to avoid spiral of death
                dt = min(dt, 0.1)
                
                if frame_count % 60 == 0:  # Log every second at 60 FPS
                    print(f"Frame {frame_count}: FPS={int(1/dt) if dt > 0 else 0}, "
                          f"Car pos=({self.car.x:.1f}, {self.car.y:.1f}), "
                          f"Speed={self.car.speed:.1f}, Lane={self.car.lane}")
                
                # Update game state
                self.handle_events()
                self.update(dt)
                self.render()
                
                # Cap the frame rate
                self.clock.tick(self.fps)
                
            except Exception as e:
                print(f"Error in game loop: {e}")
                import traceback
                traceback.print_exc()
                self.running = False
        
        print("Game loop ended. Cleaning up...")
        # Clean up
        self.cleanup()
    
    def cleanup(self):
        # Clean up resources
        pygame.quit()
        sys.exit()
