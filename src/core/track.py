# Track module for generating and rendering the racing track.
import os
import sys
import math
import pygame
import random
from enum import Enum
from typing import List, Tuple, Optional

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.utils.constants import *

class BiomeType(Enum):
    FOREST = "forest"
    GRASSLAND = "grassland"
    DESERT = "desert"
    MOUNTAIN = "mountain"
    RAINFOREST = "rainforest"

class LaneMarking:
    def __init__(self, x: int, y: int, width: int = 5, height: int = 40):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 255, 255)  # White lane markings

class Track:
    """Represents the racing track in the top-down game."""
    
    def __init__(self, screen_width: int, screen_height: int, num_lanes: int = 4):
        # Initialize track parameters
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.num_lanes = num_lanes
        self.lane_width = 60  # Fixed lane width
        self.road_width = self.num_lanes * self.lane_width
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
        self._generate_path()
        self._generate_track_elements()
    
    def _generate_track_elements(self):
        """Generate lane markings and obstacles for the track."""
        # Generate vertical lane markings
        for i in range(1, self.num_lanes):
            x = (self.screen_width - self.road_width) // 2 + (i * self.lane_width)
            # Create dashed lane markers
            for y in range(0, self.track_length, 100):
                self.lane_markings.append(LaneMarking(x - 2, y, 4, 40))
        
        # Define biome boundaries (in pixels from start)
        biome_length = 3000  # pixels per biome
        self.biome_boundaries = [
            (0, BiomeType.GRASSLAND),
            (biome_length, BiomeType.FOREST),
            (biome_length * 2, BiomeType.MOUNTAIN),
            (biome_length * 3, BiomeType.DESERT),
            (biome_length * 4, BiomeType.RAINFOREST),
        ]
        
        # Generate random obstacles
        for _ in range(50):
            lane = random.randint(0, self.num_lanes - 1)
            x = (self.screen_width - self.road_width) // 2 + (lane * self.lane_width) + random.randint(10, self.lane_width - 40)
            y = random.randint(500, self.track_length - 500)
            self.obstacles.append(pygame.Rect(x, y, 30, 30))
    
    def _generate_path(self):
        """Generate a smooth vertical path for the car to follow."""
        self.path_points = []
        num_points = 1000
        self.track_length = self.screen_height * 10  # 10 screens long
        
        sections = [
            (0.0, 0.2, 150, 0.5, False),
            (0.2, 0.4, 250, 1.0, False),
            (0.4, 0.6, 80, 2.0, False),
            (0.6, 0.7, 0, 0, True),
            (0.7, 0.9, 350, 0.3, False),
            (0.9, 1.0, 0, 0, True)
        ]
        
        for i in range(num_points + 1):
            y = (i / num_points) * self.track_length
            t = i / num_points
            
            x = self.screen_width / 2
            
            for start_t, end_t, amplitude, frequency, is_straight in sections:
                if start_t <= t < end_t and not is_straight:
                    section_t = (t - start_t) / (end_t - start_t)
                    x_offset = math.sin(section_t * frequency * math.pi * 2) * amplitude
                    x = self.screen_width / 2 + x_offset
                    break
            
            padding = self.road_width / 2
            x = max(padding, min(x, self.screen_width - padding))
            
            self.path_points.append((x, y))
    
    def get_path_point(self, distance: float) -> Tuple[float, float]:
        """Get a point along the path at the given distance."""
        if not self.path_points:
            return (self.screen_width // 2, 0)
            
        distance = distance % self.track_length
        
        segment_length = self.track_length / (len(self.path_points) - 1)
        segment = int(distance / segment_length)
        segment = min(segment, len(self.path_points) - 2)
        
        start_point = self.path_points[segment]
        end_point = self.path_points[segment + 1]
        
        segment_start_dist = segment * segment_length
        t = (distance - segment_start_dist) / segment_length
        
        x = start_point[0] + (end_point[0] - start_point[0]) * t
        y = start_point[1] + (end_point[1] - start_point[1]) * t
        
        return (x, y)
    
    def get_current_biome(self, camera_y: float) -> BiomeType:
        """Get the current biome based on camera position."""
        distance = camera_y % self.track_length
        
        current_biome = BiomeType.GRASSLAND
        for boundary, biome in sorted(self.biome_boundaries, key=lambda x: x[0]):
            if distance >= boundary:
                current_biome = biome
        return current_biome
    
    def get_biome_color(self, biome: BiomeType) -> Tuple[int, int, int]:
        """Get the background color for a biome."""
        return {
            BiomeType.FOREST: (34, 139, 34),
            BiomeType.GRASSLAND: (124, 252, 0),
            BiomeType.DESERT: (255, 211, 155),
            BiomeType.MOUNTAIN: (169, 169, 169),
            BiomeType.RAINFOREST: (0, 100, 0)
        }.get(biome, (50, 150, 50))
    
    def render(self, screen: pygame.Surface, camera_x: float, camera_y: float):
        """Render the track with the current camera position."""
        current_biome = self.get_current_biome(camera_y)
        screen.fill(self.get_biome_color(current_biome))
        
        road_left = (self.screen_width - self.road_width) // 2
        
        # Draw the road
        pygame.draw.rect(screen, self.road_color, 
                        (road_left, 0, self.road_width, self.screen_height))
        
        # Draw shoulders
        shoulder_width = road_left
        pygame.draw.rect(screen, self.shoulder_color, 
                        (0, 0, shoulder_width, self.screen_height))
        pygame.draw.rect(screen, self.shoulder_color, 
                        (self.screen_width - shoulder_width, 0, 
                         shoulder_width, self.screen_height))
        
        # Draw lane markings
        for i in range(1, self.num_lanes):
            x = road_left + (i * self.lane_width)
            for y_offset in range(-100, self.screen_height + 100, 100):
                y = y_offset - (camera_y % 100)
                pygame.draw.rect(screen, (255, 255, 255), 
                              (x - 2, y, 4, 40))
        
        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle_screen_y = obstacle.y - camera_y
            if -obstacle.height <= obstacle_screen_y <= self.screen_height:
                pygame.draw.rect(screen, (200, 50, 50), 
                              (obstacle.x, obstacle_screen_y, 
                               obstacle.width, obstacle.height))
        
        font = pygame.font.Font(None, 36)
        biome_text = f"{current_biome.value.upper()}"
        text_surface = font.render(biome_text, True, (255, 255, 255))
        screen.blit(text_surface, (self.screen_width - 150, 20))
            
    def check_collision(self, car_rect):
        for obstacle in self.obstacles:
            if car_rect.colliderect(obstacle):
                return True
        return False