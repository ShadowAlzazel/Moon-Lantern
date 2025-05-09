
import pygame
import os
from sprites import TileFace
from settings import LAYERS

class TileRenderer:
    """
    Handles the rendering of tile faces and face culling.
    """
    def __init__(self, groups):
        self.groups = groups
        # Scale the image by 
        self._scaled_size = 4
        # Determine tile dimensions based on loaded textures
        self.tile_width = 32 * self._scaled_size  # Base texture is 32x32
        self.tile_height = 32 * self._scaled_size
        
        # Load the tile textures for different types
        self.tile_textures = self._load_tile_textures()
        
    def _load_tile_textures(self):
        """Load textures for different tile types"""
        textures = {}
        face_dir = "assets/textures/faces"
        
        # Check if faces directory exists
        if not os.path.exists(face_dir):
            # If not, run the texture splitter
            from utils.textures import TextureSplitter
            splitter = TextureSplitter()
            # This will create the faces directory and populate it
            # with the split textures
            splitter.split_all_textures()
        
        # Load textures for different tile types
        tile_types = ['grass_block', 'red_grass_block']  # Add more as needed
        
        for tile_type in tile_types:
            textures[tile_type] = {}
            for face_type in ['top', 'left', 'right']:
                face_path = os.path.join(face_dir, f"{tile_type}_{face_type}.png")
                if os.path.exists(face_path):
                    # Load the face texture
                    face_surface = pygame.image.load(face_path).convert_alpha()
                    # Scale it
                    scaled_face = pygame.transform.scale(
                        face_surface, 
                        (face_surface.get_width() * self._scaled_size, 
                         face_surface.get_height() * self._scaled_size)
                    )
                    textures[tile_type][face_type] = scaled_face
                else:
                    print(f"Warning: Face texture {face_path} not found! Using fallback.")
                    # Use red_grass_block as fallback if the texture is missing
                    fallback_path = os.path.join(face_dir, f"red_grass_block_{face_type}.png")
                    if os.path.exists(fallback_path):
                        face_surface = pygame.image.load(fallback_path).convert_alpha()
                        # Scale it
                        scaled_face = pygame.transform.scale(
                            face_surface, 
                            (face_surface.get_width() * self._scaled_size, 
                             face_surface.get_height() * self._scaled_size)
                        )
                        textures[tile_type][face_type] = scaled_face
        
        return textures
    
    def create_face(self, tile, face_type, tile_type=None):
        """Create a face for the given tile if it should be visible"""
        if tile_type is None:
            tile_type = "grass_block"  # Default
            
        # If the tile type doesn't exist, use grass_block as fallback
        if tile_type not in self.tile_textures:
            tile_type = "grass_block"
            
        # Get the face texture for this tile type
        face_surface = self.tile_textures[tile_type].get(face_type)
        if not face_surface:
            print(f"Warning: No texture for {tile_type}_{face_type}")
            return
        
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
        
    def cart_to_iso(self, x, y):
        """
        Convert cartesian grid coordinates (x, y) to isometric screen coordinates.
        Adjust these formulas to get the spacing/look you desire.
        """
        # Basic isometric transform
        iso_x = (x - y) * (self.tile_width // 2)
        iso_y = (x + y) * (self.tile_height // 4)
        return iso_x, iso_y
        
    def iso_to_cart(self, iso_x, iso_y):
        """
        Convert isometric screen coordinates to cartesian grid coordinates.
        This is the inverse of cart_to_iso.
        """
        # Inverse of isometric transform
        half_tile_width = self.tile_width // 2
        quarter_tile_height = self.tile_height // 4
        
        # Calculate grid coordinates
        grid_y = (iso_y / quarter_tile_height - iso_x / half_tile_width) / 2
        grid_x = (iso_y / quarter_tile_height + iso_x / half_tile_width) / 2
        
        return grid_x, grid_y