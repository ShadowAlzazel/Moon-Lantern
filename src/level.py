import pygame
from settings import *
from player import Player

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        # Sprite Groups
        self.all_sprites = pygame.sprite.Group()
        # Setup
        self.setup()

    def setup(self):
        self.player = Player((360, 640), self.all_sprites)

    def run(self, dtime):
        # Sprites
        self.display_surface.fill("Black")
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dtime)