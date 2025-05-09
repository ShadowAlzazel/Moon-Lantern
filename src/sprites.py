import pygame
from settings import *

# Generic Class for all other sprites
class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups, zlayer=LAYERS['main']):
        super().__init__(groups)
        self.pos = pos
        self.image = surface 
        self.rect = self.image.get_rect(topleft=pos)
        self.zlayer = zlayer

class Tile(pygame.sprite.Sprite):
    """
    A tile in the isometric world that can have up to three visible faces
    """
    def __init__(self, pos, groups, zlayer=LAYERS['ground'], grid_pos=None):
        super().__init__(groups)
        self.pos = pos
        self.grid_pos = grid_pos  # Store the grid position (col, row)
        self.zlayer = zlayer
        self.groups = groups
        
        # Store references to the faces of this tile
        self.faces = {
            'top': None,
            'left': None,
            'right': None
        }
        
        # Create an empty surface for the tile itself
        # This is used just for collision detection and doesn't get rendered
        self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos)
    
    def add_face(self, face_type, face_sprite):
        """Add a face to this tile"""
        self.faces[face_type] = face_sprite


class TileFace(Generic):
    """
    A single face of a tile (top, left, or right)
    """
    def __init__(self, parent_tile, face_type, pos, surface, groups, zlayer=LAYERS['ground']):
        super().__init__(pos, surface, groups, zlayer)
        self.parent_tile = parent_tile  # Reference to the parent tile
        self.face_type = face_type      # Which face: 'top', 'left', or 'right'
        
        # Adjust the drawing order (z-sorting) based on the face type
        # This ensures proper overlapping of faces
        z_offset = 0
        if face_type == 'right':
            z_offset = 1
        elif face_type == 'left':
            z_offset = 2
        elif face_type == 'top':
            z_offset = 3
            
        self.zlayer = zlayer + z_offset / 10.0  # Small offset to ensure proper ordering


class Particle(Generic):
    def __init__(self, pos, surf, groupgs, z, duration=200):
        super().__init__(pos, surface, groups)
        self.start_time = pygame.tim.get_ticks()
        self.duration = duration
        
        # Replace white surface
        mask_surf = pygame.mask.from_surface(self.image)
        new_surf = mask_surf.to_surface()
        new_surf.set_colorkey((0,0,0))
        self.image = new_surf


class Flora(Generic):
    def __init__(self, pos, surface, groups, zlayer=LAYERS['plant']):
        super().__init__(pos, surface, groups)
        self.image = surface 
        self.rect = self.image.get_rect(topleft=pos)
        self.zlayer = zlayer


class Entities(Generic):
    def __init__(self, pos, surface, groups, zlayer=LAYERS['entities']):
        super().__init__(pos, surface, groups)
        self.image = surface 
        self.rect = self.image.get_rect(topleft=pos)
        self.zlayer = zlayer