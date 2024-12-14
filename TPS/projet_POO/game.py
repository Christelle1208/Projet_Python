import pygame
import json
import random
from tiles import Tile
from characters import * 
from abilities import *
from config import *
from equipements import *
from print_f import *
from positions import *
from menu import *

class Game:
    def __init__(self, screen, map_choice):
        
        self.screen = screen
        self.hidden_mud = set()
        self.map = []
        self.cell_size = CELL_SIZE
        self.current_turn = "player1"
        self.units = []
        self.current_unit_index = 0
        self.cursor_pos = (1, 1)
        self.ability_mode = None 
        self.affected_tiles = []
        self.player1_cooldowns = {"Bomb": 2, "Sniper": 2, "Smoke": 0, "Heal": 2}
        self.player2_cooldowns = {"Bomb": 2, "Sniper": 2, "Smoke": 0, "Heal": 2}
        self.cursor_alpha = 0 
        self.cursor_alpha_direction = 1  


        with open(f"assets/map{map_choice}.json") as f:
            data = json.load(f)
            self.load_map(data)

        self.initialize_units()
        self.spawn_equipment()
        self.start_turn()

        
    def initialize_units(self):
        """initialisation des joueurs sur la map"""

        player1_start_positions,player2_start_positions = [],[]
        for i in range(4):
            player1_start_positions.append(random_position(PLAYER1_ROW,PLAYER1_COLUMN,player1_start_positions))
            player2_start_positions.append(random_position(PLAYER2_ROW,PLAYER2_COLUMN,player2_start_positions))
        
        self.units = [
            Tank("Tank", PLAYER1_IMAGES["T"]), Assassin("Assassin", PLAYER1_IMAGES["A"]),
            archer("archer", PLAYER1_IMAGES["M"]), Mage("Mage", PLAYER1_IMAGES["G"]),
            Tank("Tank", PLAYER2_IMAGES["T"]), Assassin("Assassin", PLAYER2_IMAGES["A"]),
            archer("archer", PLAYER2_IMAGES["M"]), Mage("Mage", PLAYER2_IMAGES["G"])
        ]

        for i, unit in enumerate(self.units):
            if i < 4: 
                unit.team = "player1"
                unit.x, unit.y = player1_start_positions[i]
            else:  
                unit.team = "player2"
                unit.x, unit.y = player2_start_positions[i - 4]
            unit.set_game(self)




        

        def generate_positions(rows):
            """Génère trois positions aléatoires dans des lignes définies."""
            positions = set()  # Utiliser un set pour éviter les doublons
            while len(positions) < 3:
                x = random.choice(rows)  # Ligne autorisée
                y = random.randint(0, GRID_SIZE - 1)  # Colonne aléatoire
                positions.add((x, y))
            return list(positions)


        self.screen = screen
        print("Types : Tank, Assassin, Mage, Archer_poison, Archer_electricite")
        type_joueur,team=["","",""],'player'
        player1_pos = generate_positions(rows=[0, 1])
        for i in range(3):
            type_joueur[i]=str(input(f"Joueur 1 : Choisissez un type de personnage pour l'unité {i+1}: "))
        self.player_units = [Personnage(type_joueur[0],team,player1_pos[0]).character(),
                             Personnage(type_joueur[1],team,player1_pos[1]).character(),
                             Personnage(type_joueur[2],team,player1_pos[2]).character()]
        
        x,y=random.randint(1,7),random.randint(1,7)
        type_ennemi,team=["","",""],'enemy'
        player2_pos = generate_positions(rows=[6, 7])
        for i in range(3):
            type_ennemi[i]=str(input(f"Joueur 2 : Choisissez un type de personnage pour l'unité {i+1}: "))
        self.enemy_units = [Personnage(type_ennemi[0],team,player2_pos[0]).character(),
                            Personnage(type_ennemi[1],team,player2_pos[1]).character(),
                            Personnage(type_ennemi[2],team,player2_pos[2]).character()]

    
    def flip_display(self):
        """Affiche le jeu."""

        # Efface l'écran
        self.screen.fill(BLACK)

        # Affiche les cases accessibles pour l'unité sélectionnée
        for unit in self.player_units + self.enemy_units:
            if unit.accessible_tiles:  # Vérifie si l'unité a des cases accessibles stockées
                for tile_x, tile_y in unit.accessible_tiles:
                    rect = pygame.Rect(tile_x * CELL_SIZE, tile_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, (50, 50, 200,128), rect)  # Bleu pour les cases accessibles

        # Affiche la grille par-dessus
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)  # Ligne blanche pour la grille

        # Affiche les unités
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

        # Rafraîchit l'écran
        pygame.display.flip()



def main():

    # Initialisation de Pygame
    pygame.init()

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")

    # Instanciation du jeu
    game = Game(screen)

    # Boucle principale du jeu
    while True:
        game.handle_player_turn(1) # Tour du joueur 1
        game.handle_player_turn(2) # Tour du joueur 2


if __name__ == "__main__":
    main()
