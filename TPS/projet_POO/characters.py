import pygame
import random

from unit import *

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
    name: str
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

    def __init__(self,name,pos,team):
        self.name=name
        self.team=team
        self.x=pos[0]
        self.y=pos[1]
    
    def character(self):
        match(self.name):
            case("Tank"):
                return Unit("Tank",self.x,self.y, 70, 5, 10, self.team, range=1)
            case("Assassin"):
                return Unit("Assassin",self.x,self.y, 40, 15, 3, self.team, range=4)
            case("Mage"):
                return Unit("Mage",self.x,self.y, 35, 10, 5, self.team, range=2)
            case("Marksman"):
                return Unit("Marksman",self.x,self.y, 30, 7, 2, self.team, range=3)
            case _:
                print("Type de personnage inconnu : par défaut, le personnage sera un Tank")
                return Unit("Tank",self.x,self.y, 70, 5, 10, self.team, range=1) 

