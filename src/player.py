import pygame
from settings import *
from support import *
from timer import Timer
from inventory import Inventory

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        # Assets
        self.import_assets()
        # Sprite
        self.status = 'down_idle'
        self.frame_index = 0    
        # Image
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.zlayer = LAYERS['main']
        # Hitbox
        #self.hitbox = self.rect.copy().inflate()
        # Movement
        self.direction = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 160
        # Timers
        self.timers = {
            'main_hand': Timer(450, self.use_tool),
            'off_hand': Timer(350, self.use_tool),
            'q_item': Timer(350, self.use_item),
            'e_item': Timer(350, self.use_item)
        }
        # Inventory
        self.inventory = Inventory(9)


    def use_item(self):
        print("IDLE")  


    def use_tool(self):
        print("IDLE")


    # TODO: Use Maps and Asset Postproccessor!
    def import_assets(self):
        # These are the character sub folders
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': []
        }
        for animation in self.animations.keys():
            # Note: If in moon_lantern dir use below if in src directory use -> full_path = f'../assets/character/{animation}'
            full_path = f'assets/character/{animation}'
            self.animations[animation] = import_folder(full_path)


    def animate(self, dtime):
        self.frame_index += 4 * dtime
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]


    def input(self):
        keys_pressed = pygame.key.get_pressed()
        # TODO: Create weapons/tools usable when moving

        # No movement when tool use or use a tool
        if not self.timers['main_hand'].active:
            # Y Axis
            if keys_pressed[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys_pressed[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0
            # X Axis
            if keys_pressed[pygame.K_LEFT]:
                self.status = 'left'
                self.direction.x = -1
            elif keys_pressed[pygame.K_RIGHT]:
                self.status = 'right'
                self.direction.x = 1
            else:
                self.direction.x = 0
            # Item Use whe
            if keys_pressed[pygame.K_q]:
                self.timers['main_hand'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0


    def get_status(self):
        # Check if the player is not moving, then add _idle to status
        if self.direction.magnitude() == 0:
            self.status = f'{self.status.split("_")[0]}_idle'
        # Check tool
        if self.timers['main_hand'].active:
            print("USING TOOL")


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


    def update_timers(self):
        for timer in self.timers.values():
            timer.update()


    def update(self, dtime):
        self.input()
        self.update_timers()
        self.get_status()
        self.move(dtime)
        self.animate(dtime)

