import sys
import pygame

<<<<<<< HEAD
from simulacao import Simulacao
from parametros import Parametro
Stop_simulation=False
if __name__ == "__main__":
    pygame.init(  )
    pygame.mixer.init(  )
    SCREEN_WIDTH = 120
    SCREEN_HEIGHT = 120
    FPS = 1
    clock = pygame.time.Clock(  )
    screen = pygame.display.set_mode( ( SCREEN_WIDTH, SCREEN_HEIGHT ) )
    pygame.display.set_caption( "Agentes" )
    parametro = Parametro(  )
    simulacao = Simulacao( parametro )
    Stop_simulation=False
=======
from scene_manager import SceneManager

if __name__ == "__main__":
    pygame.init(  )
    pygame.mixer.init(  )
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    FPS = 15
    clock = pygame.time.Clock(  )
    screen = pygame.display.set_mode( ( SCREEN_WIDTH, SCREEN_HEIGHT ) )
    pygame.display.set_caption( "Agentes" )
    gerenciador_cenas = SceneManager(  )
>>>>>>> main

    while True:
        for event in pygame.event.get(  ):
            if event.type== pygame.KEYDOWN:
                Stop_simulation=not Stop_simulation
            if event.type == pygame.QUIT:
                pygame.quit(  )
                sys.exit(  )
<<<<<<< HEAD
        if not Stop_simulation:
            simulacao.run(  )
    
=======
        
        gerenciador_cenas.run(  )

>>>>>>> main
        pygame.display.update(  )
        clock.tick( FPS )