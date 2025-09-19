"""Unit tests for car physics and movement in the top-down racing game."""
import unittest
import math
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.car import Car
from src.core.track import Track

class TestCarPhysics(unittest.TestCase):
    """Test cases for car physics and movement."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.screen_width = 1200
        self.screen_height = 800
        self.track = Track(self.screen_width, self.screen_height)
        self.car = Car(self.screen_width // 2, self.screen_height * 0.8)
        self.dt = 1/60  # 60 FPS
    
    def test_initial_state(self):
        """Test the initial state of the car."""
        self.assertEqual(self.car.speed, 0)
        self.assertEqual(self.car.rotation, 0)
        self.assertEqual(self.car.x, self.screen_width // 2)
        self.assertEqual(self.car.y, self.screen_height * 0.8)
    
    def test_acceleration(self):
        """Test car acceleration."""
        self.car.update(1.0, 0, self.dt, self.track)
        self.assertGreater(self.car.speed, 0)
        initial_speed = self.car.speed
        self.car.update(1.0, 0, self.dt, self.track)
        self.assertGreater(self.car.speed, initial_speed)
    
    def test_braking(self):
        """Test car braking."""
        self.car.speed = 10
        self.car.update(-1.0, 0, self.dt, self.track)
        self.assertLess(self.car.speed, 10)

    def test_steering(self):
        """Test car steering."""
        self.car.speed = 10
        self.car.update(0, -1.0, self.dt, self.track) # Steer left
        self.assertLess(self.car.rotation, 0)
        initial_x = self.car.x
        self.car.update(0, 0, self.dt, self.track)
        self.assertLess(self.car.x, initial_x)

    def test_road_boundaries(self):
        """Test that the car stays within the road boundaries."""
        self.car.x = 10 # Far left
        self.car.update(0, 0, self.dt, self.track)
        road_left = (self.track.screen_width - self.track.road_width) // 2
        self.assertGreaterEqual(self.car.x, road_left)

        self.car.x = self.screen_width - 10 # Far right
        self.car.update(0, 0, self.dt, self.track)
        road_right = road_left + self.track.road_width
        self.assertLessEqual(self.car.x, road_right)

if __name__ == '__main__':
    unittest.main()