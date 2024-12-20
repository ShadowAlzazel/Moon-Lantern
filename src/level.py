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
            surface=pygame.image.load('assets/textures/environment/floor_primordial.png').convert_alpha(),
            groups=self.all_sprites,
            zlayer=LAYERS['ground']    
        )

    async def run(self, dtime):
        # Basic bg
        self.display_surface.fill("black")
        # Draw all sprites
        await self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dtime)


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    async def custom_draw(self, player):
        # Offset 
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2
        
        # Each layer should be run blocking and not async
        for layer in LAYERS.values():
            self.current_layer = layer
            render_tasks = [asyncio.create_task(self.render_sprite(sprite)) for sprite in self.sprites()]
            done, pending = await asyncio.wait(render_tasks)
            # Note: Remove ALL async def if running this
            #for sprite in self.sprites():
            #   if sprite.zlayer == layer:
            #    self.display_surface.blit(sprite.image, sprite.rect)

    # Main rendering function
    async def render_sprite(self, sprite):
        if sprite.zlayer == self.current_layer:
            offset_rect = sprite.rect.copy()
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect) # Expensive to run
            
        # TODO Optimizations
        # IF sprite outside of render range(display) to not blit
        
        # Create a map of static objects
