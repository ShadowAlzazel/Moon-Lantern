import pygame 
from sprites import Generic, Tile, TileFace
from settings import *

class TileRenderer: 
    
    def __init__(self, groups):
        self.groups = groups
        # Scale the image by 
        self._scaled_size = 4
        
        # Load the grass block image
        # TODO: Different block types!!!
        tile_image_path = f"assets/textures/tiles/grass_block.png"
        self.image_surface = pygame.image.load(tile_image_path).convert_alpha()
        
        # Extract and create the three faces from the source texture
        self.faces = self._extract_tile_faces()
        
        # MOVE TO SEPERATE WORLD CLASS !!
        # Define how many tiles wide/high the grid is
        self.grid_width = 25 # COLUMNS 
        self.grid_height = 25 # ROWS
        
        # Create the isometric grid
        # TODO!!! CHange to noise based procedurally generate later.
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
                iso_x, iso_y = self.cart_to_iso(col, row)
                
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
                self._create_face(tile, 'top', has_north, has_east)
                # Show left face only if no tile to the west
                if not has_west:
                    self._create_face(tile, 'left', has_north, has_east)
                # Show right face only if no tile to the south
                if not has_south:
                    self._create_face(tile, 'right', has_north, has_east)      
    
    
    def _extract_tile_faces(self):
        """Extract the top, left and right faces from the tile texture"""
        # Get original dimensions
        orig_width = self.image_surface.get_width()
        orig_height = self.image_surface.get_height()
        
        # Scale dimensions
        self.tile_width = orig_width * self._scaled_size
        self.tile_height = orig_height * self._scaled_size
        
        # Calculate face dimensions (this will depend on your specific texture)
        # These values should be adjusted based on your actual tile texture
        top_height = orig_height // 2
        side_height = orig_height - top_height
        
        # Extract face regions from original texture
        # These coordinates need to be adjusted based on your specific texture layout
        top_surface = self.image_surface.subsurface((0, 0, orig_width, top_height))
        left_surface = self.image_surface.subsurface((0, top_height, orig_width // 2, side_height))
        right_surface = self.image_surface.subsurface((orig_width // 2, top_height, orig_width // 2, side_height))
        
        # Scale the faces
        scaled_top = pygame.transform.scale(
            top_surface, 
            (self.tile_width, top_height * self._scaled_size)
        )
        scaled_left = pygame.transform.scale(
            left_surface, 
            (self.tile_width // 2, side_height * self._scaled_size)
        )
        scaled_right = pygame.transform.scale(
            right_surface, 
            (self.tile_width // 2, side_height * self._scaled_size)
        )
        
        return {
            'top': scaled_top,
            'left': scaled_left,
            'right': scaled_right
        }    
        
        
    def _create_face(self, tile, face_type, has_north, has_east):
        """Create a face for the given tile if it should be visible"""
        face_surface = self.faces[face_type]
        
        # Calculate offsets based on the face type
        if face_type == 'top':
            offset_x, offset_y = 0, 0
        elif face_type == 'left':
            offset_x = 0
            offset_y = self.faces['top'].get_height()
        elif face_type == 'right':
            offset_x = self.faces['left'].get_width()
            offset_y = self.faces['top'].get_height()
        
        # Adjust position based on the tile's base position
        pos = (tile.pos[0] + offset_x, tile.pos[1] + offset_y)
        
        # Create the face sprite
        face = TileFace(
            parent_tile=tile,
            face_type=face_type,
            pos=pos,
            surface=face_surface,
            groups=tile.groups,
            zlayer=LAYERS['ground']
        )
        # Add the face to the tile
        tile.add_face(face_type, face)        
        
        
    def cart_to_iso(self, x, y):
        """
            Convert cartesian grid coordinates (x, y) to isometric screen coordinates.
            Adjust these formulas to get the spacing/look you desire.
        """
        # Basic isometric transform
        iso_x = (x - y) * (self.tile_width // 2)
        iso_y = (x + y) * (self.tile_height // 4)
        return iso_x, iso_y
    
    
    def get_neighboring_tiles(self, col, row):
        """Get the neighboring tiles for a given grid position"""
        neighbors = {
            'north': None,
            'east': None,
            'south': None, 
            'west': None
        }
 
        # Check each direction
        if row > 0:
            neighbors['north'] = self.tile_grid[row-1][col]
        if col < self.grid_width - 1:
            neighbors['east'] = self.tile_grid[row][col+1]
        if row < self.grid_height - 1:
            neighbors['south'] = self.tile_grid[row+1][col]
        if col > 0:
            neighbors['west'] = self.tile_grid[row][col-1] 
        return neighbors