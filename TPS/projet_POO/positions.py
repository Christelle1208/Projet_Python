import random

def random_position(ligne, colonne, liste):
    x = random.choice(ligne)
    y = random.choice(colonne)
    while (x,y) in liste:
        print("doublon")
        x = random.choice(ligne)
        y = random.choice(colonne)
    return (x,y)

# liste = []
# ligne = [1,2,3,4,5]
# colonne = [1,2,3,4,5]
# for i in range(4):
#     liste.append(random_position(ligne, colonne, liste))
# print (liste)

