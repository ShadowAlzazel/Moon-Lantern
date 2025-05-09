import pygame
import os
import sys

from PIL import Image
from typing import Dict, List, Tuple, Union

def import_folder(path): 
    surface_list = []
    for _, __, img_files in os.walk(path):
        for image in img_files:
            full_path = f'{path}/{image}'
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)

    return surface_list

def import_image(path: str) -> Image.Image:
    image = Image.open(path)
    return image

def import_surface(path: str) -> pygame.Surface:
    image_surface = pygame.image.load(path).convert_alpha()
    return image_surface

def image_to_surface(image: Image.Image) -> pygame.Surface:
    pil_image = image.convert("RGBA")
    raw_data = pil_image.tobytes()
    # Create a Pygame Surface
    surface = pygame.image.frombuffer(raw_data, pil_image.size, "RGBA")
    return surface