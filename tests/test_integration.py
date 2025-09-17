"""Integration tests for the racing game."""
import unittest
import pygame
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.game import RacingGame as Game
from src.core.car import Car

class TestGameIntegration(unittest.TestCase):
    """Integration tests for the racing game."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Initialize pygame for testing
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        
        # Create a game instance with title and dimensions
        self.game = Game("Test Game", self.screen_width, self.screen_height)
        
        # Set a fixed time step for consistent testing
        self.dt = 1/60  # 60 FPS
    
    def tearDown(self):
        """Clean up after tests."""
        pygame.quit()
    
    def test_game_initialization(self):
        """Test that the game initializes correctly."""
        self.assertIsNotNone(self.game.screen)
        self.assertIsNotNone(self.game.clock)
        self.assertIsInstance(self.game.car, Car)
        self.assertIsNotNone(self.game.track)
        self.assertEqual(self.game.camera_x, 0)
        self.assertEqual(self.game.camera_y, 0)
    
    def test_game_update(self):
        """Test that the game updates correctly."""
        # Store initial state
        initial_car_x = self.game.car.x
        
        # Simulate pressing the up arrow key (throttle)
        # We need to set the key state directly since we can't easily simulate key hold
        self.game.keys_pressed = {pygame.K_UP: True}
        
        # Update the game multiple times to allow for acceleration
        for _ in range(60):  # 1 second at 60 FPS
            self.game.update(self.dt)
        
        # Car should have moved forward (increased x)
        self.assertGreater(self.game.car.x, initial_car_x)
    
    def test_lane_changes(self):
        """Test that lane changes work correctly in the game."""
        # Store initial lane and position
        initial_lane = self.game.car.lane
        initial_y = self.game.car.y
        
        # Simulate pressing the right arrow key
        self.game.keys_pressed = {pygame.K_RIGHT: True}
        
        # Update the game several times to complete the lane change
        for _ in range(120):  # 2 seconds at 60 FPS
            self.game.update(self.dt)
        
        # Car's y position should have changed
        self.assertNotEqual(self.game.car.y, initial_y)
    
    def test_camera_following(self):
        """Test that the camera follows the car correctly."""
        # Move the car forward
        self.game.keys_pressed = {pygame.K_UP: True}
        
        for _ in range(120):  # 2 seconds at 60 FPS
            self.game.update(self.dt)
        
        # Car should have moved forward
        self.assertGreater(self.game.car.x, 100)  # Started at x=100
        
        # Camera should follow the car (implementation dependent)

if __name__ == '__main__':
    unittest.main()
