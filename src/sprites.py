import pygame
from settings import *

# Generic Class for all other sprites
class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups, zlayer=LAYERS['main']):
        super().__init__(groups)
        self.image = surface 
        self.rect = self.image.get_rect(topleft=pos)
        self.zlayer = zlayer

class Tile(Generic):
    """A single tile in the world"""
    def __init__(self, pos, surface, groups, zlayer=LAYERS['ground']):
        super().__init__(pos, surface, groups)
        self.image = surface 
        self.rect = self.image.get_rect(topleft=pos)
        self.zlayer = zlayer

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