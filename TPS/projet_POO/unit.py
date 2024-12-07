import pygame
from config import CELL_SIZE
import random

class Unit:
    def __init__(self, name, hp, attack, defense, range ,evasion, image_path):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.range = range
        self.has_acted = False
        self.evasion = evasion
        self.x = 0
        self.y = 0
        self.team = None
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))  # Scale image to fit the tile
        self.is_visible = True  # Assume all units start visible
        self.game = None  # Placeholder for the associated Game instance

    def set_game(self, game):
        """Associate this unit with a Game instance."""
        self.game = game

    def draw(self, screen, current_turn):
        """Draw the unit and its HP bar if visible."""
        if not self.is_visible and self.team != current_turn:
            return  

        # Draw the character image
        screen.blit(self.image, (self.x * CELL_SIZE, self.y * CELL_SIZE))

        if self.team == current_turn:
            border_color = (0, 0, 255)  # Blue for friendly units
        elif self.is_visible:
            border_color = (255, 0, 0)  # Red for visible enemies
        else:
            border_color = None

        # Draw border around the unit's tile
        if border_color:
            pygame.draw.rect(
                screen,
                border_color,
                (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                3  # Border thickness
            )
        # Draw the HP bar
        bar_width = 5  # Starting position 
        bar_height = CELL_SIZE  # Small height for the HP bar
        bar_x = self.x * CELL_SIZE + CELL_SIZE  # Positioned to the right of the unit
        bar_y = self.y * CELL_SIZE + (CELL_SIZE - bar_height) // 2  # Centered vertically

        # Calculate HP bar proportion
        hp_ratio = max(0, self.hp / self.max_hp)  # Ensure the ratio is not negative
        hp_fill_height = int(bar_height * hp_ratio)

        # Draw the background of the HP bar
        pygame.draw.rect(screen, (255, 0, 0), (bar_x - 5, bar_y, bar_width, bar_height))  # Red background for missing HP
        pygame.draw.rect(screen, (0, 255, 0), (bar_x - 5, bar_y + bar_height - hp_fill_height, bar_width,hp_fill_height))  # Green for current HP


    def take_damage(self, amount, ignore_defense=False):
        """Calculate and apply damage, considering evasion."""
        evasion = self.evasion
        if self.game.map[self.y][self.x].tile_type == "lava":
            evasion -= 0.1
        if random.random() < evasion:  # Check if the attack is evaded
            if self.is_visible:  # Only print feedback if the unit is visible
                print(f"{self.name} dodges the attack!")
            return  # No damage is applied if the attack is dodged

        # Apply damage if the attack is not dodged
        if ignore_defense:
            self.hp -= amount
        else:
            damage_taken = max(0, amount - self.defense)
            self.hp -= damage_taken

        if self.is_visible:  # Only print feedback if the unit is visible
            print(f"{self.name} takes {amount} damage! HP left: {self.hp}")

    def can_move_to(self, x, y, map):
        """Check if the target position (x, y) is within the unit's movement range."""
        return (
            (abs(self.x - x) + abs(self.y - y) <= (self.range + 1)) and
            1 <= x < len(map[0]) -1 and
            1 <= y < len(map) - 1
        )

    def attack_enemy(self, target):
        attack = self.attack
        if self.game.map[self.y][self.x].tile_type == "lava":
            attack *= 0.9
        print(f"{self.name} attacks {target.name} with power {attack}.")
        target.take_damage(attack)


class Tank(Unit):
    def __init__(self, name, image_path):
        super().__init__(name, hp=100, attack=20, defense=10, range=1, evasion=0.1, image_path=image_path)

    def attack_enemy(self, target):
        print(f"{self.name} (Tank) performs a heavy strike on {target.name}.")
        super().attack_enemy(target)


class Assassin(Unit):
    def __init__(self, name, image_path):
        super().__init__(name, hp=70, attack=40, defense=5, range=2, evasion=0.35, image_path=image_path)

    def attack_enemy(self, target):
        print(f"{self.name} (Assassin) strikes swiftly at {target.name}.")
        super().attack_enemy(target)


class Marksman(Unit):
    def __init__(self, name, image_path):
        super().__init__(name, hp=75, attack=35, defense=6, range=3, evasion=0.2, image_path=image_path)

    def attack_enemy(self, target):
        print(f"{self.name} (Marksman) shoots at {target.name} from afar.")
        super().attack_enemy(target)


class Mage(Unit):
    def __init__(self, name, image_path):
        super().__init__(name, hp=65, attack=35, defense=3, range=2, evasion=0.25, image_path=image_path)

    def attack_enemy(self, target):
        print(f"{self.name} (Mage) casts a magical spell on {target.name}.")
        target.take_damage(self.attack, ignore_defense=True)  # Ignores defense

    def move(self):
        print(f"{self.name} (Mage) moves and can walk on water.")
