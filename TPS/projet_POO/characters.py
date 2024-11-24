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
___________ a modifier __________________

class Unit:
    def __init__(self, name, hp, attack, defense, speed, range):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.range = range
        self.has_acted = False
        self.x = 0
        self.y = 0
        self.team = None
        self.color = None

    def take_damage(self, amount, ignore_defense=False):
        if ignore_defense:
            self.hp -= amount
        else:
            damage_taken = max(0, amount - self.defense)
            self.hp -= damage_taken
        print(f"{self.name} takes {amount} damage! HP left: {self.hp}")

    def can_move_to(self, x, y):
        """Check if the target position (x, y) is within the unit's movement range."""
        return abs(self.x - x) <= self.range and abs(self.y - y) <= self.range

    def attack_enemy(self, target):
        print(f"{self.name} attacks {target.name} with power {self.attack}.")
        target.take_damage(self.attack)

    def draw(self, screen):
        """Draw the unit on the screen."""
        border_color = BLUE if self.team == "player1" else RED
        pygame.draw.rect(
            screen, 
            border_color, 
            (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 
            2
        )
        pygame.draw.circle(
            screen, 
            self.color, 
            (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2), 
            CELL_SIZE // 3
        )

class Tank(Unit):
    def __init__(self):
        super().__init__("Tank", hp=100, attack=20, defense=10, speed=2, range=1)

    def attack_enemy(self, target):
        print(f"{self.name} (Tank) performs a heavy strike on {target.name}.")
        super().attack_enemy(target)

class Assassin(Unit):
    def __init__(self):
        super().__init__("Assassin", hp=70, attack=40, defense=5, speed=4, range=1)

    def attack_enemy(self, target):
        print(f"{self.name} (Assassin) strikes swiftly at {target.name}.")
        super().attack_enemy(target)

class Marksman(Unit):
    def __init__(self):
        super().__init__("Marksman", hp=75, attack=35, defense=6, speed=3, range=3)

    def attack_enemy(self, target):
        print(f"{self.name} (Marksman) shoots at {target.name} from afar.")
        super().attack_enemy(target)

class Mage(Unit):
    def __init__(self):
        super().__init__("Mage", hp=60, attack=30, defense=3, speed=3, range=2)

    def attack_enemy(self, target):
        print(f"{self.name} (Mage) casts a magical spell on {target.name}.")
        target.take_damage(self.attack, ignore_defense=True)  

    def move(self):
        print(f"{self.name} (Mage) moves and can walk on water.")

héritage entre les characteres, et ajout des caractéristiques des characteres  ( déplacements, prend des dégats, déplacements...)

