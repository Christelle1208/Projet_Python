import pygame
from config import CELL_SIZE

class Unit:
    def __init__(self, name, hp, attack, defense, range, image_path):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.range = range
        self.has_acted = False
        self.x = 0
        self.y = 0
        self.team = None
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))  # Scale image to fit the tile
        self.is_visible = True  # all units start visible
        
      def draw(self, screen, current_turn):
        """Draw the unit and its HP bar if visible."""
        if not self.is_visible and self.team != current_turn:
            return  # Don't draw invisible units

        # Draw the character image
        screen.blit(self.image, (self.x * CELL_SIZE, self.y * CELL_SIZE))

        # Draw the HP bar
        bar_width = CELL_SIZE // 2  # Half the cell width
        bar_height = 5  # Small height for the HP bar
        bar_x = self.x * CELL_SIZE + CELL_SIZE + 2  # Positioned to the right of the unit
        bar_y = self.y * CELL_SIZE + (CELL_SIZE - bar_height) // 2  # Centered vertically

        # Calculate HP bar proportion
        hp_ratio = max(0, self.hp / 100)  # Ensure the ratio is not negative
        hp_fill_width = int(bar_width * hp_ratio)

        # Draw the background of the HP bar
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))  # Red background for missing HP
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, hp_fill_width, bar_height))  # Green for current HP


    def take_damage(self, amount, ignore_defense=False):
        if ignore_defense:
            self.hp -= amount
        else:
            damage_taken = max(0, amount - self.defense)
            self.hp -= damage_taken
        print(f"{self.name} takes {amount} damage! HP left: {self.hp}")

    def can_move_to(self, x, y, map):
        """Check if the target position (x, y) is within the unit's movement range."""
        return (
            (abs(self.x - x) + abs(self.y - y) <= (self.range + 1)) and
            0 <= x < len(map[0]) and
            0 <= y < len(map)
        )

    def attack_enemy(self, target):
        print(f"{self.name} attacks {target.name} with power {self.attack}.")
        target.take_damage(self.attack)


class Tank(Unit):
    def __init__(self, name, image_path):
        super().__init__(name, hp=100, attack=20, defense=10, range=1, image_path=image_path)

    def attack_enemy(self, target):
        print(f"{self.name} (Tank) performs a heavy strike on {target.name}.")
        super().attack_enemy(target)


class Assassin(Unit):
    def __init__(self, name, image_path):
        super().__init__(name, hp=70, attack=40, defense=5, range=2, image_path=image_path)

    def attack_enemy(self, target):
        print(f"{self.name} (Assassin) strikes swiftly at {target.name}.")
        super().attack_enemy(target)


class Marksman(Unit):
    def __init__(self, name, image_path):
        super().__init__(name, hp=75, attack=35, defense=6, range=3, image_path=image_path)

    def attack_enemy(self, target):
        print(f"{self.name} (Marksman) shoots at {target.name} from afar.")
        super().attack_enemy(target)


class Mage(Unit):
    def __init__(self, name, image_path):
        super().__init__(name, hp=65, attack=35, defense=3, range=2, image_path=image_path)

    def attack_enemy(self, target):
        print(f"{self.name} (Mage) casts a magical spell on {target.name}.")
        target.take_damage(self.attack, ignore_defense=True)  # Ignores defense

    def move(self):
        print(f"{self.name} (Mage) moves and can walk on water.")

