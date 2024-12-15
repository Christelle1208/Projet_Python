from unit import Unit
from print_f import print_f

# ========================================
# Classe Tank
# ========================================
class Tank(Unit):
    """Classe représentant une unité Tank."""

    def __init__(self, name: str, image_path: str):
        super().__init__(name, hp=100, attack=20, defense=10, range=1, evasion=0.1, image_path=image_path)

    def attack_enemy(self, target: Unit):
        """Attaque une cible."""
        print_f(f"{self.name} lance une attaque sur le personnage {target.name}.")
        super().attack_enemy(target)


# ========================================
# Classe Assassin
# ========================================
class Assassin(Unit):
    """Classe représentant une unité Assassin."""

    def __init__(self, name: str, image_path: str):
        super().__init__(name, hp=70, attack=40, defense=5, range=2, evasion=0.35, image_path=image_path)

    def attack_enemy(self, target: Unit):
        """Attaque une cible."""
        print_f(f"{self.name} tente un homicide sur le personnage {target.name}.")
        super().attack_enemy(target)


# ========================================
# Classe Archer
# ========================================
class Archer(Unit):
    """Classe représentant une unité Archer."""

    def __init__(self, name: str, image_path: str):
        super().__init__(name, hp=75, attack=35, defense=6, range=3, evasion=0.2, image_path=image_path)

    def attack_enemy(self, target: Unit):
        """Attaque une cible."""
        print_f(f"{self.name} lance ses flèches sur le personnage {target.name}.")
        super().attack_enemy(target)


# ========================================
# Classe Mage
# ========================================
class Mage(Unit):
    """Classe représentant une unité Mage."""

    def __init__(self, name: str, image_path: str):
        super().__init__(name, hp=65, attack=35, defense=3, range=2, evasion=0.25, image_path=image_path)

    def attack_enemy(self, target: Unit):
        """Attaque une cible en lançant un sort."""
        print_f(f"{self.name} jette un sort sur le personnage {target.name}.")
        target.take_damage(self.attack, ignore_defense=True)
