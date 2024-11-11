import pygame
import random

from unit_copy import *

'''
Différents perspnnages :
- Tank (beaucoup de PV, peu d'attaque, grosse défense)
- Assassin (beaucoup d'attaque, courte portée, PV moyens, défense moyenne)
- Mage (PV moyens, défense moyenne, attaque moyenne)
- Archers (attaque moyenne, défense faible, PV moyens)
'''
class Personnage:
    """
    Classe pour représenter un personnage.

    '''Attributs
    ---------
    type_perso: str
        Le type de personnage.
    team: str
        L'équipe du personnage.
    x: int
        La position x du personnage.
    y: int
        La position y du personnage.

    Méthodes
    --------
    character()
        Retourne une unité correspondant au personnage.
    """

    def __init__(self,type_perso,team,x,y):
        self.type_perso=type_perso
        self.team=team
        self.x=x
        self.y=y
    
    def character(self):
        match(self.type_perso):
            case("Tank"):
                return Unit(self.x, self.y, 70, 5, self.team, type_perso="Tank")
            case("Assassin"):
                return Unit(self.x, self.y, 40, 15, self.team, type_perso="Assassin")
            case("Mage"):
                return Unit(self.x, self.y, 35, 10, self.team, type_perso="Mage")
            case("Archer_poison"):
                return Unit(self.x, self.y, 30, 7, self.team, type_perso="Archer_poison")
            case("Archer_electricite"):
                return Unit(self.x, self.y, 30, 7, self.team, type_perso="Archer_electricite")
            case _:
                print("Type de personnage inconnu")
                return None

