import pygame
import json
from game import Game
from config import *
from print_f import *
from positions import *
from menu import *

def main():
    map_choice = main_menu()
    if map_choice == 1:
        map_path = MAP1
    elif map_choice == 2:
        map_path = MAP2
    elif map_choice == 3:
        map_path = MAP3

    with open(map_path) as f:
        data = json.load(f)
        num_rows = len(data["layers"][0]["data"])
        num_columns = len(data["layers"][0]["data"][0]) if num_rows > 0 else 0

    width = num_columns * CELL_SIZE 
    height = num_rows * CELL_SIZE
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("projet poo")

    game = Game(screen,map_choice)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                game.handle_key(event.key)

        game.update()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
