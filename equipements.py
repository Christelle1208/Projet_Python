from config import CELL_SIZE, BOOTS, SWORD, ARMOR
import pygame
from print_f import *


class Equipment:
    """class pour l'équipement."""
    def __init__(self, name, image_path):
        """initialisation de l'équipement.
        Args:
            name (str): le nom de l'équipement.
            image_path (str): le chemin de l'image de l'équipement.
        """
        self.name = name
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
    def apply(self, unit):
        """appliquer l'équipement."""
        pass

class AttackBoost(Equipment):
    """augmente la force d'attaque."""

    def apply(self, unit):
        """appliquer l'attaque."""
        unit.attack += self.boost_amount
        print_f(f"{unit.name} voit son attaque augmenter de {self.boost_amount}!")
        
    def __init__(self, boost_amount):
        """initialisation de l'attaque.
        Args:
            boost_amount (int): le montant de l'attaque.
        """
        super().__init__("récupere l'épée de la mort", SWORD)
        self.boost_amount = boost_amount


class DefenseBoost(Equipment):
    """augmente la defense."""

    def apply(self, unit):
        """appliquer la défense."""
        unit.defense += self.boost_amount
        print_f(f"{unit.name} voit sa défense augmenter de {self.boost_amount}!")
    def __init__(self, boost_amount):
        """initialisation de la défense.
        Args:
            boost_amount (int): le montant de la défense.
        """
        super().__init__("récupere le bouclier divin", ARMOR)
        self.boost_amount = boost_amount


class EvasionBoost(Equipment):
    """augmente le taux d'évasion."""
    
    def apply(self, unit):
        """appliquer l'évasion."""
        unit.evasion += self.evasion_rate
        print_f(f"{unit.name} voit son taux d'évasion augmenter de {self.evasion_rate * 100}%.")
    def __init__(self, evasion_rate):
        """initialisation de l'évasion.
        Args:
            evasion_rate (float): le taux d'évasion.
        """
        super().__init__("récupere l'évasion fugitive", BOOTS)
        self.evasion_rate = evasion_rate
