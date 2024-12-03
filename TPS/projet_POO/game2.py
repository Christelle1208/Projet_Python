import pygame
import json
from tiles import Tile
from unit import Tank, Assassin, Marksman, Mage
from config import DEFAULT_CELL_SIZE, PLAYER1_IMAGES, PLAYER2_IMAGES
from bonus import Bonus  # Importation de la classe Bonus

class Game2:
    def __init__(self, screen):
        self.screen = screen
        self.hidden_lava = set()
        self.map = []
        self.cell_size = DEFAULT_CELL_SIZE
        self.current_turn = "player1"
        self.units = []
        self.current_unit_index = 0
        self.cursor_pos = (0, 0)
        self.ability_mode = None  # Tracks the currently selected ability
        self.bonuses = []  # Liste pour gérer les bonus sur la carte

        # Load map
        with open("assets/map1.json") as f:
            data = json.load(f)
            self.load_map(data)

        # Initialize units
        self.initialize_units()
        if not self.validate_map():
            raise ValueError("Invalid map: Fix the map and try again.")

        # Initialiser les bonus sur la carte
        self.generate_bonuses()

        self.start_turn()

    def load_map(self, data):
        """Charge la carte à partir du fichier JSON."""
        self.map = []
        for y, row in enumerate(data["map"]):
            map_row = []
            for x, tile in enumerate(row):
                map_row.append(Tile(x, y, tile, self.cell_size, self.hidden_lava))
            self.map.append(map_row)

    def initialize_units(self):
        """Initialise les unités pour chaque joueur."""
        self.player1_units = [Tank("Tank1", PLAYER1_IMAGES["tank"]),
                              Assassin("Assassin1", PLAYER1_IMAGES["assassin"]),
                              Marksman("Marksman1", PLAYER1_IMAGES["marksman"])]
        self.player2_units = [Tank("Tank2", PLAYER2_IMAGES["tank"]),
                              Assassin("Assassin2", PLAYER2_IMAGES["assassin"]),
                              Marksman("Marksman2", PLAYER2_IMAGES["marksman"])]

    def validate_map(self):
        """Vérifie si la carte est valide."""
        return len(self.map) > 0 and len(self.map[0]) > 0

    def start_turn(self):
        """Initialise le début d'un tour."""
        self.current_turn = "player1"

    def generate_bonuses(self):
        """Génère et place les bonus sur la carte."""
        # Exemple : placer 3 bonus sur la carte
        for _ in range(3):
            bonus = Bonus.generate_random_bonus((len(self.map), len(self.map[0])), self.cell_size)
            self.bonuses.append(bonus)

    def handle_player_turn(self, player):
        """Tour du joueur."""
        for selected_unit in self.player1_units if player == 1 else self.player2_units:

            # Calculer les cases accessibles pour l'unité sélectionnée
            selected_unit.is_selected = True
            selected_unit.accessible_tiles = selected_unit.get_accessible_tiles(move_range=selected_unit.range)  # Fixe les cases accessibles
            self.flip_display()  # Rafraîchit l'affichage avec les cases accessibles

            has_acted = False
            while not has_acted:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    # Gestion des clics de souris
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = event.pos
                        clicked_x, clicked_y = mouse_x // CELL_SIZE, mouse_y // CELL_SIZE

                        # Vérifier si le clic est sur une case accessible
                        if (clicked_x, clicked_y) in selected_unit.accessible_tiles:
                            selected_unit.x, selected_unit.y = clicked_x, clicked_y
                            has_acted = True
                            selected_unit.is_selected = False
                            selected_unit.accessible_tiles = []  # Effacer les cases accessibles après le déplacement
                            self.flip_display()  # Rafraîchir l'affichage

            # Vérifier si l'unité a collecté un bonus
            for bonus in self.bonuses:
                if bonus.x == selected_unit.x and bonus.y == selected_unit.y:
                    bonus.apply_bonus(selected_unit)
                    self.bonuses.remove(bonus)  # Supprimer le bonus après qu'il a été utilisé

    def flip_display(self):
        """Affiche le jeu."""

        # Efface l'écran
        self.screen.fill((0, 0, 0))

        # Affiche les cases accessibles pour l'unité sélectionnée
        for unit in self.player1_units + self.player2_units:
            if unit.accessible_tiles:  # Vérifie si l'unité a des cases accessibles stockées
                for tile_x, tile_y in unit.accessible_tiles:
                    rect = pygame.Rect(tile_x * self.cell_size, tile_y * self.cell_size, self.cell_size, self.cell_size)
                    pygame.draw.rect(self.screen, (50, 50, 200, 128), rect)  # Bleu pour les cases accessibles

        # Affiche la grille par-dessus
        for x in range(0, len(self.map[0]) * self.cell_size, self.cell_size):
            for y in range(0, len(self.map) * self.cell_size, self.cell_size):
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)  # Ligne blanche pour la grille

        # Affiche les unités
        for unit in self.player1_units + self.player2_units:
            unit.draw(self.screen)

        # Affiche les bonus
        for bonus in self.bonuses:
            bonus.draw(self.screen)

        # Rafraîchit l'écran
        pygame.display.flip()

def main():
    # Initialisation de Pygame
    pygame.init()

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Mon jeu de stratégie")

    # Instanciation du jeu (maintenant Game2)
    game = Game2(screen)

    # Boucle principale du jeu
    while True:
        game.handle_player_turn(1)  # Tour du joueur 1
        game.handle_player_turn(2)  # Tour du joueur 2

if __name__ == "__main__":
    main()
