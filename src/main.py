import pygame
import sys
import asyncio
from settings import *
from level import Level
from utils.debug import DebugOverlay

FPS_ON = True

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Moon Lantern")
        self.clock = pygame.time.Clock()
        self.debug = DebugOverlay(game=self)
        self.level = Level(game=self)
        self.font = pygame.font.SysFont(None, 30)  # Default font, size 30

    async def run(self):
        while True:
            for event in pygame.event.get():
                # Quitting
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Pressed Key Events
                if event.type == pygame.KEYDOWN:
                    ### Zoom
                    if event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                        # Zoom in
                        new_zoom = self.level.all_sprites.zoom + 0.1
                        self.level.all_sprites.set_zoom(new_zoom)
                    elif event.key == pygame.K_MINUS:
                        # Zoom out
                        new_zoom = self.level.all_sprites.zoom - 0.1
                        self.level.all_sprites.set_zoom(new_zoom)
                    ### DEBUG
                    if event.key == pygame.K_F3:
                        self.debug.toggle()
                    if event.key == pygame.K_F4:
                        self.debug.toggle_chunk_borders()
                
            # Frame timer
            dtime = self.clock.tick(FPS) / 1000
            await self.level.run(dtime)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    asyncio.run(game.run())