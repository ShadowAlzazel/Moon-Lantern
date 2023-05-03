import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        # Image in W x H
        self.image = pygame.Surface((32, 64))
        self.image.fill("Green")
        self.rect = self.image.get_rect(center=pos)
        # Movement
        self.direction = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 160

    def input(self):
        keys_pressed = pygame.key.get_pressed()
        # Y Axis
        if keys_pressed[pygame.K_UP]:
            self.direction.y = -1
        elif keys_pressed[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        # X Axis
        if keys_pressed[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys_pressed[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def move(self, dtime):
        # Normalize direction
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        # Horizontal 
        self.pos.x += self.direction.x * self.speed * dtime
        self.rect.centerx = self.pos.x
        # Vertical 
        self.pos.y += self.direction.y * self.speed * dtime
        self.rect.centery = self.pos.y
        #print(self.direction)

    def update(self, dtime):
        self.input()
        self.move(dtime)