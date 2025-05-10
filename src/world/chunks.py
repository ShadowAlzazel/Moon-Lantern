import pygame
from typing import Dict, Tuple, Set, List
from sprites import Tile
from settings import LAYERS
from world.tiles import TileRenderer
from world.noise import NoiseGenerator

class Chunk:
    """
    Represents a square chunk of the world grid.
    """
    def __init__(self, chunk_pos: Tuple[int, int], chunk_size: int, tile_renderer: TileRenderer, 
                 noise_gen: NoiseGenerator, groups: pygame.sprite.Group):
        # Chunk position in chunk coordinates (not tile coordinates)
        self.chunk_x, self.chunk_y = chunk_pos
        self.chunk_size = chunk_size
        self.tile_renderer = tile_renderer
        self.noise_gen = noise_gen
        self.groups = groups
        
        # Store all tiles in this chunk
        self.tiles: Dict[Tuple[int, int], Tile] = {}
        
        # Track if this chunk has been generated
        self.is_generated = False
        
        # Tile set mapping
        self.tile_set_mapping = {
            "grass_block": "grass_block",
            "red_grass_block": "red_grass_block",
            # Add more tile types here
        }
        
    def world_to_chunk_coords(self, world_x: int, world_y: int) -> Tuple[int, int]:
        """Convert world coordinates to local chunk coordinates."""
        local_x = world_x - (self.chunk_x * self.chunk_size)
        local_y = world_y - (self.chunk_y * self.chunk_size)
        return local_x, local_y
        
    def chunk_to_world_coords(self, local_x: int, local_y: int) -> Tuple[int, int]:
        """Convert local chunk coordinates to world coordinates."""
        world_x = local_x + (self.chunk_x * self.chunk_size)
        world_y = local_y + (self.chunk_y * self.chunk_size)
        return world_x, world_y
    
    def get_tile_at(self, world_x: int, world_y: int) -> Tile:
        """Get tile at the specified world coordinates."""
        return self.tiles.get((world_x, world_y))
    
    def generate(self):
        """Generate all tiles for this chunk using noise."""
        if self.is_generated:
            return
        # First pass - create all tiles but don't add faces yet
        for local_y in range(self.chunk_size):
            for local_x in range(self.chunk_size):
                # Convert to world coordinates
                world_x, world_y = self.chunk_to_world_coords(local_x, local_y)
                # Get tile type based on noise
                tile_type = self.noise_gen.get_tile_type(world_x, world_y)
                # Calculate isometric position
                iso_x, iso_y = self.tile_renderer.cart_to_iso(world_x, world_y)
                # Create the tile
                new_tile = Tile(
                    pos=(iso_x, iso_y),
                    groups=self.groups,
                    zlayer=LAYERS['ground'],
                    grid_pos=(world_x, world_y),
                    tile_type=tile_type
                )
                # Store the tile
                self.tiles[(world_x, world_y)] = new_tile
        
        
        # Now during second pass - add faces while checking adjacent chunks
        for world_pos, tile in self.tiles.items():
            world_x, world_y = world_pos
            
            # Create top face for all tiles
            self.tile_renderer.create_face(tile, 'top', tile.tile_type)
            
            # Check if we need side faces - this needs to check both within this chunk AND in adjacent chunks
            # East neighbor
            east_pos = (world_x + 1, world_y)
            east_neighbor = self.tiles.get(east_pos)
            
            # If no east neighbor in this chunk, check if there's a tile in an adjacent chunk
            if east_neighbor is None:
                # This position might be in a neighboring chunk
                east_chunk_pos = self.get_chunk_pos_for_world_pos(east_pos[0], east_pos[1])
                
                # Only add the face if there's definitely no tile there
                if not self.tile_exists_at_world_pos(east_pos[0], east_pos[1]):
                    self.tile_renderer.create_face(tile, 'right', tile.tile_type)
            
            # South neighbor - same logic
            south_pos = (world_x, world_y + 1)
            south_neighbor = self.tiles.get(south_pos)
            
            if south_neighbor is None:
                # This position might be in a neighboring chunk
                south_chunk_pos = self.get_chunk_pos_for_world_pos(south_pos[0], south_pos[1])
                
                # Only add the face if there's definitely no tile there 
                if not self.tile_exists_at_world_pos(south_pos[0], south_pos[1]):
                    self.tile_renderer.create_face(tile, 'left', tile.tile_type)
                
        self.is_generated = True
    
    def get_chunk_pos_for_world_pos(self, world_x, world_y):
        """Get the chunk coordinates that would contain the given world position."""
        chunk_x = world_x // self.chunk_size
        chunk_y = world_y // self.chunk_size
        return chunk_x, chunk_y
        
    def tile_exists_at_world_pos(self, world_x, world_y):
        """Check if a tile exists at the specified world position, including in other chunks."""
        # First check within this chunk
        if (world_x, world_y) in self.tiles:
            return True
            
        # Not in this chunk, so it would be in another chunk
        # But we don't have direct access to other chunks here
        # Instead, we'll use a clever trick for chunk border logic
        
        # If this position is exactly on a chunk boundary, assume it exists
        # This prevents creating side faces at chunk boundaries
        chunk_x, chunk_y = self.get_chunk_pos_for_world_pos(world_x, world_y)
        
        # If it's a different chunk than this one
        if chunk_x != self.chunk_x or chunk_y != self.chunk_y:
            # Calculate the closest edge of that chunk
            chunk_edge_x = chunk_x * self.chunk_size
            chunk_edge_y = chunk_y * self.chunk_size
            
            # If this is exactly on the edge of a chunk, 
            # assume there is a tile there to prevent visible seams
            if world_x == chunk_edge_x or world_y == chunk_edge_y:
                return True
            
            # For positions inside other chunks, use noise to determine if a tile would exist there
            # This ensures consistency across chunk boundaries
            return self.noise_gen.get_tile_type(world_x, world_y) != None
            
        return False
    
    def update_faces(self, chunk_manager):
        """
        Update tile faces based on neighboring tiles (including those in adjacent chunks).
        This should be called after all chunks in the view distance are generated.
        """
        for world_pos, tile in self.tiles.items():
            world_x, world_y = world_pos
            
            # First, remove any existing faces to prevent duplicates
            for face_type, face in list(tile.faces.items()):
                if face:
                    face.kill()
                    tile.faces[face_type] = None
            
            # Create top face for all tiles
            self.tile_renderer.create_face(tile, 'top', tile.tile_type)
            
            # Check if we need side faces by checking if neighbors exist
            # East neighbor - Could be in this chunk or adjacent chunk
            east_neighbor = self.tiles.get((world_x + 1, world_y))
            if not east_neighbor:
                # Check if it's in another chunk
                east_neighbor = chunk_manager.get_tile_at(world_x + 1, world_y)
            
            if not east_neighbor:
                self.tile_renderer.create_face(tile, 'right', tile.tile_type)
            
            # South neighbor - Could be in this chunk or adjacent chunk
            south_neighbor = self.tiles.get((world_x, world_y + 1))
            if not south_neighbor:
                # Check if it's in another chunk
                south_neighbor = chunk_manager.get_tile_at(world_x, world_y + 1)
                
            if not south_neighbor:
                self.tile_renderer.create_face(tile, 'left', tile.tile_type)
    
    def unload(self):
        """Remove all tiles in this chunk from the game."""
        for tile in self.tiles.values():
            # Remove all faces
            for face in tile.faces.values():
                if face:
                    face.kill()
            # Remove the tile itself
            tile.kill()
        
        # Clear the tiles dictionary
        self.tiles.clear()
        self.is_generated = False


class ChunkManager:
    """
    Handles loading and unloading chunks around the player.
    """
    def __init__(self, groups: pygame.sprite.Group, seed=None):
        self.groups = groups
        self.chunk_size = 8  # Size of each chunk in tiles (reduced from 16)
        self.render_distance = 2  # How many chunks to render in each direction
        
        # Create tile renderer and noise generator
        self.tile_renderer = TileRenderer(groups=groups)
        self.noise_gen = NoiseGenerator(seed=seed)
        
        # Store loaded chunks
        self.chunks: Dict[Tuple[int, int], Chunk] = {}
        
        # Track the last player chunk for chunk loading/unloading
        self.last_player_chunk = None
    
    def get_chunk_pos_for_world_pos(self, world_x: int, world_y: int) -> Tuple[int, int]:
        """Get the chunk coordinates containing the given world position."""
        chunk_x = world_x // self.chunk_size
        chunk_y = world_y // self.chunk_size
        return chunk_x, chunk_y
    
    def get_tile_at(self, world_x: int, world_y: int) -> Tile:
        """Get the tile at the specified world coordinates."""
        chunk_pos = self.get_chunk_pos_for_world_pos(world_x, world_y)
        
        # Get or create the chunk
        if chunk_pos in self.chunks:
            chunk = self.chunks[chunk_pos]
            return chunk.get_tile_at(world_x, world_y)
        return None
        
    def check_tile_at(self, world_x: int, world_y: int) -> bool:
        """Check if a tile exists at the specified world coordinates without loading chunks."""
        chunk_pos = self.get_chunk_pos_for_world_pos(world_x, world_y)
        
        # If chunk is loaded, check the actual tile
        if chunk_pos in self.chunks:
            chunk = self.chunks[chunk_pos]
            return (world_x, world_y) in chunk.tiles
        
        # If chunk isn't loaded, use noise to predict if a tile would exist there
        # This ensures consistent chunk borders
        return self.noise_gen.get_tile_type(world_x, world_y) != None
    
    def update_chunks(self, player_pos: Tuple[int, int]):
        """Update loaded chunks based on player position."""
        # Convert player's isometric position to approximate world coordinates
        player_iso_x, player_iso_y = player_pos
        
        # Use the tile renderer to convert isometric to cartesian
        # This gives us more accurate world coordinates for the player
        grid_x, grid_y = self.tile_renderer.iso_to_cart(player_iso_x, player_iso_y)
        player_world_x, player_world_y = int(grid_x), int(grid_y)
        
        # Get chunk position
        player_chunk_pos = self.get_chunk_pos_for_world_pos(player_world_x, player_world_y)
        
        # If player hasn't moved to a new chunk, no need to update
        if player_chunk_pos == self.last_player_chunk:
            return
            
        self.last_player_chunk = player_chunk_pos
        
        # Determine which chunks should be loaded
        chunks_to_load = set()
        player_chunk_x, player_chunk_y = player_chunk_pos
        
        for dy in range(-self.render_distance, self.render_distance + 1):
            for dx in range(-self.render_distance, self.render_distance + 1):
                chunk_pos = (player_chunk_x + dx, player_chunk_y + dy)
                chunks_to_load.add(chunk_pos)
        
        # Determine which chunks to unload
        chunks_to_unload = set(self.chunks.keys()) - chunks_to_load
        
        # First load new chunks at chunk boundaries
        # This ensures borders are generated properly with knowledge of neighboring chunks
        border_chunks = []
        new_inner_chunks = []
        
        for chunk_pos in chunks_to_load:
            if chunk_pos not in self.chunks:
                # Check if this is a border chunk (has neighbors)
                is_border = False
                for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                    neighbor_pos = (chunk_pos[0] + dx, chunk_pos[1] + dy)
                    if neighbor_pos in self.chunks:
                        is_border = True
                        break
                
                # Sort chunks so borders are generated first
                if is_border:
                    border_chunks.append(chunk_pos)
                else:
                    new_inner_chunks.append(chunk_pos)
        
        # First create all the chunks without generating them
        for chunk_pos in border_chunks + new_inner_chunks:
            if chunk_pos not in self.chunks:
                new_chunk = Chunk(
                    chunk_pos=chunk_pos,
                    chunk_size=self.chunk_size,
                    tile_renderer=self.tile_renderer,
                    noise_gen=self.noise_gen,
                    groups=self.groups
                )
                self.chunks[chunk_pos] = new_chunk
        
        # Now generate all the chunks
        for chunk_pos in border_chunks + new_inner_chunks:
            self.chunks[chunk_pos].generate()
        
        # update faces on *all* loaded chunks
        for chunk in self.chunks.values():
            chunk.update_faces(self)
        
        # Unload chunks after loading new ones to avoid flickering at borders
        for chunk_pos in chunks_to_unload:
            if chunk_pos in self.chunks:
                self.chunks[chunk_pos].unload()
                del self.chunks[chunk_pos]