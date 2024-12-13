import pygame
from print_f import *

class Ability:
    """classe habilité."""
    def __init__(self, name):
        self.name = name

    def activate(self, game, user, target_pos):
        """activation de l'habilité."""
        pass


class Bomb(Ability):
    """habilité bombe."""
    def __init__(self):
        super().__init__("Bomb")

    def activate(self, game, user, target_pos):
        center_x, center_y = target_pos
        
        # calcule les tiles affectées Calculate affected tiles based on the cursor position
        affected_tiles = [
            (center_x + dx, center_y + dy)
            for dx in range(-5, 6)
            for dy in range(-5, 6)
            if (
                1 <= center_x + dx < len(game.map[0]) - 1 and
                1 <= center_y + dy < len(game.map) - 1 and
                abs(dx) + abs(dy) <= 3
            )
        ]
# dégats sur la zone affectée
        for unit in game.units:
            if (unit.x, unit.y) in affected_tiles:
                distance = abs(unit.x - center_x) + abs(unit.y - center_y)
                damage = max(0, 30 - (distance * 5))  # plus il est loin, moin les dégats sont forts
                unit.take_damage(damage)
                if unit.hp <= 0:
                    print_f(f"{unit.name} a éte vaincu !")
                    if game.map[unit.y][unit.x].tile_type == "grass":
                        game.map[unit.y][unit.x].tile_type = "dead_grass"
                    if game.map[unit.y][unit.x].tile_type == "soil":
                        game.map[unit.y][unit.x].tile_type = "dead_soil"
                    game.units.remove(unit)
                    

        print_f(f"{user.name} a utiliser l'habilité bombe.")
        user.has_acted = True
        game.clear_affected_tiles()  # supprime la fumée après utilisation 
class Sniper(Ability):
    """habilité sniper."""
    def __init__(self):
        super().__init__("Sniper")

    def activate(self, game, user, target_pos):
        target_x, target_y = target_pos
        target_unit = next((unit for unit in game.units if unit.x == target_x and unit.y == target_y), None)
        if target_unit:
            distance = abs(user.x - target_x) + abs(user.y - target_y)
            damage = max(20, 50 - (distance * 2))  # Min 20% degat
            target_unit.take_damage(damage)
            if target_unit.hp <= 0:  
                print_f(f"{target_unit.name} a été vaincu !")
                if game.map[target_unit.y][target_unit.x].tile_type == "grass":
                    game.map[target_unit.y][target_unit.x].tile_type = "dead_grass"
                if game.map[target_unit.y][target_unit.x].tile_type == "soil":
                    game.map[target_unit.y][target_unit.x].tile_type = "dead_soil"
                game.units.remove(target_unit)
        user.has_acted = True