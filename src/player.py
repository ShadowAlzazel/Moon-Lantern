import pygame
from typing import Dict, List, Tuple, Union
from settings import *
from support import *
from timer import Timer
from inventory import Inventory
from item import Item
from processor.atlas_mapper import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos: Tuple[int, int], group: pygame.sprite.Group) -> None:
        super().__init__(group)
        # Assets
        self._import_assets()
        # Sprite
        self.status: str = 'down_idle'
        self.frame_index: float = 0.0
        # Image
        self.image: pygame.Surface = self.animations[self.status][int(self.frame_index)]
        self.rect: pygame.Rect = self.image.get_rect(center=pos)
        self.zlayer: int = LAYERS['main']
        # Hitbox
        # self.hitbox = self.rect.copy().inflate()
        # Movement
        self.direction: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
        self.pos: pygame.math.Vector2 = pygame.math.Vector2(self.rect.center)
        self.speed: int = 200
        # Timers
        self.timers: Dict[str, Timer] = {
            'main_hand': Timer(450, self.use_tool),
            'off_hand': Timer(350, self.use_tool),
            'q_item': Timer(350, self.use_item),
            'e_item': Timer(350, self.use_item),
        }
        self._setup_inventory()
      
        
    def _import_assets(self) -> None:
        self.animations: Dict[str, List[pygame.Surface]] = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': []
        }
        for animation in self.animations.keys():
            full_path: str = f'assets/textures/character/{animation}'
            self.animations[animation] = import_folder(full_path)


    def _setup_inventory(self) -> None:
        self.inventory: Inventory = Inventory(9)
        self.inventory.slots['main_hand'] = 1


    def use_item(self) -> None:
        print("IDLE")  


    def use_tool(self) -> None:
        if self.inventory.slots['main_hand']:
            print("USE TOOL")


    def animate(self, dtime: float) -> None:
        self.frame_index += 4 * dtime
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]


    def input(self) -> None:
        keys_pressed: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
        if not self.timers['main_hand'].active:
            # Y Axis
            if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0
            # X Axis
            if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
                self.status = 'left'
                self.direction.x = -1
            elif keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
                self.status = 'right'
                self.direction.x = 1
            else:
                self.direction.x = 0
            # Item Use
            if keys_pressed[pygame.K_q]:
                self.timers['main_hand'].activate()
                self.direction = pygame.math.Vector2() # Some tools allow movement while casting
                self.frame_index = 0


    def get_status(self) -> None:
        # Idling
        if self.direction.magnitude() == 0:
            self.status = f'{self.status.split("_")[0]}_idle'
            
        # Using main hand    
        if self.timers['main_hand'].active:
            #self.status = 'axe'
            full_path: str = f'assets/textures/item/axe.png'
            axe_img = import_image(full_path)
            mapped_img = generate_mapped_image(axe_img, "iridium")
            surface_img = image_to_surface(mapped_img)
            self.image.blit(surface_img, (0,0))


    def move(self, dtime: float) -> None:
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        # Horizontal 
        self.pos.x += self.direction.x * self.speed * dtime
        self.rect.centerx = self.pos.x
        # Vertical 
        self.pos.y += self.direction.y * self.speed * dtime
        self.rect.centery = self.pos.y


    def update_timers(self) -> None:
        for timer in self.timers.values():
            timer.update()


    def update(self, dtime: float) -> None:
        self.input()
        self.update_timers()
        self.get_status()
        self.move(dtime)
        self.animate(dtime)