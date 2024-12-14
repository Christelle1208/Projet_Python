import pygame
from print_f import *
from abilities import *

def handle_key(self, key):

        self.clear_affected_tiles()
        
        cooldowns = self.player1_cooldowns if self.current_turn == "player1" else self.player2_cooldowns
        
        if self.ability_mode:  
            
            dx, dy = 0, 0
            if key == pygame.K_UP:
                dy = -1
            elif key == pygame.K_DOWN:
                dy = 1
            elif key == pygame.K_LEFT:
                dx = -1
            elif key == pygame.K_RIGHT:
                dx = 1
            elif key == pygame.K_SPACE: 
                target_pos = self.cursor_pos
                self.ability_mode.activate(self, self.selected_unit, target_pos)
                self.selected_unit.has_acted = True  
                self.clear_affected_tiles() 
                self.ability_mode = None  
                self.select_next_unit()  
                return
            
            elif key == pygame.K_ESCAPE: 
                print_f("habilité sélection annulée.")
                cooldowns[self.ability_mode.name] = 0
                self.clear_affected_tiles() 
                self.ability_mode = None
                self.cursor_pos = (self.selected_unit.x, self.selected_unit.y)
                
                return

           
            new_x, new_y = self.cursor_pos[0] + dx, self.cursor_pos[1] + dy
            
            if 1 <= new_x < len(self.map[0]) - 1 and 1 <= new_y < len(self.map) - 1:
                self.cursor_pos = (new_x, new_y)
            
            if isinstance(self.ability_mode, Bomb):
                affected_tiles = [
                    (self.cursor_pos[0] + dx, self.cursor_pos[1] + dy)
                    for dx in range(-5, 6)
                    for dy in range(-5, 6)
                    if (
                        1 <= self.cursor_pos[0] + dx < len(self.map[0]) - 1 and
                        1 <= self.cursor_pos[1] + dy < len(self.map) - 1 and
                        abs(dx) + abs(dy) <= 3
                    )
                ]
                self.add_affected_tiles(affected_tiles, (255, 0, 0, 100))  


        elif key == pygame.K_1 and cooldowns["Bomb"] == 0:
            print_f("habilité bomb sélectionnée, choisir une zone.")
            self.ability_mode = Bomb()
            cooldowns["Bomb"] = 3
            affected_tiles = [
                (self.cursor_pos[0] + dx, self.cursor_pos[1] + dy)
                for dx in range(-5, 6)
                for dy in range(-5, 6)
                if (
                    1 <= self.cursor_pos[0] + dx < len(self.map[0]) - 1 and
                    1 <= self.cursor_pos[1] + dy < len(self.map) - 1 and
                    abs(dx) + abs(dy) <= 3
                )
            ]
            self.add_affected_tiles(affected_tiles, (255, 0, 0, 100))  
            
        elif key == pygame.K_2 and cooldowns["Sniper"] == 0:
            print_f("habilité sniper choisie, choisir une cible.")
            self.ability_mode = Sniper()
            cooldowns["Sniper"] = 3
            
        elif key == pygame.K_3 and cooldowns["Smoke"] == 0:
            print_f("habilité smoke choisie, choisir une zone.")
            self.ability_mode = Smoke()
            cooldowns["Smoke"] = 1
            
        elif key == pygame.K_4 and cooldowns["Heal"] == 0:
            print_f("habilité soin activée.")
            Heal().activate(self, self.selected_unit, None)
            cooldowns["Heal"] = 3 
            self.selected_unit.has_acted = True 
            self.select_next_unit()
            
        else:
            dx, dy = 0, 0
            if key == pygame.K_UP:
                dy = -1
            elif key == pygame.K_DOWN:
                dy = 1
            elif key == pygame.K_LEFT:
                dx = -1
            elif key == pygame.K_RIGHT:
                dx = 1
            elif key == pygame.K_SPACE:
                self.confirm_action()
                return
            
            new_x, new_y = self.cursor_pos[0] + dx, self.cursor_pos[1] + dy
            if self.selected_unit.can_move_to(new_x, new_y, self.map):
                self.cursor_pos = (new_x, new_y)
