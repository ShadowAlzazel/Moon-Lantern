import pygame 
import os
from sprites import Generic, Tile, TileFace
from settings import *

class TileRenderer: 
    
    def __init__(self, groups):
        self.groups = groups
        # Scale the image by 
        self._scaled_size = 4
        # Determine tile dimensions based on loaded textures
        self.tile_width = 32 * self._scaled_size  # Base texture is 32x32
        self.tile_height = 32 * self._scaled_size
        
        # Load the grass block image
        # TODO: Different block types!!!
        tile_image_path = f"assets/textures/tiles/grass_block.png"
        self.image_surface = pygame.image.load(tile_image_path).convert_alpha()
        
        # Extract and create the three faces from the source texture
        self.faces = self._load_face_textures()
        
        # MOVE TO SEPERATE WORLD CLASS !!
        # Define how many tiles wide/high the grid is
        self.grid_width = 5 # COLUMNS 
        self.grid_height = 5 # ROWS
        
        # Create the isometric grid
        # TODO!!! CHange to noise based procedurally generate later.
        self.tile_grid = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.create_isometric_grid()
      
        
    def _load_face_textures(self):
        """Load the pre-processed face textures"""
        faces = {}
        face_dir = "assets/textures/faces"
        
        # Check if faces directory exists
        if not os.path.exists(face_dir):
            # If not, run the texture splitter
            from utils.textures import TextureSplitter
            splitter = TextureSplitter()
            # This will create the faces directory and populate it
            # with the split textures
            splitter.split_all_textures()
        
        # Load the face textures for grass block
        base_name = "red_grass_block"
        
        for face_type in ['top', 'left', 'right']:
            face_path = os.path.join(face_dir, f"{base_name}_{face_type}.png")
            if os.path.exists(face_path):
                # Load the face texture
                face_surface = pygame.image.load(face_path).convert_alpha()
                # Scale it
                scaled_face = pygame.transform.scale(
                    face_surface, 
                    (face_surface.get_width() * self._scaled_size, 
                     face_surface.get_height() * self._scaled_size)
                )
                faces[face_type] = scaled_face
            else:
                print(f"Warning: Face texture {face_path} not found!")
        
        return faces
        
        
    def _create_face(self, tile, face_type):
        """Create a face for the given tile if it should be visible"""
        face_surface = self.faces[face_type]
        
        # Calculate position offsets for the face based on the tile's position
        base_x, base_y = tile.pos
        
        # Adjust Z-ordering for proper overlapping
        z_offset = 0
        
        # Calculate offset based on the texture splitter's polygon definitions
        # These offsets should match the polygon coordinates used in TextureSplitter
        if face_type == 'top':
            # Top face is centered on the tile
            offset_x = 0
            offset_y = 0
            z_offset = 0.3  # Top face should be above side faces
        elif face_type == 'right':
            # Left face should align with the left edge of the isometric tile
            offset_x = 0
            offset_y = 0
            z_offset = 0.2  # Left face above right face
        elif face_type == 'left':
            # Right face should align with the right half of the isometric tile
            offset_x = 0
            offset_y = 0
            z_offset = 0.1  # Right face at a middle z-level
        
        # Calculate final position
        pos = (base_x + offset_x, base_y + offset_y)
        
        # Create the face sprite
        face = TileFace(
            parent_tile=tile,
            face_type=face_type,
            pos=pos,
            surface=face_surface,
            groups=tile.groups,
            zlayer=LAYERS['ground'] + z_offset  # Add small offset for z-ordering
        )
        
        # Add the face to the tile
        tile.add_face(face_type, face) 
        
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
                self._create_face(tile, 'top')
                
                # Show left face only if no tile to the west
                if not has_east:
                    self._create_face(tile, 'right')
                
                # Show right face only if no tile to the south
                if not has_south:
                    self._create_face(tile, 'left') 
        
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