import pygame
from settings import *

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups, layer=LAYERS['MAIN']):
        super().__init__(groups)
        self.image = surface 
        self.rect = self.image.get_rect(topleft=pos)
        self.layer = layer

class Flora(Generic):
    def __init__(self, pos, surface, groups):
        super().__init__(pos, surface, groups)