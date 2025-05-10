import pygame

class DebugOverlay:
    """
    Debug overlay that displays information about chunks, player position, etc.
    """
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.font = pygame.font.SysFont(None, 24)
        self.enabled = True
        self.show_chunk_borders = True
        
    def toggle(self):
        """Toggle debug overlay on/off"""
        self.enabled = not self.enabled
        
    def toggle_chunk_borders(self):
        """Toggle chunk border display"""
        self.show_chunk_borders = not self.show_chunk_borders
        
    def draw(self, world, player, camera_group):
        """Draw debug information"""
        if not self.enabled:
            return
            
        # Get player position in world coordinates
        player_iso_x, player_iso_y = player.rect.center
        grid_x, grid_y = world.chunk_manager.tile_renderer.iso_to_cart(player_iso_x, player_iso_y)
        
        # Get chunk position
        chunk_x, chunk_y = world.chunk_manager.get_chunk_pos_for_world_pos(int(grid_x), int(grid_y))
        
        # FPS
        fps = self.clock.get_fps() 
        
        # Debug text
        debug_info = [
            f"FPS: {fps:.1f}",
            f"Player ISO: ({player_iso_x}, {player_iso_y})",
            f"Player Grid: ({grid_x:.1f}, {grid_y:.1f})",
            f"Chunk: ({chunk_x}, {chunk_y})",
            f"Loaded Chunks: {len(world.chunk_manager.chunks)}",
            f"Zoom: {camera_group.zoom:.1f}",
            f"Sprites: {len(camera_group.sprites())}"
        ]
        
        # Draw text
        y_offset = 10
        for info in debug_info:
            text_surface = self.font.render(info, True, (255, 255, 255))
            self.screen.blit(text_surface, (10, y_offset))
            y_offset += 25
            
        # Draw chunk borders if enabled
        if self.show_chunk_borders:
            self._draw_chunk_borders(world, camera_group)
    
    def _draw_chunk_borders(self, world, camera_group):
        """Draw borders around chunks for debugging"""
        chunk_size = world.chunk_manager.chunk_size
        tile_renderer = world.chunk_manager.tile_renderer
        
        # Draw borders for each loaded chunk
        for chunk_pos, chunk in world.chunk_manager.chunks.items():
            chunk_x, chunk_y = chunk_pos
            
            # Get corners of the chunk in world coordinates
            corners = [
                (chunk_x * chunk_size, chunk_y * chunk_size),  # Top-left
                ((chunk_x + 1) * chunk_size, chunk_y * chunk_size),  # Top-right
                ((chunk_x + 1) * chunk_size, (chunk_y + 1) * chunk_size),  # Bottom-right
                (chunk_x * chunk_size, (chunk_y + 1) * chunk_size)  # Bottom-left
            ]
            
            # Convert corners to screen coordinates
            screen_corners = []
            for x, y in corners:
                iso_x, iso_y = tile_renderer.cart_to_iso(x, y)
                # Apply camera offset and zoom
                screen_x = (iso_x * camera_group.zoom) - camera_group.offset.x
                screen_y = (iso_y * camera_group.zoom) - camera_group.offset.y
                screen_corners.append((screen_x, screen_y))
            
            # Draw lines connecting corners
            for i in range(4):
                start = screen_corners[i]
                end = screen_corners[(i + 1) % 4]
                pygame.draw.line(self.screen, (255, 0, 0), start, end, 2)