import pygame
import sys
import asyncio
from settings import *
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Moon Lantern")
        self.clock = pygame.time.Clock()
        self.level = Level()

    async def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dtime = self.clock.tick(FPS) / 1000
            await self.level.run(dtime)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    asyncio.run(game.run())