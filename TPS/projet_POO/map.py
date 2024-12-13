import pygame
import json
from config import CELL_SIZE

class Map:
    def __init__(self, map_path):
        self.map_data = self.load_map(map_path)
        self.tileset = self.map_data["layers"][0]["tileset"]
        self.grid = self.map_data["layers"][0]["data"]
        self.num_rows = len(self.grid)
        self.num_columns = len(self.grid[0]) if self.num_rows > 0 else 0
        self.width = self.num_columns * CELL_SIZE
        self.height = self.num_rows * CELL_SIZE

    def load_map(self, map_path):
        with open(map_path, "r") as f:
            return json.load(f)

    def draw(self, screen):
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                if tile == 1:
                    color = (139, 69, 19)  # Couleur pour les murs
                elif tile == 0:
                    color = (211, 211, 211)  # Couleur pour le sol
                elif tile == 2:
                    color = (0, 255, 0)  # Position de départ du joueur
                elif tile == 3:
                    color = (255, 0, 0)  # Ennemi
                else:
                    color = (0, 0, 0) # noir

                # Dessiner chaque tuile
                pygame.draw.rect(
                    screen,
                    color,
                    pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )

    def is_walkable(self, x, y):
        if 0 <= y < self.num_rows and 0 <= x < self.num_columns:
            tile = self.grid[y][x]
            return tile in [0, 2, 3]  # Sol ou case accessible
        return False

    def get_player_start(self):
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                if tile == 2:
                    return x, y
        return None  
