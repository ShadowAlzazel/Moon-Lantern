import os
import pygame
from sprites import Tile
from settings import LAYERS
from world.tiles import TileRenderer

class World:
    """
    Handles the creation and management of the world grid.
    """
    def __init__(self, groups: pygame.sprite.Group):
        self.groups = groups
        
        # Create the tile renderer
        self.tile_renderer = TileRenderer(groups=groups)
        
        # Define how many tiles wide/high the grid is
        self.grid_width = 25  # COLUMNS 
        self.grid_height = 25  # ROWS
        
        # Create the isometric grid
        # TODO!!! Change to noise based procedurally generate later.
        self.tile_grid = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.create_isometric_grid()
        
    def create_isometric_grid(self):
        """
        Creates an isometric grid with face-based tiles and handles face culling.
        """
        # First, create all tile positions in the grid
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                # Convert cartesian (row, col) to isometric coordinates
                iso_x, iso_y = self.tile_renderer.cart_to_iso(col, row)
                
                # Create a new tile at this position
                self.tile_grid[row][col] = Tile(
                    pos=(iso_x, iso_y),
                    groups=self.groups,
                    zlayer=LAYERS['ground'],
                    grid_pos=(col, row)
                )
        
        # Now that all tiles are created, determine face visibility for each tile
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                tile = self.tile_grid[row][col]
                
                # Check if neighboring tiles exist to determine which faces to show
                has_north = row > 0
                has_east = col < self.grid_width - 1
                has_south = row < self.grid_height - 1
                has_west = col > 0
                
                # Always show the top face
                self.tile_renderer.create_face(tile, 'top')
                
                # Show left face only if no tile to the west
                if not has_east:
                    self.tile_renderer.create_face(tile, 'right')
                
                # Show right face only if no tile to the south
                if not has_south:
                    self.tile_renderer.create_face(tile, 'left')
    
    def get_neighboring_tiles(self, col, row):
        """Returns neighboring tiles in the grid"""
        neighbors = {}
        
        # Check all four directions
        directions = {
            'north': (0, -1),
            'east': (1, 0),
            'south': (0, 1),
            'west': (-1, 0)
        }
        
        for direction, (dx, dy) in directions.items():
            new_col, new_row = col + dx, row + dy
            
            # Check if the new position is within grid bounds
            if 0 <= new_col < self.grid_width and 0 <= new_row < self.grid_height:
                neighbors[direction] = self.tile_grid[new_row][new_col]
            else:
                neighbors[direction] = None
                
        return neighbors