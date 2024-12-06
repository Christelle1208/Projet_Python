import pygame
import json
from tiles import Tile
from unit import Tank, Assassin, Marksman, Mage
from bonus import Bonus
from config import DEFAULT_CELL_SIZE, PLAYER1_IMAGES, PLAYER2_IMAGES
class Game:
    def __init__(self, screen):
        """
        Construit le jeu avec la surface de la fenêtre.

        Paramètres
        ----------
        screen : pygame.Surface
            La surface de la fenêtre du jeu.
        """
        self.screen = screen
        self.hidden_lava = set()
        self.map = []
        self.cell_size = DEFAULT_CELL_SIZE
        self.current_turn = "player1"
        self.units = []
        self.current_unit_index = 0
        self.cursor_pos = (0, 0)
        self.ability_mode = None  # Tracks the currently selected ability

        # Load map
        with open("assets/map1.json") as f:
            data = json.load(f)
            self.load_map(data)

        # Initialize units
        self.initialize_units()
        if not self.validate_map():
            raise ValueError("Invalid map: Fix the map and try again.")

        self.start_turn()

         # Créer une liste pour les bonus
        self.bonuses = []
        self.occupied_positions = set()

        # Générer des bonus sur la carte
        for _ in range(3):  # Exemple de générer 3 bonus
            bonus = Bonus.generate_random_bonus(map_size=(8, 8), cell_size=self.cell_size, occupied_positions=self.occupied_positions)
            self.bonuses.append(bonus)
            self.occupied_positions.add((bonus.x, bonus.y))

        self.start_turn()


        def generate_positions(rows):
            """Génère trois positions aléatoires dans des lignes définies."""
            positions = set()  # Utiliser un set pour éviter les doublons
            while len(positions) < 3:
                x = random.choice(rows)  # Ligne autorisée
                y = random.randint(0, GRID_SIZE - 1)  # Colonne aléatoire
                positions.add((x, y))
            return list(positions)

        self.screen = screen
        print("Types : Tank, Assassin, Mage, Marksman")
        type_joueur,team=["","",""],'player'
        player1_pos = generate_positions(rows=[0, 1])
        for i in range(3):
            type_joueur[i]=str(input(f"Joueur 1 : Choisissez un type de personnage pour l'unité {i+1}: "))
        self.player_units = [Personnage(type_joueur[0],player1_pos[0],team).character(),
                             Personnage(type_joueur[1],player1_pos[1],team).character(),
                             Personnage(type_joueur[2],player1_pos[2],team).character()]
        
        x,y=random.randint(1,7),random.randint(1,7)
        type_ennemi,team=["","",""],'enemy'
        player2_pos = generate_positions(rows=[6, 7])
        for i in range(3):
            type_ennemi[i]=str(input(f"Joueur 2 : Choisissez un type de personnage pour l'unité {i+1}: "))
        self.enemy_units = [Personnage(type_ennemi[0],player2_pos[0],team).character(),
                            Personnage(type_ennemi[1],player2_pos[1],team).character(),
                            Personnage(type_ennemi[2],player2_pos[2],team).character()]
        
    def handle_player_turn(self, player):
        """Tour du joueur."""
        for selected_unit in self.player_units if player == 1 else self.enemy_units:

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
                        clicked_x, clicked_y = mouse_x // self.cell_size, mouse_y // self.cell_size

                        # Vérifier si le clic est sur une case accessible
                        if (clicked_x, clicked_y) in selected_unit.accessible_tiles:
                            selected_unit.x, selected_unit.y = clicked_x, clicked_y
                            has_acted = True
                            selected_unit.is_selected = False
                            selected_unit.accessible_tiles = []  # Effacer les cases accessibles après le déplacement
                            self.flip_display()  # Rafraîchir l'affichage

                            # Vérifier si une unité a collecté un bonus
                            for bonus in self.bonuses:
                                if (selected_unit.x, selected_unit.y) == (bonus.x, bonus.y):
                                    bonus.apply_bonus(selected_unit)
                                    self.bonuses.remove(bonus)  # Retirer le bonus collecté

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
        # Affiche les bonus
        for bonus in self.bonuses:
            bonus.draw(self.screen)
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
