import pygame
import sys
import asyncio
from settings import *
from level import Level

FPS_ON = True

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Moon Lantern")
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.font = pygame.font.SysFont(None, 30)  # Default font, size 30

    async def run(self):
        while True:
            for event in pygame.event.get():
                # Quitting
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Zooming 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                        # Zoom in
                        new_zoom = self.level.all_sprites.zoom + 0.1
                        self.level.all_sprites.set_zoom(new_zoom)
                    elif event.key == pygame.K_MINUS:
                        # Zoom out
                        new_zoom = self.level.all_sprites.zoom - 0.1
                        self.level.all_sprites.set_zoom(new_zoom)
                
            # Frame timer
            dtime = self.clock.tick(FPS) / 1000
            await self.level.run(dtime)
            
            # Draw FPS
            if FPS_ON:
                fps = self.clock.get_fps()
                fps_text = self.font.render(f'FPS: {fps:.1f}', True, pygame.Color('white'))
                self.screen.blit(fps_text, (10, 10))
            
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    asyncio.run(game.run())