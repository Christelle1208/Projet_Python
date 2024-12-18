﻿# Projet_Python

Explication du jeu :

Chaque joueur possède 4 personnages : un Archer, un Mage, un Assassin et un Tank

Chaque joueur à 4 habiletés à sa disposition : la Bombe (1), le Sniper (2), la Fumée (3) et une capacité de régénération/soin (4), on peut annuler la sélection de l'habilité en cliquant sur la touche esc.

Chaque habileté possède un « cooldown » : le joueur ne peut utiliser cette attaque que tous les deux ou trois tours par exemple. Cela évite un jeu basé uniquement sur des attaques à distance et encourage les déplacements stratégiques. Les personnages ont également une probabilité d’esquiver une attaque.

Le Mage est le seul personnage à pouvoir se déplacer sur l’eau et ses attaques ignorent la défense des autres joueurs.

Le joueur ne voit ses ennemis qu’à partir du moment où ceux-ci sont dans sa portée de déplacement.

La Bombe fait des dégâts sur une zone en forme d’étoile : plus la cible est proche du centre, plus les dégâts seront importants, si la cible est en bordure de zone d’attaque, les dégâts seront minimaux. Le Sniper prend une zone de 1x1 et ne fait des dégâts qu’à l’unité sur cet emplacement. La Fumée à une zone d’effet de 3x3 et masque la visibilité des unités présents dans cette zone durant un tour. Le Soin rend à son utilisateur 20% de ses points de vie.

Les joueurs ont le choix entre trois cartes différentes, sélectionnables depuis le menu du jeu. Différents obstacles sont présents : l’eau, des rochers et de la boue. Cette dernière réduit la probabilité d’esquive et la statistique d’attaque du personnage se tenant sur la case. De plus, la boue est masquée et n’est révélée que lors d’un déplacement d’une unité sur son emplacement pour la première fois.

Des bonus de 3 types peuvent apparaître aléatoirement sur la carte : une chaussure (bonus d’esquive), un bouclier (bonus de défense) et une épée (bonus d’attaque).
