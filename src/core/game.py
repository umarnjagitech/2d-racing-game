"""
Main game module containing the game loop and core game logic.
"""
import pygame
import sys
from typing import Tuple
from ..utils.constants import *
from .car import Car
from .track import Track
from ..ui.hud import HUD

class RacingGame:
    """Main game class that handles initialization, game loop, and cleanup."""
    
    def __init__(self, title: str, width: int, height: int):
        """Initialize the game window and resources."""
        pygame.init()
        pygame.display.set_caption(title)
        
        # Set up the display
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = False
        self.fps = 60
        
        # Game state
        self.car = Car()
        self.track = Track()
        self.hud = HUD(self.screen)
        
        # Camera settings
        self.camera_x = 0
        self.camera_y = 0
        
        # Game metrics
        self.lap_time = 0
        self.best_lap = float('inf')
        self.lap_count = 0
        
    def handle_events(self):
        """Process all events in the event queue."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self, dt: float):
        """Update game state."""
        # Get keyboard input
        keys = pygame.key.get_pressed()
        
        # Handle car controls
        throttle = 0
        steering = 0
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            throttle = 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            throttle = -1
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            steering = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            steering = 1
            
        # Update car
        self.car.update(throttle, steering, dt)
        
        # Update camera to follow car
        self.camera_x = self.car.x - self.screen.get_width() // 2
        self.camera_y = self.car.y - self.screen.get_height() // 2
        
        # Update lap time
        self.lap_time += dt
    
    def render(self):
        """Render the game state."""
        # Clear the screen
        self.screen.fill((50, 150, 50))  # Green background for now
        
        # Draw track
        self.track.render(self.screen, self.camera_x, self.camera_y)
        
        # Draw car
        self.car.render(self.screen, self.camera_x, self.camera_y)
        
        # Draw HUD
        self.hud.render(self.lap_time, self.best_lap, self.lap_count, self.car.speed)
        
        # Update the display
        pygame.display.flip()
    
    def run(self):
        """Run the main game loop."""
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
        """Clean up resources."""
        pygame.quit()
        sys.exit()
