import sys
import pygame

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

    while True:
        for event in pygame.event.get(  ):
            if event.type== pygame.KEYDOWN:
                Stop_simulation=not Stop_simulation
            if event.type == pygame.QUIT:
                pygame.quit(  )
                sys.exit(  )
        if not Stop_simulation:
            simulacao.run(  )
    
        pygame.display.update(  )
        clock.tick( FPS )