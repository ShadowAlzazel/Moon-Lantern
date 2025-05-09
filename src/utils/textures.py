import pygame
import os
import sys

class TextureSplitter:
    """
    Utility to pre-split isometric tile textures into separate face textures.
    This can be run separately to pre-process all your tile textures.
    """
    def __init__(self, input_dir="assets/textures/tiles", output_dir="assets/textures/faces"):
        """
        Initialize the texture splitter.
        
        Args:
            input_dir: Directory containing source tile textures
            output_dir: Directory where split faces will be saved
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize pygame if not already initialized
        if not pygame.get_init():
            pygame.init()
    
    def split_texture(self, filename):
        """
        Split a single texture into top, left, and right faces.
        
        Args:
            filename: Name of the texture file to split
            top_height_ratio: Ratio of the texture height allocated to the top face
        
        Returns:
            Dictionary containing the three split face surfaces
        """
        # Load the texture
        full_path = os.path.join(self.input_dir, filename)
        tex = pygame.image.load(full_path).convert_alpha()
        w, h = tex.get_size()
        assert (w, h) == (32, 32), "This splitter expects 32×32 sprites"

        # Define the 4-pt polygons for each face, using coords:
        top_pts   = [(14, 0), (17, 0), (31, 7), (31, 8), (17, 15), (14, 15), (0, 8), (0,7)]
        right_pts = [(31, 9), (31, 24), (17, 31), (16, 31), (16, 16), (30, 9)]
        left_pts  = [(0,9), (1, 9), (15, 16), (15, 31), (14, 31), (0, 24)]

        faces = {}
        for name, pts in (("top", top_pts),
                          ("left", left_pts),
                          ("right", right_pts)):

            # Build an all-white mask for the polygon
            mask = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.polygon(mask, (255, 255, 255, 255), pts)

            # Copy & multiply by mask: outside poly → zero alpha
            face = tex.copy()
            face.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

            # Save out
            base = os.path.splitext(filename)[0]
            out_name = f"{base}_{name}.png"
            pygame.image.save(face, os.path.join(self.output_dir, out_name))

            faces[name] = face

        print(f"→ Split '{filename}' into: top, left, right")
        return faces
    
    def split_all_textures(self):
        """
        Process all texture files in the input directory.
        """
        # Get all PNG files in the input directory
        pngs = [f for f in os.listdir(self.input_dir) if f.lower().endswith(".png")]
        if not pngs:
            print(f"No PNGs in {self.input_dir}")
            return

        for fn in pngs:
            try:
                self.split_texture(fn)
            except Exception as e:
                print(f"Error on {fn}: {e}")

# If run as a standalone script, call pygame.init() and other
if __name__ == "__main__":
    # Start pygame
    pygame.init()
    pygame.display.set_mode((0, 0))
    
    # Can be run as a standalone script to pre-process textures
    input_dir = "assets/textures/tiles"
    output_dir = "assets/textures/faces"
    
    # Override directories if provided as arguments
    if len(sys.argv) > 1:
        input_dir = sys.argv[1]
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    
    splitter = TextureSplitter(input_dir, output_dir)
    splitter.split_all_textures()
    print("Texture splitting complete!")
    # End pygame
    pygame.quit()