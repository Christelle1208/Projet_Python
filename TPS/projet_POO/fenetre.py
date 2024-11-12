import pygame
import pytmx 
import pyscroll 



pygame.init()

class Game:
    
    def __init__(self):
        
        #fenêtre du jeu

        self.screen = pygame.display.set_mode((1400,700))
        pygame.display.set_caption("mon_jeu")
        
        #chargement de la carte
        tmx_data = pytmx.util_pygame.load_pygame('/Users/shaqaotmeal/Desktop/ISI/python/PROJET/carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data,self.screen.get_size())
        #map_layer.zoom = 2
        
        self.group = pyscroll.PyscrollGroup(map_layer = map_layer, default_layer = 1)
   
        
                
    def run(self):
        
        # boucle du jeu

        running = True

        while running :
            
            self.group.draw(self.screen)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT :
                    running = False
                    
        pygame.quit()
