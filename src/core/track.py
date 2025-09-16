# Track module for generating and rendering the racing track.
import pygame
import math
from ..utils.constants import *

class Track:
    # Represents the racing track in the game.
    
    def __init__(self):
        # Initialize the track with default parameters
        self.checkpoints = []
        self.boundaries = []
        self._generate_oval_track()
        
    def _generate_oval_track(self, width=800, height=600):
        # Generate a simple oval track
        # Outer boundary (rectangle for now)
        outer_width = width
        outer_height = height
        outer_rect = pygame.Rect(100, 100, outer_width, outer_height)
        
        # Inner boundary (smaller rectangle)
        inner_width = width // 2
        inner_height = height // 2
        inner_rect = pygame.Rect(
            100 + (width - inner_width) // 2,
            100 + (height - inner_height) // 2,
            inner_width,
            inner_height
        )
        
        # Store track boundaries as line segments
        self.boundaries = [
            # Outer rectangle (clockwise)
            [(100, 100), (100 + outer_width, 100)],
            [(100 + outer_width, 100), (100 + outer_width, 100 + outer_height)],
            [(100 + outer_width, 100 + outer_height), (100, 100 + outer_height)],
            [(100, 100 + outer_height), (100, 100)],
            # Inner rectangle (counter-clockwise)
            [inner_rect.topleft, (inner_rect.left, inner_rect.bottom)],
            [(inner_rect.left, inner_rect.bottom), inner_rect.bottomright],
            [inner_rect.bottomright, (inner_rect.right, inner_rect.top)],
            [(inner_rect.right, inner_rect.top), inner_rect.topleft],
        ]
        
        # Add checkpoints (corners of the track)
        self.checkpoints = [
            (100 + outer_width//2, 100),  # Top
            (100 + outer_width, 100 + outer_height//2),  # Right
            (100 + outer_width//2, 100 + outer_height),  # Bottom
            (100, 100 + outer_height//2),  # Left
        ]
    
    def render(self, screen, camera_x, camera_y):
        # Draw the track on the screen
        # Args:
        #   screen: The surface to draw the track on
        #   camera_x: Camera x offset
        #   camera_y: Camera y offset
        # Draw grass (background)
        screen.fill((34, 139, 34))  # Forest green
        
        # Draw track surface (dirt color)
        pygame.draw.rect(
            screen,
            (139, 69, 19),  # Brown
            (
                self.boundaries[0][0][0] - camera_x,
                self.boundaries[0][0][1] - camera_y,
                self.boundaries[1][0][0] - self.boundaries[0][0][0],
                self.boundaries[2][0][1] - self.boundaries[0][0][1]
            )
        )
        
        # Draw inner boundary (grass)
        inner_rect = pygame.Rect(
            self.boundaries[4][0][0] - camera_x,
            self.boundaries[4][0][1] - camera_y,
            self.boundaries[5][0][0] - self.boundaries[4][0][0],
            self.boundaries[6][0][1] - self.boundaries[4][0][1]
        )
        pygame.draw.rect(screen, (34, 139, 34), inner_rect)
        
        # Draw track boundaries (white lines)
        for boundary in self.boundaries:
            start = (boundary[0][0] - camera_x, boundary[0][1] - camera_y)
            end = (boundary[1][0] - camera_x, boundary[1][1] - camera_y)
            pygame.draw.line(screen, (255, 255, 255), start, end, 5)
        
        # Draw checkpoints (for debugging)
        for i, (x, y) in enumerate(self.checkpoints):
            pygame.draw.circle(
                screen,
                (0, 255, 0) if i == 0 else (255, 0, 0),
                (int(x - camera_x), int(y - camera_y)),
                10
            )
            
    def check_collision(self, car_rect):
        # Check if the car collides with track boundaries
        # Args:
        #   car_rect: Pygame Rect representing the car's hitbox
        # Returns:
        #   bool: True if collision detected, False otherwise
        # Simple AABB collision with track boundaries
        for boundary in self.boundaries:
            if self._line_rect_intersect(boundary, car_rect):
                return True
        return False
    
    def _line_rect_intersect(self, line, rect):
        # Check if a line segment intersects with a rectangle
        # Convert rect to lines
        rect_lines = [
            [(rect.left, rect.top), (rect.right, rect.top)],
            [(rect.right, rect.top), (rect.right, rect.bottom)],
            [(rect.right, rect.bottom), (rect.left, rect.bottom)],
            [(rect.left, rect.bottom), (rect.left, rect.top)]
        ]
        
        # Check for line-line intersection with each rect edge
        for rect_line in rect_lines:
            if self._line_intersect(line[0], line[1], rect_line[0], rect_line[1]):
                return True
        return False
    
    def _line_intersect(self, a1, a2, b1, b2):
        # Check if two line segments a1-a2 and b1-b2 intersect
        # Implementation of line segment intersection test
        # Using cross product method
        def ccw(A, B, C):
            return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])
        
        return ccw(a1, b1, b2) != ccw(a2, b1, b2) and ccw(a1, a2, b1) != ccw(a1, a2, b2)
