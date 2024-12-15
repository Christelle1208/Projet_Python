import pygame

class Bouton:
    """Classe permettant de créer un bouton interactif."""

    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        """
        Initialise la classe Bouton.

        Args:
            image (pygame.Surface): L'image du bouton.
            pos (tuple): La position (x, y) du bouton.
            text_input (str): Le texte affiché sur le bouton.
            font (pygame.font.Font): La police utilisée pour le texte.
            base_color (tuple): La couleur de base du texte.
            hovering_color (tuple): La couleur du texte lorsque la souris survole le bouton.
        """
        self.image = image if image is not None else None
        self.x_pos, self.y_pos = pos
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input

        # Création du texte
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text

        # Définition des rectangles pour les positions
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        """
        Met à jour l'affichage du bouton sur l'écran.

        Args:
            screen (pygame.Surface): L'écran où afficher le bouton.
        """
        if self.image:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        """
        Vérifie si le curseur est sur le bouton.

        Args:
            position (tuple): La position (x, y) du curseur.

        Returns:
            bool: True si le curseur est sur le bouton, sinon False.
        """
        return self.rect.collidepoint(position)

    def changeColor(self, position):
        """
        Change la couleur du texte en fonction du survol de la souris.

        Args:
            position (tuple): La position (x, y) du curseur.
        """
        if self.rect.collidepoint(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
