import pygame
from settings import *

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups, zlayer=LAYERS['main']):
        super().__init__(groups)
        self.image = surface 
        self.rect = self.image.get_rect(topleft=pos)
        self.zlayer = zlayer

class Flora(Generic):
    def __init__(self, pos, surface, groups, zlayer=LAYERS['floor_plant']):
        super().__init__(pos, surface, groups)
        self.image = surface 
        self.rect = self.image.get_rect(topleft=pos)
        self.zlayer = zlayer

class Fauna(Generic):
    def __init__(self, pos, surface, groups, zlayer=LAYERS['main']):
        super().__init__(pos, surface, groups)
        self.image = surface 
        self.rect = self.image.get_rect(topleft=pos)
        self.zlayer = zlayer