
import noise
import random
import numpy as np
from typing import Tuple, Dict, List, Any

class NoiseGenerator:
    """
    Handles Simplex noise generation for procedural terrain.
    """
    def __init__(self, seed=None):
        # Set seed for reproducibility
        self.seed = seed if seed is not None else random.randint(0, 999999)
        random.seed(self.seed)
        
        # Default noise parameters
        self.octaves = 3
        self.persistence = 0.5
        self.lacunarity = 2.0
        self.scale = 100.0
        self.offset_x = random.randint(-10000, 10000)
        self.offset_y = random.randint(-10000, 10000)
        
        # Biome thresholds
        self.biome_thresholds = {
            "deep_water": -0.6,
            "shallow_water": -0.3,
            "sand": -0.1,
            "grass": 0.3,
            "forest": 0.6,
            "mountain": 0.8,
            "snow": 1.0
        }
        
    def get_noise_at(self, x: int, y: int) -> float:
        """
        Get the noise value at a specific world position.
        Returns a value between -1 and 1.
        """
        # Apply offsets for variation
        nx = (x + self.offset_x) / self.scale
        ny = (y + self.offset_y) / self.scale
        
        # Generate noise with multiple octaves for natural-looking terrain
        value = 0
        max_value = 0
        amplitude = 1
        frequency = 1
        
        for _ in range(self.octaves):
            value += noise.snoise2(nx * frequency, ny * frequency, base=self.seed) * amplitude
            max_value += amplitude
            amplitude *= self.persistence
            frequency *= self.lacunarity
            
        # Normalize to range [-1, 1]
        return value / max_value
        
    def get_biome_at(self, x: int, y: int) -> str:
        """
        Determine the biome type at the given coordinates based on noise.
        """
        noise_value = self.get_noise_at(x, y)
        
        # Map noise value to biome
        if noise_value < self.biome_thresholds["deep_water"]:
            return "deep_water"
        elif noise_value < self.biome_thresholds["shallow_water"]:
            return "shallow_water"
        elif noise_value < self.biome_thresholds["sand"]:
            return "sand"
        elif noise_value < self.biome_thresholds["grass"]:
            return "grass"
        elif noise_value < self.biome_thresholds["forest"]:
            return "forest"
        elif noise_value < self.biome_thresholds["mountain"]:
            return "mountain"
        else:
            return "snow"
    
    def get_tile_type(self, x: int, y: int) -> str:
        """
        Get the tile type for a specific world position based on the biome.
        """
        biome = self.get_biome_at(x, y)
        
        # Map biomes to tile types
        biome_to_tile = {
            "deep_water": "water_block",
            "shallow_water": "water_block",
            "sand": "sand_block",
            "grass": "grass_block",
            "forest": "grass_block",  # Could be a special forest block
            "mountain": "stone_block",
            "snow": "snow_block"
        }
        
        # For now, we only have two tile types implemented, so we'll simplify
        simplified_mapping = {
            "deep_water": "red_grass_block",  # Placeholder
            "shallow_water": "red_grass_block",  # Placeholder
            "sand": "red_grass_block",
            "grass": "grass_block",
            "forest": "grass_block",
            "mountain": "red_grass_block",
            "snow": "red_grass_block"
        }
        
        return simplified_mapping[biome]
        
    def get_elevation(self, x: int, y: int) -> int:
        """
        Calculate elevation based on noise.
        """
        noise_value = self.get_noise_at(x, y)
        
        # Map noise to elevation (0-3 blocks high for now)
        if noise_value < self.biome_thresholds["shallow_water"]:
            return 0  # Water level
        elif noise_value < self.biome_thresholds["forest"]:
            return 1  # Regular land
        elif noise_value < self.biome_thresholds["mountain"]:
            return 2  # Hills
        else:
            return 3  # Mountains