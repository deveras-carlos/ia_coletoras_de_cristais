import sys
import pygame

from simulacao import Simulacao
from parametros import Parametro

if __name__ == "__main__":
    pygame.init(  )
    pygame.mixer.init(  )
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    FPS = 1
    clock = pygame.time.Clock(  )
    screen = pygame.display.set_mode( ( SCREEN_WIDTH, SCREEN_HEIGHT ) )
    pygame.display.set_caption( "Agentes" )
    parametro = Parametro(  )
    simulacao = Simulacao( parametro )

    while True:
        for event in pygame.event.get(  ):
            if event.type == pygame.QUIT:
                pygame.quit(  )
                sys.exit(  )
        
        simulacao.run(  )

        pygame.display.update(  )
        clock.tick( FPS )