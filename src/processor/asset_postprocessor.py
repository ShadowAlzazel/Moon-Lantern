import pygame, sys
from support import *

class AssetPostprocessor:
    def __init__(self, rootpath):
        self.rootpath = rootpath
        self.EXTENSION_PNG = '.png'
        self.PIXEL_MAP_SUFFIX = '.map'
        self.SOURCE_PREFIX = 'source.'

    def on_postprocess_texture():
        pass

    def process_pixel_atlas(self, surface, file_name: str):
        if not file_name.find('_'):
            return 
        
        map_name = f'{file_name.split("_")[0]}{self.PIXEL_MAP_SUFFIX}'


    def find_pixel_map(self):
        pass

    