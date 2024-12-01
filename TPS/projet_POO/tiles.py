import pygame
from config import GRASS_IMAGE_PATH, WATER_IMAGE_PATH, LAVA_IMAGE_PATH, SOIL_IMAGE_PATH
class Tile:
    def __init__(self, x, y, tile_type, cell_size, hidden_lava):
        self.x = x
        self.y = y
        self.tile_type = tile_type
        self.cell_size = cell_size
        self.is_hidden = (x, y) in hidden_lava  # Track if the tile is hidden lava
        self.is_smoke_covered = False

        # Load and scale images
        self.grass_image = pygame.image.load(GRASS_IMAGE_PATH)
        self.water_image = pygame.image.load(WATER_IMAGE_PATH)
        self.lava_image = pygame.image.load(LAVA_IMAGE_PATH)
        self.soil_image = pygame.image.load(SOIL_IMAGE_PATH)  # New soil image

        self.grass_image = pygame.transform.scale(self.grass_image, (self.cell_size, self.cell_size))
        self.water_image = pygame.transform.scale(self.water_image, (self.cell_size, self.cell_size))
        self.lava_image = pygame.transform.scale(self.lava_image, (self.cell_size, self.cell_size))
        self.soil_image = pygame.transform.scale(self.soil_image, (self.cell_size, self.cell_size))  # Scale soil

    def reveal(self):
        """Reveal the tile by setting it as no longer hidden."""
        self.is_hidden = False

    def draw(self, screen):
        """Draw the tile based on its type and hidden state."""
        x_pos = self.x * self.cell_size
        y_pos = self.y * self.cell_size

        # Draw grass if it's hidden lava
        if self.is_smoke_covered:  # Smoke 
            overlay_color = (128, 128, 128)  # Gray smoke color
            pygame.draw.rect(screen, overlay_color, (x_pos, y_pos, self.cell_size, self.cell_size))
        elif self.is_hidden and self.tile_type == "lava":
            screen.blit(self.grass_image, (x_pos, y_pos))
        elif self.tile_type == "water":
            screen.blit(self.water_image, (x_pos, y_pos))
        elif self.tile_type == "lava":
            screen.blit(self.lava_image, (x_pos, y_pos))
        elif self.tile_type == "soil":
            screen.blit(self.soil_image, (x_pos, y_pos))
        else:
            screen.blit(self.grass_image, (x_pos, y_pos))

