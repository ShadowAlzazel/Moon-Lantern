from os import walk
import pygame

def import_folder(path): 
    surface_list = []

    for _, __, img_files in walk(path):
        print(f'HI: {img_files}')
        for image in img_files:
            full_path = f'{path}/{image}'
            print(full_path)
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)


    return surface_list