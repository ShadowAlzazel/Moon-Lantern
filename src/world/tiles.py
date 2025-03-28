import pygame 
from sprites import Generic, Tile
from settings import *

class World: 
    
    def __init__(self, groups):
        self.groups = groups
        
        # TODO: Custom iter for each block
        # Load the grass block image
        tile_image_path = f"assets/textures/tiles/grass_block.png"
        self.image_surface = pygame.image.load(tile_image_path).convert_alpha()
        self.image_width = self.image_surface.get_width()
        self.image_height = self.image_surface.get_height()
        # TODO: Change BLock to tri face object, and only render the face that is shown 
        
        
        # Scale the image by 
        _scaled_size = 4
        self.tile_width = self.image_width * _scaled_size
        self.tile_height = self.image_height * _scaled_size
        self.tile_surface = pygame.transform.scale(self.image_surface, (self.tile_width, self.tile_height))
        
        # Define how many tiles wide/high the grid is
        self.grid_width = 5 # COLUMNS 
        self.grid_height = 5 # ROWS
        
        # Create the isometric grid
        self.tile_grid = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.create_isometric_grid()
        
    def create_isometric_grid(self):
        """
            Loops over grid positions and converts each to isometric coordinates.
            Then creates a Tile sprite and places it in the all_sprites group.
        """
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                # Convert cartesian (row, col) to isometric coordinates
                iso_x, iso_y = self.cart_to_iso(col, row)
                # Create the tile and add it to the groups
                self.tile_grid[row][col] = Tile(
                    pos=(iso_x, iso_y),
                    surface=self.tile_surface,
                    groups=self.groups,
                    zlayer=LAYERS['ground']
                )         
        
    def cart_to_iso(self, x, y):
        """
            Convert cartesian grid coordinates (x, y) to isometric screen coordinates.
            Adjust these formulas to get the spacing/look you desire.
        """
        # Basic isometric transform
        iso_x = (x - y) * (self.tile_width // 2)
        iso_y = (x + y) * (self.tile_height // 4)
        return iso_x, iso_y
    