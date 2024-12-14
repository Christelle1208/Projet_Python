from unit import *

class Tank(Unit):
    def __init__(self, name, image_path):
        super().__init__(name, hp=100, attack=20, defense=10, range=1, evasion=0.1, image_path=image_path)

    def attack_enemy(self, target):
        print_f(f"{self.name} lance une attaque sur le personnage {target.name}.")
        super().attack_enemy(target)


class Assassin(Unit):
    def __init__(self, name, image_path):
        super().__init__(name, hp=70, attack=40, defense=5, range=2, evasion=0.35, image_path=image_path)

    def attack_enemy(self, target):
        print_f(f"{self.name} tente un homicide sur le personnage {target.name}.")
        super().attack_enemy(target)


class archer(Unit):
    def __init__(self, name, image_path):
        super().__init__(name, hp=75, attack=35, defense=6, range=3, evasion=0.2, image_path=image_path)

    def attack_enemy(self, target):
        print_f(f"{self.name} lance ses fléchettes sur {target.name}.")
        super().attack_enemy(target)


class Mage(Unit):
    def __init__(self, name, image_path):
        super().__init__(name, hp=65, attack=35, defense=3, range=2, evasion=0.25, image_path=image_path)

    def attack_enemy(self, target):
        print_f(f"{self.name} jette un sort sur {target.name}.")
        target.take_damage(self.attack, ignore_defense=True)
