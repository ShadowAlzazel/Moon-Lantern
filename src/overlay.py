import pygame
from settings import *
from player import Player

class Overlay:
    def __init__(self, player):
        # Setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        
        # Imports 
        self.tools