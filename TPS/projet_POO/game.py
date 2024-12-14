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
            
