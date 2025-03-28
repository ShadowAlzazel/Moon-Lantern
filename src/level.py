import pygame
import asyncio
from settings import *
from player import Player
from sprites import Generic
from world.tiles import World

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
        
        self.world = World(self.all_sprites)
        #Generic(
        #    pos=(0,0),
        #    surface=pygame.image.load('assets/textures/environment/floor_primordial.png').convert_alpha(),
        #    groups=self.all_sprites,
        #    zlayer=LAYERS['ground']    
        #)

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
        # Zoom 
        self.zoom = 1.0 
        self.min_zoom = 0.5
        self.max_zoom = 4.0
        
    def set_zoom(self, zoom_value): 
        self.zoom = max(self.min_zoom, min(self.max_zoom, zoom_value))
        
    # Drawing to the screen
    async def custom_draw(self, player):
        """
            Draws all sprites relative to the player's position, 
            ensuring the player stays centered on screen when zooming.
        """
        # Compute the 'zoomed' center of the player in world space 
        # (i.e., player world position * zoom).
        player_center_world = pygame.math.Vector2(player.rect.center)  # Player center in world coords
        player_center_zoomed = player_center_world * self.zoom
        
        # The screen center in pixel coords (constant).
        screen_center = pygame.math.Vector2(
            self.display_surface.get_width() / 2,
            self.display_surface.get_height() / 2
        )
        
        # Camera and world Offset 
        self.offset = player_center_zoomed - screen_center
        
        # Each layer should be run blocking and not async
        for layer in LAYERS.values():
            self.current_layer = layer
            render_tasks = []
            for sprite in self.sprites():
                render_tasks.append(asyncio.create_task(self.render_sprite(sprite)))
            done, pending = await asyncio.wait(render_tasks)

    # Main rendering function
    async def render_sprite(self, sprite):
        # Skip offlayer
        if sprite.zlayer != self.current_layer:
            return
        
        # Get the sprite world pos, then convert/zoom it
        sprite_center_world = pygame.math.Vector2(sprite.rect.center)
        sprite_center_zoomed = sprite_center_world * self.zoom
        final_center = sprite_center_zoomed - self.offset
        
        # Scale the sprite image by the zoom
        width = int(sprite.rect.width * self.zoom)
        height = int(sprite.rect.height * self.zoom)
        if width <= 0 or height <= 0:
            return  # Avoid scaling to negative or zero
 
        scaled_image = pygame.transform.scale(sprite.image, (width, height))
        # Adjust rect
        scaled_rect = scaled_image.get_rect(center=final_center)
        
        # Culling check, skip blitting off-screen
        screen_rect = self.display_surface.get_rect()
        if not screen_rect.colliderect(scaled_rect):
            print(f'Skipping sprite in layer [{sprite.zlayer}] with pos({sprite.pos})')
            return
        if (scaled_rect.right < 0 or scaled_rect.left > SCREEN_WIDTH or 
            scaled_rect.bottom < 0 or scaled_rect.top > SCREEN_HEIGHT):
            return
        
        # Display tile 
        self.display_surface.blit(scaled_image, scaled_rect) # Expensive to run 
        # TODO Optimizations
        # IF sprite outside of render range(display) to not blit
        # Create a map of static objects