import random

    def random_position(ligne, colonne, taken_positions):
            """Génère une position aléatoire unique."""
            x = random.choice(ligne)
            y = random.choice(colonne)
            while (x, y) in taken_positions:
                print("doublon")
                x = random.choice(ligne)
                y = random.choice(colonne)
            return (x, y)

        player1_ligne = range(1, 5)  
        player1_colonne = range(1, 5)  

        player2_ligne = range (16,20)
        player2_colonne = range(16,20)

# liste = []
# ligne = [1,2,3,4,5]
# colonne = [1,2,3,4,5]
# for i in range(4):
#     liste.append(random_position(ligne, colonne, liste))
# print (liste)
