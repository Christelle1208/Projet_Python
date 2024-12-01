import pygame
from config import CELL_SIZE, GREEN, GRID_SIZE  

class Unit2:
    def __init__(self, name, hp, attack, defense, range, image_path, x=0, y=0, team=None):
        """
        Initialise une unité avec ses attributs.
        
        :param name: Nom de l'unité (ex: "Tank", "Assassin", etc.)
        :param hp: Points de vie de l'unité
        :param attack: Puissance d'attaque de l'unité
        :param defense: Défense de l'unité
        :param range: Portée de mouvement de l'unité
        :param image_path: Chemin de l'image pour l'unité
        :param x: Position x de l'unité sur la grille
        :param y: Position y de l'unité sur la grille
        :param team: Équipe de l'unité (ex: "player", "enemy")
        """
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.range = range
        self.has_acted = False
        self.x = x
        self.y = y
        self.team = team
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE)) 
        self.is_visible = True 
        self.is_selected = False 

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            damage = max(0, self.attack - target.defense) 
            target.hp -= damage
            print(f"{self.name} attaque {target.name} et lui inflige {damage} dégâts.")
        else:
            print(f"{self.name} ne peut pas attaquer {target.name} (trop loin).")

    def get_accessible_tiles(self, move_range):
        """Retourne les cases accessibles pour cette unité en fonction de son mouvement."""
        tiles = []
        for dx in range(-move_range, move_range + 1):
            for dy in range(-move_range, move_range + 1):
                if abs(dx) + abs(dy) <= move_range:  
                    new_x, new_y = self.x + dx, self.y + dy
                    if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE: 
                        tiles.append((new_x, new_y))
        return tiles

    def draw(self, screen):
        """Dessine l'unité sur l'écran."""
        match self.name:
            case 'Tank':
                color = (0, 100, 200)  
            case 'Assassin':
                color = (255, 0, 0)  
            case 'Mage':
                color = (225, 105, 160)  
            case 'Marksman':
                color = (255, 255, 0)  
            case _:
                color = (150, 150, 150) 

       
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        center_x, center_y = self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2
        if self.team == 'player':
            
            pygame.draw.circle(screen, color, (center_x, center_y), CELL_SIZE // 3)
        else:
           
            points = [
                (center_x, center_y - CELL_SIZE // 3),  
                (center_x - CELL_SIZE // 3, center_y + CELL_SIZE // 3),  
                (center_x + CELL_SIZE // 3, center_y + CELL_SIZE // 3) 
            ]
            pygame.draw.polygon(screen, color, points)
