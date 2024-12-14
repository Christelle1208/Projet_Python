import pygame
from config import *
class Tile:
    def __init__(self, x, y, tile_type, cell_size, hidden_mud):
        self.x = x
        self.y = y
        self.tile_type = tile_type
        self.cell_size = cell_size
        self.is_hidden = (x, y) in hidden_mud  # vérifie si le tile boue est chachée
        self.is_smoke_covered = False
        self.smoke_duration = 0

        self.grass_image = pygame.image.load(GRASS_IMAGE_PATH)
        self.water_image = pygame.image.load(WATER_IMAGE_PATH)
        self.mud_image = pygame.image.load(MUD_IMAGE_PATH) 
        self.soil_image = pygame.image.load(SOIL_IMAGE_PATH)
        self.rock1_image = pygame.image.load(ROCK1_IMAGE_PATH)
        self.rock2_image = pygame.image.load(ROCK2_IMAGE_PATH)
        self.rock3_image = pygame.image.load(ROCK3_IMAGE_PATH)
        self.dead_soil_image = pygame.image.load(DEAD_SOIL)
        self.dead_grass_image = pygame.image.load(DEAD_GRASS)

        self.grass_image = pygame.transform.scale(self.grass_image, (self.cell_size, self.cell_size))
        self.water_image = pygame.transform.scale(self.water_image, (self.cell_size, self.cell_size))
        self.mud_image = pygame.transform.scale(self.mud_image, (self.cell_size, self.cell_size))
        self.soil_image = pygame.transform.scale(self.soil_image, (self.cell_size, self.cell_size))  
        self.rock1_image = pygame.transform.scale(self.rock1_image, (self.cell_size, self.cell_size))
        self.rock2_image = pygame.transform.scale(self.rock2_image, (self.cell_size, self.cell_size))
        self.rock3_image = pygame.transform.scale(self.rock3_image, (self.cell_size, self.cell_size))
        self.dead_grass_image = pygame.transform.scale(self.dead_grass_image, (self.cell_size, self.cell_size))
        self.dead_soil_image = pygame.transform.scale(self.dead_soil_image, (self.cell_size, self.cell_size))

    def reveal(self):
        """révéle si la tile en la définissant comme no hidden."""
        self.is_hidden = False

    def draw(self, screen):
        """dessine la tile selon son type et sa visibilité."""
        x_pos = self.x * self.cell_size
        y_pos = self.y * self.cell_size

        # mettre herbe tant que la boue est cachée
        if self.is_smoke_covered:
            overlay_color = (128, 128, 128) 
            pygame.draw.rect(screen, overlay_color, (x_pos, y_pos, self.cell_size, self.cell_size))
        elif self.is_hidden and self.tile_type == "mud":
            screen.blit(self.grass_image, (x_pos, y_pos))
        elif self.tile_type == "water":
            screen.blit(self.water_image, (x_pos, y_pos))
        elif self.tile_type == "mud":
            screen.blit(self.mud_image, (x_pos, y_pos))
        elif self.tile_type == "soil":
            screen.blit(self.soil_image, (x_pos, y_pos))
        elif self.tile_type == "wall":
            if (self.x,self.y) in ((0,0),(20,20),(0,20),(20,0)):
                screen.blit(self.rock2_image, (x_pos, y_pos))
            else:
                screen.blit(self.rock1_image, (x_pos, y_pos))
        elif self.tile_type == "rock":
            screen.blit(self.rock3_image, (x_pos, y_pos))
        elif self.tile_type == "dead_grass":
            screen.blit(self.dead_grass_image, (x_pos, y_pos))
        elif self.tile_type == "dead_soil":
            screen.blit(self.dead_soil_image, (x_pos, y_pos))
        else:
            screen.blit(self.grass_image, (x_pos, y_pos))

