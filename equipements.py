from config import CELL_SIZE, BOOTS, SWORD, ARMOR
import pygame
from print_f import print_f


# ========================================
# Classe parente : Equipment
# ========================================
class Equipment:
    """Classe pour représenter un équipement."""

    def __init__(self, name: str, image_path: str):
        """Initialisation de l'équipement.

        Args:
            name (str): Le nom de l'équipement.
            image_path (str): Le chemin de l'image de l'équipement.
        """
        self.name = name
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))

    def apply(self, unit):
        """Appliquer l'effet de l'équipement à une unité.

        Args:
            unit (Unit): L'unité à laquelle appliquer l'effet.
        """
        pass


# ========================================
# Sous-classe : AttackBoost
# ========================================
class AttackBoost(Equipment):
    """Équipement qui augmente la force d'attaque."""

    def __init__(self, boost_amount: int):
        super().__init__("Récupère l'épée de la mort", SWORD)
        self.boost_amount = boost_amount

    def apply(self, unit):
        """Appliquer l'effet d'augmentation d'attaque."""
        unit.attack += self.boost_amount
        print_f(f"{unit.name} voit son attaque augmenter de {self.boost_amount}!")


# ========================================
# Sous-classe : DefenseBoost
# ========================================
class DefenseBoost(Equipment):
    """Équipement qui augmente la défense."""

    def __init__(self, boost_amount: int):
        super().__init__("Récupère le bouclier divin", ARMOR)
        self.boost_amount = boost_amount

    def apply(self, unit):
        """Appliquer l'effet d'augmentation de défense."""
        unit.defense += self.boost_amount
        print_f(f"{unit.name} voit sa défense augmenter de {self.boost_amount}!")


# ========================================
# Sous-classe : EvasionBoost
# ========================================
class EvasionBoost(Equipment):
    """Équipement qui augmente le taux d'évasion."""

    def __init__(self, evasion_rate: float):
        super().__init__("Récupère l'évasion fugitive", BOOTS)
        self.evasion_rate = evasion_rate

    def apply(self, unit):
        """Appliquer l'effet d'augmentation du taux d'évasion."""
        unit.evasion += self.evasion_rate
        print_f(f"{unit.name} voit son taux d'évasion augmenter de {self.evasion_rate * 100:.2f}%!")
