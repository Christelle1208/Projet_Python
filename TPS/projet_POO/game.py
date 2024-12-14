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


 
    def load_map(self, data):
            """chargement des tiles"""
            num_rows = len(data["layers"][0]["data"])
            num_columns = len(data["layers"][0]["data"][0]) if num_rows > 0 else 0
            self.cell_size = min(self.screen.get_width() // num_columns, self.screen.get_height() // num_rows)
    
    
            for y, row in enumerate(data["layers"][0]["data"]):
                for x, tile_id in enumerate(row):
                    if tile_id == 3:  # BOUE
                        self.hidden_mud.add((x, y))
    
            
            for y, row in enumerate(data["layers"][0]["data"]):
                tile_row = []
                for x, tile_id in enumerate(row):
                    tile_type = (
                    "wall" if tile_id == 0 else
                    "grass" if tile_id == 1 else
                    "water" if tile_id == 2 else
                    "mud" if tile_id == 3 else
                    "soil" if tile_id == 4 else
                    "rock" if tile_id == 5 else
                    "grass"
                    )
                    tile = Tile(x, y, tile_type, self.cell_size, self.hidden_mud)
                    tile_row.append(tile)
                self.map.append(tile_row)

    def start_turn(self):
        """Reset les unités pour le nouveau tour"""
        for unit in self.units:
            if unit.team == self.current_turn:
                unit.has_acted = False
        self.update_visibility()
        self.current_unit_index = 0
        self.select_next_unit()
        
        

    def select_next_unit(self):
        self.update_visibility()
        """sélectionne les unités suivantes"""
        if self.check_game_over():
                return
        player_units = [unit for unit in self.units if unit.team == self.current_turn and not unit.has_acted]
        if player_units:
            self.selected_unit = player_units[self.current_unit_index % len(player_units)]
            self.selected_unit.is_selected = True
            self.cursor_pos = (self.selected_unit.x, self.selected_unit.y)
        else:
            self.switch_turn()

            
    def decrement_cooldowns(self):
        """décrémentation du temps d'attente."""
        cooldowns = self.player1_cooldowns if self.current_turn == "player1" else self.player2_cooldowns
        for ability in cooldowns:
            if cooldowns[ability] > 0:
                cooldowns[ability] -= 1
                
                

    def switch_turn(self):
        """Change le tour des joueurs."""
        self.expire_smoke()
        self.decrement_cooldowns()
        self.current_turn = "player2" if self.current_turn == "player1" else "player1"
        print_f(f"Au tour de {self.current_turn}")
        self.start_turn()
        

    def draw_abilities(self):
        font = pygame.font.Font(None, 24)
        
        cooldowns = self.player1_cooldowns if self.current_turn == "player1" else self.player2_cooldowns
        
        ability_texts = [
            f"1: Bomb ({cooldowns['Bomb']}R)" if cooldowns["Bomb"] > 0 else "1: Bomb",
            f"2: Sniper ({cooldowns['Sniper']}R)" if cooldowns["Sniper"] > 0 else "2: Sniper",
            f"3: Smoke ({cooldowns['Smoke']}R)" if cooldowns["Smoke"] > 0 else "3: Smoke",
            f"4: Heal ({cooldowns['Heal']}R)" if cooldowns["Heal"] > 0 else "4: Heal"
        ]
        
        x_cooldowns_pos = 10
        y_cooldowns_pos = 5  
        
        for text in ability_texts:
        
            color = (255, 0, 0) if "R" in text else (255, 255, 255)
            rendered_text = font.render(text, True, color)
            self.screen.blit(rendered_text, (x_cooldowns_pos, y_cooldowns_pos))
            x_cooldowns_pos += 120 


    def expire_smoke(self):
        for row in self.map:
            for tile in row:
                if tile.is_smoke_covered:
                    tile.smoke_duration -= 1
                    if tile.smoke_duration <= 0:
                        tile.is_smoke_covered = False
                        
                        
    def add_affected_tiles(self, tiles, color):
        """ajout des tiles afféctées par une habilité."""
        self.affected_tiles = [(x, y, color) for x, y in tiles]
        
    
    def clear_affected_tiles(self):
        """supprime les tiles affectées."""
        self.affected_tiles = []
            
    def update(self):
        """maj visuel du jeu."""
        for row in self.map:
            for tile in row:
                tile.draw(self.screen)

        if self.selected_unit:
            for dx in range(-self.selected_unit.range - 1, self.selected_unit.range + 2):
                for dy in range(-self.selected_unit.range - 1, self.selected_unit.range + 2):
                    x, y = self.selected_unit.x + dx, self.selected_unit.y + dy
                    if self.can_move_to(self.selected_unit, x, y):
                        target_tile = self.map[y][x]
                        if target_tile.tile_type == "water" and self.selected_unit.name == "Mage": 
                            color = (0, 255, 255, 100) 
                        elif target_tile.tile_type == "mud" and not target_tile.is_hidden: 
                            color = (128, 164, 132, 100)  
                        else:
                            color = (40, 200, 40, 100) 

                        move_surface = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA) #transparence
                        move_surface.fill(color)
                        self.screen.blit(move_surface, (x * self.cell_size, y * self.cell_size))

        for (x, y, equipment) in self.equipment_positions:
            if any(abs(unit.x - x) + abs(unit.y - y) <= unit.range for unit in self.units if unit.team == self.current_turn):
                self.screen.blit(
                equipment.image,
                (x * self.cell_size , y * self.cell_size)
                )
        

    
        for unit in self.units:
            unit.draw(self.screen, self.current_turn)
    
        for x, y, color in self.affected_tiles:
            affected_surface = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
            affected_surface.fill(color) 
            self.screen.blit(affected_surface, (x * self.cell_size, y * self.cell_size))

        self.cursor_alpha += 2 * self.cursor_alpha_direction
        if self.cursor_alpha >= 100 or self.cursor_alpha <= 0:
            self.cursor_alpha_direction *= -1 

        cursor_surface = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
        cursor_surface.fill((255, 255, 255, self.cursor_alpha))
        self.screen.blit(cursor_surface, (self.cursor_pos[0] * self.cell_size, self.cursor_pos[1] * self.cell_size))

        self.draw_abilities()

        
    def check_game_over(self):
        team1_units = [unit for unit in self.units if unit.team == "player1"]
        team2_units = [unit for unit in self.units if unit.team == "player2"]

        if not team1_units:  
            print_f("FIN DU JEU! le joueur 2 a gagné!")
            self.display_game_over("le joueur 2 a gagné!")
            return True
        elif not team2_units:  
            print_f("FIN DU JEU! le joueur 1 a gagné!")
            self.display_game_over("le joueur 1 a gagné!")
            return True
        return False
<<<<<<< HEAD
   def display_game_over(self, message):
        """affichage game over."""
        font = pygame.font.Font(None, 72)
        text = font.render("Game Over", True, (255, 255, 255))
        winner_text = font.render(message, True, (255, 255, 255))

        self.screen.fill((0, 0, 0)) 
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 3))
        self.screen.blit(winner_text, (self.screen.get_width() // 2 - winner_text.get_width() // 2, self.screen.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(7000) 
        pygame.quit()
        exit()

    def can_move_to(self, unit, x, y):
        """vérifie si une unité peut se déplacer à une position donnéee."""
        if not (0 <= x < len(self.map[0]) and 0 <= y < len(self.map)):  
            return False

        target_tile = self.map[y][x]
        if (target_tile.tile_type == "water" and unit.name != "Mage") or target_tile.tile_type == "rock":
            return False
        return unit.can_move_to(x, y,self.map)
=======

    def spawn_equipment(self):

        self.equipment_positions = []  
        occupied_positions = {(unit.x, unit.y) for unit in self.units}  
        
        left_positions = [
            (x, y) for y in range(1, len(self.map) // 2)
            for x in range(1, len(self.map[0]) // 2)
            if self.map[y][x].tile_type not in ("wall", "rock", "mud") and (x, y) not in occupied_positions
        ]
        right_positions = [
            (x, y) for y in range(len(self.map) // 2, len(self.map) - 1)
            for x in range(len(self.map[0]) // 2, len(self.map[0]) - 1)
            if self.map[y][x].tile_type not in ("wall", "rock", "mud") and (x, y) not in occupied_positions
        ]

        for _ in range(3):
            
            left_water_positions = [pos for pos in left_positions if self.map[pos[1]][pos[0]].tile_type == "water"]
            if left_water_positions:
                pos = random.choice(left_water_positions)
                self.equipment_positions.append((pos[0], pos[1], random.choice([AttackBoost(10), DefenseBoost(5), EvasionBoost(0.1)])))
                left_positions.remove(pos)
                
            if left_positions:
                pos = random.choice(left_positions)
                self.equipment_positions.append((pos[0], pos[1], random.choice([AttackBoost(10), DefenseBoost(5), EvasionBoost(0.1)])))
                left_positions.remove(pos)

            if right_positions:
                pos = random.choice(right_positions)
                self.equipment_positions.append((pos[0], pos[1], random.choice([AttackBoost(10), DefenseBoost(5), EvasionBoost(0.1)])))
                right_positions.remove(pos)



    def check_equipment_pickup(self):
        """vérifie si un charactère a récupéré un équipement."""
        for (x, y, equipment) in self.equipment_positions[:]:
            for unit in self.units:
                if (unit.x, unit.y) == (x, y):
                    equipment.apply(unit)  
                    print_f(f"{unit.name}  {equipment.name}!")
                    self.equipment_positions.remove((x, y, equipment)) 
>>>>>>> 32034c3f8f95e2d4025794e80ca62b68273c2767
