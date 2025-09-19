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
    """Main game class for the top-down racing game."""
    
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
        self.car = Car(width // 2, height * 0.8)  # Start at bottom-center
        self.hud = HUD(self.screen)
        self.camera_y = 0
        
        # Game metrics
        self.lap_time = 0
        self.best_lap = float('inf')
        self.lap_count = 0
        
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
        
        throttle = 0.0
        steering = 0.0
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            throttle = 1.0
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            throttle = -1.0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            steering = -1.0
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            steering = 1.0
        
        # Update car
        self.car.update(throttle, steering, dt, self.track)
        
        # Update camera to follow car's progress
        self.camera_y = self.car.distance_traveled
        
        # Update lap time
        self.lap_time += dt
    
    def render(self):
        # Render track with camera offset
        self.track.render(self.screen, 0, self.camera_y)
        
        # Draw car
        self.car.render(self.screen)
        
        # Draw HUD
        self.hud.render(
            self.lap_time, 
            self.best_lap, 
            self.lap_count, 
            self.car.speed * 10
        )
        
        # Update the display
        pygame.display.flip()
    
    def run(self):
        # Run the main game loop
        self.running = True
        last_time = pygame.time.get_ticks() / 1000.0
        
        while self.running:
            try:
                current_time = pygame.time.get_ticks() / 1000.0
                dt = current_time - last_time
                last_time = current_time
                dt = min(dt, 0.1)
                
                self.handle_events()
                self.update(dt)
                self.render()
                
                self.clock.tick(self.fps)
                
            except Exception as e:
                print(f"Error in game loop: {e}")
                import traceback
                traceback.print_exc()
                self.running = False
        
        self.cleanup()
    
    def cleanup(self, testing=False):
        # Clean up resources
        pygame.quit()
        if not testing:
            sys.exit()