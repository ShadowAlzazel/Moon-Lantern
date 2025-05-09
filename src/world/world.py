import pygame 

from world.tiles import TileRenderer

class World:
    
    def __init__(self, groups):
        self.groups = groups 
        # Create the tile renderer
        self.tile_renderer = TileRenderer(groups=groups)