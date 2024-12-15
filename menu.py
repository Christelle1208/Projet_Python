import pygame
import sys
from boutons import Bouton
pygame.mixer.init()

pygame.init()

background_music=pygame.mixer.music.load("assets/Background music.mp3")
pygame.mixer.music.play(10, 0.0)
CLICK_SOUND = pygame.mixer.Sound("assets/Click Sound.wav")

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background Image.jpg")
#Resize the background image to fit the screen
BG = pygame.transform.scale(BG, (1280, 720))

def get_font(size):
    """Get the font."""
    return pygame.font.Font("assets/font.ttf", size) 
    
def options():
    """Options menu."""
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("Choose a map :", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 200))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Bouton(image=None, pos=(640, 660), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")
        
        MAP1 = Bouton(image=None, pos=(640, 300), 
                            text_input="MAP 1", font=get_font(75), base_color="Green", hovering_color="Purple")
        
        MAP2 = Bouton(image=None, pos=(640, 400), 
                            text_input="MAP 2", font=get_font(75), base_color="Orange", hovering_color="Purple")
        
        MAP3 = Bouton(image=None, pos=(640, 500), 
                            text_input="MAP 3", font=get_font(75), base_color="Red", hovering_color="Purple")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        MAP1.changeColor(OPTIONS_MOUSE_POS)
        MAP1.update(SCREEN)
        MAP2.changeColor(OPTIONS_MOUSE_POS)
        MAP2.update(SCREEN)
        MAP3.changeColor(OPTIONS_MOUSE_POS)
        MAP3.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    CLICK_SOUND.play()
                    main_menu()
                if MAP1.checkForInput(OPTIONS_MOUSE_POS):
                    CLICK_SOUND.play()
                    return 1
                if MAP2.checkForInput(OPTIONS_MOUSE_POS):
                    CLICK_SOUND.play()
                    return 2
                if MAP3.checkForInput(OPTIONS_MOUSE_POS):
                    CLICK_SOUND.play()
                    return 3

        pygame.display.update()

def main_menu():
    """Main menu."""
    map_chosen = 1
    while True:
        # background_music.play()
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#e8aa46")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Bouton(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#def29b", hovering_color="White")
        OPTIONS_BUTTON = Bouton(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#def29b", hovering_color="White")
        QUIT_BUTTON = Bouton(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#def29b", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    CLICK_SOUND.play()
                    return map_chosen
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    CLICK_SOUND.play()
                    chosen_map = options()
                    if chosen_map is not None:
                        map_chosen = chosen_map #update de la map choisie
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    CLICK_SOUND.play() 
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

