from map import Map
import pygame
import json
from game import Game
from config import CELL_SIZE, MAP1, MAP2, MAP3
from print_f import *
from positions import *
from menu import *



def main():
    pygame.init()

    # Choisir une map
    map_choice = main_menu()  
    if map_choice == 1:
        map_path = MAP1
    elif map_choice == 2:
        map_path = MAP2
    elif map_choice == 3:
        map_path = MAP3

    # Chargement de la carte
    game_map = Map(map_path)

    # Initialisation
    screen = pygame.display.set_mode((game_map.width, game_map.height))
    pygame.display.set_caption("Projet POO - Jeu 2D")

    player_position = game_map.get_player_start()
    if not player_position:
        raise ValueError("Aucune position de départ trouvée sur la carte")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))  
        game_map.draw(screen)

        # Afficher le joueur
        px, py = player_position
        pygame.draw.rect(
            screen,
            (0, 255, 0),  # Couleur du joueur
            pygame.Rect(px * CELL_SIZE, py * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        )

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
