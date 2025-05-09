import pygame
import asyncio
from settings import *
from player import Player
from sprites import Generic
from world.world import World

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
        # Cache for scaled images
        self.scaled_cache = {}
        # Track visible sprites for optimization
        self.visible_sprites = []
        
        
    def set_zoom(self, zoom_value): 
        self.zoom = max(self.min_zoom, min(self.max_zoom, zoom_value))
        
    # Drawing to the screen
    async def custom_draw(self, player):
        """
            Draws all sprites relative to the player's position, 
            ensuring the player stays centered on screen when zooming.
            Only visible sprites will be rendered.
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
        
        # Camera and world Offset - this is the key to keeping player centered
        self.offset = player_center_zoomed - screen_center
        
        # Screen rect for culling
        screen_rect = self.display_surface.get_rect()
        
        # Sort sprites by their z-layer for proper drawing order
        # This ensures tiles are drawn from back to front
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.zlayer):
            # Skip empty tile containers (they won't have images)
            if not hasattr(sprite, 'image') or sprite.image is None:
                continue
            
            # Get the sprite world pos, then convert/zoom it
            sprite_center_world = pygame.math.Vector2(sprite.rect.topleft)
            sprite_pos_zoomed = sprite_center_world * self.zoom
            final_pos = sprite_pos_zoomed - self.offset
            
            # Scale the sprite image by the zoom (with caching)
            width = int(sprite.rect.width * self.zoom)
            height = int(sprite.rect.height * self.zoom)
            if width <= 0 or height <= 0:
                continue  # Avoid scaling to negative or zero
            
            # Use cached scaled image if available
            cache_key = (id(sprite.image), width, height)
            if cache_key in self.scaled_cache:
                scaled_image = self.scaled_cache[cache_key]
            else:
                scaled_image = pygame.transform.scale(sprite.image, (width, height))
                # Cache the scaled image for future use
                self.scaled_cache[cache_key] = scaled_image
            
            # Adjust rect for positioning
            scaled_rect = scaled_image.get_rect(topleft=final_pos)
            
            # Skip rendering if sprite is outside the screen
            if not screen_rect.colliderect(scaled_rect):
                continue
            
            # Display the sprite
            self.display_surface.blit(scaled_image, scaled_rect)