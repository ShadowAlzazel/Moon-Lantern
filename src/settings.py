from pygame.math import Vector2

# Screen
SCREEN_WIDTH = 1920
SCREEN_HEIGHT= 1080
TILE_SIZE = 64
_ASSET_SIZE = 16 # A 16x16 is the standard size

# Framerate
FPS = 120

# Overlay 
OVERLAY_POSITIONS = {
    'tool': (40, SCREEN_HEIGHT - 15),
    'seed': (70, SCREEN_HEIGHT - 5)
}

PLAYER_TOOL_OFFSET = {
    'left': Vector2(-50, 40),
    'right': Vector2(50, 40),
    'up': Vector2(0, -10),
    'down': Vector2(0, 50)
}

LAYERS = {
    'water': 0,
    'ground': 1,
    'soil': 2,
    'soil_water': 3,
    'rain_floor': 4,
    'structure_bottom': 5,
    'plant': 6,
    'main': 9,
    'entities': 10,
    'structure_top': 11,
    'fruit_plant': 12,
    'rain_drops': 13,
}