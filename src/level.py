import pygame
import asyncio
from settings import *
from player import Player
from sprites import Generic

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        # Sprite Groups
        self.all_sprites = CameraGroup()
        # Setup
        self.setup()

    def setup(self):
        self.current_layer = LAYERS['ground']
        self.player = Player((360, 640), self.all_sprites)
        Generic(
            pos=(0,0),
            surface=pygame.image.load('assets/environment/temp_floor.png').convert_alpha(),
            groups=self.all_sprites,
            zlayer=LAYERS['ground']    
        )

    def run(self, dtime):
        # Sprites
        self.display_surface.fill("Black")
        #self.all_sprites.draw(self.display_surface)
        self.all_sprites.camera_draw()
        self.all_sprites.update(dtime)

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    async def camera_draw(self):
        for layer in LAYERS.values():
            current_layer = layer
            render_tasks = [asyncio.create_task(render_sprite(sprite)) for sprite in self.sprites]
            done, pending = await asyncio.wait(render_tasks)

            #for sprite in self.sprites():
            #    if sprite.zlayer == layer:
            #        self.display_surface.blit(sprite.image, sprite.rect)
    
    async def render_sprite(self):
        if sprite.zlayer == current_layer:
            self.display_surface.blit(sprite.image, sprite.rect)
