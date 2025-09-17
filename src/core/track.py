# Track module for generating and rendering the racing track.
import math
import pygame
import random
from enum import Enum
from typing import List, Tuple, Optional
from ..utils.constants import *

class BiomeType(Enum):
    FOREST = "forest"
    GRASSLAND = "grassland"
    DESERT = "desert"
    MOUNTAIN = "mountain"
    RAINFOREST = "rainforest"

class LaneMarking:
    def __init__(self, x: int, y: int, width: int = 2, height: int = 30):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 255, 255)  # White lane markings

class Track:
    """Represents the racing track in the side-scrolling game."""
    
    def __init__(self, screen_width: int, screen_height: int, num_lanes: int = 4):
        # Initialize track parameters
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.num_lanes = num_lanes
        self.lane_width = screen_width // (num_lanes + 2)  # Add some margin
        self.road_color = (50, 50, 50)  # Dark gray road
        self.shoulder_color = (100, 100, 100)  # Lighter gray for shoulders
        
        # Track elements
        self.lane_markings: List[LaneMarking] = []
        self.obstacles: List[pygame.Rect] = []
        self.biome_boundaries: List[Tuple[int, BiomeType]] = []
        
        # Track path points (for car following)
        self.path_points: List[Tuple[float, float]] = []
        self.track_length = 0
        
        # Initialize track elements
        self._generate_track_elements()
        self._generate_path()
    
    def _generate_track_elements(self):
        """Generate lane markings and obstacles for the track."""
        # Calculate lane positions
        self.start_x = (self.screen_width - (self.num_lanes * self.lane_width)) // 2
        
        # Generate lane markings (dashed lines between lanes)
        for i in range(1, self.num_lanes):
            x = self.start_x + (i * self.lane_width)
            # Create dashed lane markers (3 screens worth of markers)
            for y in range(-100, self.screen_height * 3, 60):
                self.lane_markings.append(LaneMarking(x, y, 2, 30))
        
        # Define biome boundaries (in pixels from start)
        biome_length = 2000  # pixels per biome
        self.biome_boundaries = [
            (0, BiomeType.GRASSLAND),
            (biome_length, BiomeType.FOREST),
            (biome_length * 2, BiomeType.MOUNTAIN),
            (biome_length * 3, BiomeType.DESERT),
            (biome_length * 4, BiomeType.RAINFOREST),
        ]
        self.track_length = biome_length * 5  # Total track length for all biomes
        
        # Generate random obstacles (for demonstration)
        for _ in range(20):
            lane = random.randint(0, self.num_lanes - 1)
            x = self.start_x + (lane * self.lane_width) + random.randint(10, self.lane_width - 30)
            y = random.randint(0, self.track_length)
            self.obstacles.append(pygame.Rect(x, y, 30, 30))
    
    def _generate_path(self):
        """Generate a smooth path for the car to follow."""
        # Create a wavy path for the track
        num_points = 100
        for i in range(num_points + 1):
            # Normalized position along track (0 to 1)
            t = i / num_points
            
            # Calculate x position with sine wave for curves
            # Amplitude decreases at higher positions to keep car on screen
            amplitude = self.lane_width * 1.5 * (1 - t * 0.3)
            x = self.screen_width // 2 + math.sin(t * 10) * amplitude
            
            # Calculate y position (progress along track)
            y = t * self.track_length
            
            self.path_points.append((x, y))
    
    def get_path_point(self, distance: float) -> Tuple[float, float]:
        """Get a point along the path at the given distance."""
        if not self.path_points:
            return (self.screen_width // 2, 0)
            
        # Wrap distance around track length
        distance = distance % self.track_length
        
        # Find the segment where this distance falls
        segment_length = self.track_length / (len(self.path_points) - 1)
        segment = int(distance / segment_length)
        segment = min(segment, len(self.path_points) - 2)  # Ensure we don't go out of bounds
        
        # Get the start and end points of the segment
        start_point = self.path_points[segment]
        end_point = self.path_points[segment + 1]
        
        # Calculate interpolation factor (0 to 1) within the segment
        segment_start_dist = segment * segment_length
        t = (distance - segment_start_dist) / segment_length
        
        # Linear interpolation between points
        x = start_point[0] + (end_point[0] - start_point[0]) * t
        y = start_point[1] + (end_point[1] - start_point[1]) * t
        
        return (x, y)
    
    def get_current_biome(self, camera_y: float) -> BiomeType:
        """Get the current biome based on camera position."""
        distance = camera_y % (len(BiomeType) * 2000)  # Loop through biomes
        
        # Find the current biome based on camera position
        current_biome = BiomeType.GRASSLAND  # Default
        for boundary, biome in sorted(self.biome_boundaries, key=lambda x: x[0]):
            if distance >= boundary:
                current_biome = biome
        return current_biome
    
    def get_biome_color(self, biome: BiomeType) -> Tuple[int, int, int]:
        """Get the background color for a biome."""
        return {
            BiomeType.FOREST: (34, 139, 34),     # Forest green
            BiomeType.GRASSLAND: (124, 252, 0),  # Lawn green
            BiomeType.DESERT: (255, 211, 155),   # Desert sand
            BiomeType.MOUNTAIN: (169, 169, 169), # Dark gray
            BiomeType.RAINFOREST: (0, 100, 0)    # Dark green
        }.get(biome, (50, 150, 50))  # Default to green
    
    def render(self, screen: pygame.Surface, camera_x: float, camera_y: float):
        """Render the track with the current camera position."""
        # Get current biome and set background color
        current_biome = self.get_current_biome(camera_y)
        screen.fill(self.get_biome_color(current_biome))
        
        # Draw the road surface
        road_width = self.num_lanes * self.lane_width
        road_left = (self.screen_width - road_width) // 2
        
        # Draw the road
        pygame.draw.rect(screen, self.road_color, 
                        (road_left, 0, road_width, self.screen_height))
        
        # Draw shoulders
        shoulder_width = (self.screen_width - road_width) // 2
        pygame.draw.rect(screen, self.shoulder_color, 
                        (0, 0, shoulder_width, self.screen_height))  # Left shoulder
        pygame.draw.rect(screen, self.shoulder_color, 
                        (self.screen_width - shoulder_width, 0, 
                         shoulder_width, self.screen_height))  # Right shoulder
        
        # Draw lane markings (dashed lines between lanes)
        for i in range(1, self.num_lanes):
            x = road_left + (i * self.lane_width)
            # Draw dashed lane markers for visible area
            for y in range(-60, self.screen_height + 60, 60):
                pygame.draw.rect(screen, (255, 255, 255), 
                              (x - 1, y, 2, 30))
        
        # Draw obstacles
        for obstacle in self.obstacles:
            # Only draw obstacles that are visible on screen
            obstacle_screen_y = obstacle.y - camera_y
            if -obstacle.height <= obstacle_screen_y <= self.screen_height:
                pygame.draw.rect(screen, (200, 50, 50), 
                              (obstacle.x, obstacle_screen_y, 
                               obstacle.width, obstacle.height))
        
        # Draw biome name (for debugging)
        font = pygame.font.Font(None, 36)
        biome_text = f"{current_biome.value.upper()}"
        text_surface = font.render(biome_text, True, (255, 255, 255))
        screen.blit(text_surface, (self.screen_width - 150, 20))
            
    def check_collision(self, car_rect):
        # Check if the car collides with track boundaries
        # Args:
        #   car_rect: Pygame Rect representing the car's hitbox
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
