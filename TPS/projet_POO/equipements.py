from config import CELL_SIZE, BOOTS, SWORD, ARMOR
import pygame
from print_f import *


class Equipment:
    """class pour l'équipement."""
    def __init__(self, name, image_path):
        self.name = name
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
    def apply(self, unit):
        """appliquer l'équipement."""
        pass

class AttackBoost(Equipment):
    """augmente la force d'attaque."""

    def apply(self, unit):
        unit.attack += self.boost_amount
        print_f(f"{unit.name} voit son attaque augmenter de {self.boost_amount}!")
        
    def __init__(self, boost_amount):
        super().__init__("récupere l'épée de la mort", SWORD)
        self.boost_amount = boost_amount


class DefenseBoost(Equipment):
    """augmente la defense."""

    def apply(self, unit):
        unit.defense += self.boost_amount
        print_f(f"{unit.name} voit sa défense augmenter de {self.boost_amount}!")
    def __init__(self, boost_amount):
        super().__init__("récupere le bouclier divin", ARMOR)
        self.boost_amount = boost_amount


class EvasionBoost(Equipment):
    """augmente le taux d'évasion."""
    
    def apply(self, unit):
        unit.evasion += self.evasion_rate
        print_f(f"{unit.name} voit son taux d'évasion augmenter de {self.evasion_rate * 100}%.")
    def __init__(self, evasion_rate):
        super().__init__("récupere l'évasion fugitive", BOOTS)
        self.evasion_rate = evasion_rate
