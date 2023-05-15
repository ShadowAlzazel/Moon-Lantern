import pygame

class Inventory:
    def __init__(self, slot_amount=3):
        self.slots = {
            'main_hand': None,
            'off_hand': None
        }
        for n in range(slot_amount):
            self.slots[n] = None