from PIL import Image
from typing import List, Tuple, Dict

def extract_palette_from_image(palette_image_path: str) -> List[Tuple[int, int, int]]:
    """
    Extracts a color palette from a palette image.
    Assumes the palette image contains one row of color blocks.

    :param palette_image_path: Path to the palette PNG image.
    :return: List of RGB tuples representing the palette.
    """
    palette_image = Image.open(palette_image_path).convert("RGBA")
    palette_pixels = palette_image.getdata()
    
    # Get unique colors in the image, keeping their order
    unique_colors = []
    for color in palette_pixels:
        if color not in unique_colors:
            unique_colors.append(color[:3])  # Exclude alpha channel if present
    return unique_colors


def map_palette(
    image: Image.Image,
    base_palette: List[Tuple[int, int, int]],
    target_palette: List[Tuple[int, int, int]]
) -> Image.Image:
    """
    Maps the grayscale base palette of an image to a target palette.
    
    :param image: Input PIL Image with the base grayscale palette.
    :param base_palette: List of RGB tuples representing the base grayscale palette.
    :param target_palette: List of RGB tuples representing the target color palette.
    :return: A new PIL Image with the mapped colors.
    """
    # Ensure the base and target palettes are the same size
    if len(base_palette) != len(target_palette):
        raise ValueError("Base and target palettes must have the same number of colors.")

    # Convert the image to RGBA mode to manipulate pixel data
    image = image.convert("RGBA")
    pixels = image.load()

    # Create a mapping dictionary from base palette to target palette
    color_map: Dict[Tuple[int, int, int, int], Tuple[int, int, int, int]] = {
        (*base_color, 255): (*target_color, 255)
        for base_color, target_color in zip(base_palette, target_palette)
    }

    # Replace colors in the image
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            current_color = pixels[x, y]
            if current_color in color_map:
                pixels[x, y] = color_map[current_color]

    return image


def generate_atlas_variants(
    image_path: str,
    base_palette: List[Tuple[int, int, int]],
    palettes: Dict[str, List[Tuple[int, int, int]]]
) -> Dict[str, Image.Image]:
    """
    Generates color variants of an image based on different target palettes.

    :param image_path: Path to the base image file.
    :param base_palette: List of RGB tuples representing the base grayscale palette.
    :param palettes: A dictionary where keys are palette names, and values are target palettes.
    :return: A dictionary of palette names to the corresponding PIL Image variants.
    """
    base_image = Image.open(image_path)
    variants = {
        name: map_palette(base_image.copy(), base_palette, palette)
        for name, palette in palettes.items()
    }
    return variants


def generate_mapped_image(image: Image.Image, palette: str) -> Image.Image:
    atlas: str = f'assets/textures/color_map/material/_atlas_map.png'
    palette: str = f'assets/textures/color_map/material/{palette}.png'
    map_data = lambda x: extract_palette_from_image(x)
    mapped_img = map_palette(image, map_data(atlas), map_data(palette))
    return mapped_img