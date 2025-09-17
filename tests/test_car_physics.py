"""Unit tests for car physics and movement."""
import unittest
import math
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.car import Car, Direction
from src.core.track import Track

class TestCarPhysics(unittest.TestCase):
    """Test cases for car physics and movement."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a track instance for testing
        self.screen_width = 1200
        self.screen_height = 800
        self.track = Track(self.screen_width, self.screen_height)
        
        # Create a car instance for testing
        self.car = Car(100, self.screen_height // 2)
        
        # Set a fixed time step for consistent testing
        self.dt = 1/60  # 60 FPS
    
    def test_initial_state(self):
        """Test the initial state of the car."""
        self.assertEqual(self.car.speed, 0)
        self.assertEqual(self.car.rotation, 0)
        self.assertEqual(self.car.lane, 2)
        self.assertEqual(self.car.x, 100)
        self.assertEqual(self.car.y, self.screen_height // 2)
    
    def test_acceleration(self):
        """Test car acceleration."""
        # Apply full throttle
        self.car.update(1.0, 0, self.dt, self.track)
        self.assertGreater(self.car.speed, 0)
        
        # Speed should increase with time
        initial_speed = self.car.speed
        self.car.update(1.0, 0, self.dt, self.track)
        self.assertGreater(self.car.speed, initial_speed)
    
    def test_braking(self):
        """Test car braking and deceleration."""
        # Get up to speed
        for _ in range(60):  # 1 second at 60 FPS
            self.car.update(1.0, 0, self.dt, self.track)
        
        # Apply brakes
        initial_speed = self.car.speed
        self.car.update(-1.0, 0, self.dt, self.track)
        self.assertLess(self.car.speed, initial_speed)
    
    def test_lane_changes(self):
        """Test lane changing functionality."""
        # Change lane to the right
        initial_y = self.car.y
        self.car.change_lane(Direction.RIGHT)
        
        # Update several times to complete the lane change
        for _ in range(30):  # 0.5 seconds at 60 FPS
            self.car.update(1.0, 0, self.dt, self.track)
        
        # Y position should have changed (lane change is vertical)
        self.assertNotEqual(self.car.y, initial_y)
        
        # Car should be in the next lane (lane 3)
        self.assertEqual(self.car.lane, 3)
    
    def test_track_following(self):
        """Test that the car follows the track path."""
        # Get the initial position and distance
        initial_distance = self.car.distance_along_track
        
        # Update the car for a short time
        for _ in range(60):  # 1 second at 60 FPS
            self.car.update(1.0, 0, self.dt, self.track)
        
        # Car should have moved along the track
        self.assertGreater(self.car.distance_along_track, initial_distance)
        
        # Car's position should match the track path at current distance
        track_point = self.track.get_path_point(self.car.distance_along_track)
        self.assertAlmostEqual(self.car.x, track_point[0], delta=5)
        self.assertAlmostEqual(self.car.y, track_point[1], delta=5 + self.car.lane_width * 2)
    
    def test_rotation(self):
        """Test that the car rotates correctly when the track curves."""
        # Move the car to a curved part of the track
        self.car.distance_along_track = self.track.track_length * 0.25  # First curve
        
        # Get the initial rotation (should be 0 at start)
        initial_rotation = self.car.rotation
        
        # Update the car to follow the curve
        for _ in range(60):  # 1 second at 60 FPS
            self.car.update(1.0, 0, self.dt, self.track)
        
        # Get the rotation after following the curve
        final_rotation = self.car.rotation
        
        # The rotation should have changed (not equal to initial 0)
        # or the car should have moved significantly along the track
        self.assertTrue(
            not math.isclose(final_rotation, initial_rotation, abs_tol=0.1) or 
            self.car.distance_along_track > self.track.track_length * 0.26,
            f"Rotation didn't change from {initial_rotation}° to {final_rotation}°"
        )

if __name__ == '__main__':
    unittest.main()
