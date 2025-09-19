"""Integration tests for the top-down racing game."""
import unittest
import pygame
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.game import RacingGame
from src.core.car import Car

class TestGameIntegration(unittest.TestCase):
    """Integration tests for the racing game."""
    
    def setUp(self):
        """Set up test fixtures."""
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.game = RacingGame("Test Game", self.screen_width, self.screen_height)
        self.dt = 1/60  # 60 FPS
    
    def tearDown(self):
        """Clean up after tests."""
        self.game.cleanup(testing=True)
    
    def test_game_initialization(self):
        """Test that the game initializes correctly."""
        self.assertIsNotNone(self.game.screen)
        self.assertIsNotNone(self.game.clock)
        self.assertIsInstance(self.game.car, Car)
        self.assertIsNotNone(self.game.track)
        self.assertEqual(self.game.camera_y, 0)
    
    def test_game_update_with_input(self):
        """Test that the game updates correctly with user input."""
        initial_distance = self.game.car.distance_traveled
        
        # Simulate pressing the up arrow key
        keys = {pygame.K_UP: True, pygame.K_DOWN: False, pygame.K_LEFT: False, pygame.K_RIGHT: False, pygame.K_w: False, pygame.K_s: False, pygame.K_a: False, pygame.K_d: False}
        pygame.key.get_pressed = lambda: keys
        
        self.game.update(self.dt)
        
        self.assertGreater(self.game.car.distance_traveled, initial_distance)

    def test_camera_scrolling(self):
        """Test that the camera scrolls with the car's distance."""
        self.game.car.distance_traveled = 1000
        self.game.update(self.dt)
        self.assertEqual(self.game.camera_y, 1000)

if __name__ == '__main__':
    unittest.main()