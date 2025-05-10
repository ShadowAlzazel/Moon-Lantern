import pygame
from world.chunks import ChunkManager
from world.noise import NoiseGenerator

class World:
    """
    Main class for the procedural world using Simplex noise.
    Handles the chunk loading/unloading and is the interface to the game world.
    """
    def __init__(self, groups: pygame.sprite.Group, seed=None):
        self.groups = groups
        
        # Create the noise generator
        self.noise_gen = NoiseGenerator(seed=seed)
        # Create the chunk manager
        self.chunk_manager = ChunkManager(groups=groups, noise_gen=self.noise_gen)
        
    def update(self, player_pos):
        """
        Update the world based on player position.
        This handles loading and unloading chunks.
        """
        self.chunk_manager.update_chunks(player_pos)
    
    def get_world_pos_at_screen_pos(self, screen_x, screen_y):
        """
        Convert a screen position to a world position.
        Useful for mouse interactions.
        """
        # First convert to isometric coordinates
        tile_renderer = self.chunk_manager.tile_renderer
        grid_x, grid_y = tile_renderer.iso_to_cart(screen_x, screen_y)
        
        # Round to nearest integer for grid coordinates
        return int(grid_x), int(grid_y)
    
    def get_tile_at_world_pos(self, world_x, world_y):
        """
        Get the tile at the specified world position.
        """
        return self.chunk_manager.get_tile_at(world_x, world_y)
    
    def get_tile_at_screen_pos(self, screen_x, screen_y):
        """
        Get the tile at the specified screen position.
        """
        world_x, world_y = self.get_world_pos_at_screen_pos(screen_x, screen_y)
        return self.get_tile_at_world_pos(world_x, world_y)