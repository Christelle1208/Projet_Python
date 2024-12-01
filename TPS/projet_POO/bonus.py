class Bonus:
    def __init__(self, x, y, effect_type):
        """
        Initialise un objet bonus.

        :param x: La position en x sur la carte.
        :param y: La position en y sur la carte.
        :param effect_type: Le type d'effet du bonus (ex: 'health', 'attack', 'defense').
        """
        self.x = x
        self.y = y
        self.effect_type = effect_type

    def apply_bonus(self, unit):
        if self.effect_type == 'health':
            unit.health += 20  
        elif self.effect_type == 'attack':
            unit.attack += 5  
        elif self.effect_type == 'defense':
            unit.defense += 5 

        print(f"{unit.name} a reçu un bonus de {self.effect_type}!")

  
