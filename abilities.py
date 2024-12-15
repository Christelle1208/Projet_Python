import pygame
from print_f import *

# ========================================
# Classe Parent: Ability
# ========================================
class Ability:
    """Classe pour représenter une habilité générique.

    Attributs:
        name (str): Nom de l'habilité.
    """

    def __init__(self, name: str):
        """Initialisation de l'habilité.

        Paramètres:
            name (str): Nom de l'habilité.
        """
        self.name = name

    def activate(self, game, user, target_pos):
        """Méthode à surcharger pour activer l'habilité.

        Paramètres:
            game (Game): Instance de la classe Game.
            user (Unit): Instance de la classe Unit.
            target_pos (tuple): Position de la cible.
        """
        pass


# ========================================
# Sous-classe: Bomb
# ========================================
class Bomb(Ability):
    """Habilité Bombe : Inflige des dégâts dans une zone circulaire."""

    def __init__(self):
        """Initialise l'habilité avec le nom 'Bomb'."""
        super().__init__("Bomb")

    def activate(self, game, user, target_pos):
        """Activation de l'habilité bombe.

        Inflige des dégâts décroissants selon la distance.
        """
        center_x, center_y = target_pos

        # Calcul des tiles affectées
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

        # Application des dégâts
        for unit in game.units:
            if (unit.x, unit.y) in affected_tiles:
                distance = abs(unit.x - center_x) + abs(unit.y - center_y)
                damage = max(0, 30 - (distance * 5))
                unit.take_damage(damage)

                if unit.hp <= 0:
                    print_f(f"{unit.name} a été vaincu !")
                    if game.map[unit.y][unit.x].tile_type == "grass":
                        game.map[unit.y][unit.x].tile_type = "dead_grass"
                    elif game.map[unit.y][unit.x].tile_type == "soil":
                        game.map[unit.y][unit.x].tile_type = "dead_soil"
                    game.units.remove(unit)

        print_f(f"{user.name} a utilisé l'habilité bombe.")
        user.has_acted = True
        game.clear_affected_tiles()


# ========================================
# Sous-classe: Sniper
# ========================================
class Sniper(Ability):
    """Habilité Sniper : Inflige des dégâts à longue distance."""

    def __init__(self):
        """Initialise l'habilité avec le nom 'Sniper'."""
        super().__init__("Sniper")

    def activate(self, game, user, target_pos):
        """Activation de l'habilité sniper.

        Inflige des dégâts à une cible unique, avec diminution par distance.
        """
        target_x, target_y = target_pos

        # Trouver l'unité cible
        target_unit = next((unit for unit in game.units if unit.x == target_x and unit.y == target_y), None)
        if target_unit:
            distance = abs(user.x - target_x) + abs(user.y - target_y)
            damage = max(20, 50 - (distance * 2))  # Dégâts minimum de 20
            target_unit.take_damage(damage)

            if target_unit.hp <= 0:
                print_f(f"{target_unit.name} a été vaincu !")
                if game.map[target_unit.y][target_unit.x].tile_type == "grass":
                    game.map[target_unit.y][target_unit.x].tile_type = "dead_grass"
                elif game.map[target_unit.y][target_unit.x].tile_type == "soil":
                    game.map[target_unit.y][target_unit.x].tile_type = "dead_soil"
                game.units.remove(target_unit)

        user.has_acted = True


# ========================================
# Sous-classe: Smoke
# ========================================
class Smoke(Ability):
    """Habilité Fumée : Crée une zone couverte de fumée."""

    def __init__(self):
        """Initialise l'habilité avec le nom 'Smoke'."""
        super().__init__("Smoke")

    def activate(self, game, user, target_pos):
        """Activation de l'habilité fumée.

        Couvre une zone autour de la cible avec de la fumée.
        """
        center_x, center_y = target_pos

        # Calcul des tiles affectées
        affected_tiles = [
            (center_x + dx, center_y + dy)
            for dx in range(-1, 2)
            for dy in range(-1, 2)
            if 0 <= center_x + dx < len(game.map[0]) and 0 <= center_y + dy < len(game.map)
        ]

        # Applique la fumée
        for x, y in affected_tiles:
            tile = game.map[y][x]
            tile.is_smoke_covered = True
            tile.smoke_duration = 3

        print_f(f"Fumée appliquée autour de la zone ({center_x}, {center_y}).")
        print_f(f"{user.name} a utilisé l'habilité fumée.")
        user.has_acted = True


# ========================================
# Sous-classe: Heal
# ========================================
class Heal(Ability):
    """Habilité Heal : Soigne les unités alliées à proximité."""

    def __init__(self):
        """Initialise l'habilité avec le nom 'Heal'."""
        super().__init__("Heal")

    def activate(self, game, user, _):
        """Activation de l'habilité soin.

        Soigne les unités alliées dans un rayon de 3 cases.
        """
        friendly_units = [unit for unit in game.units if unit.team == user.team]
        for unit in friendly_units:
            if abs(unit.x - user.x) <= 3 and abs(unit.y - user.y) <= 3:
                unit.hp = min(unit.hp + 20, unit.max_hp)

        user.has_acted = True
