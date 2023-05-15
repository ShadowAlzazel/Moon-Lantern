import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self, pos, group, name="item"):
        super().__init__(group)
        # Assets
        self.name = name
        self.import_assets()  
        # Sprite
        self.status = 'down'
        self.frame_index = 0    

    # TODO: Use Maps and Asset Postproccessor!
    def import_assets(self):
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': []
        }
        for animation in self.animations.keys():
            full_path = f'assets/items/{self.name}/{animation}'
            self.animations[animation] = import_folder(full_path)