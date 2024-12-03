import sys
import pygame

from Cenas.menu import menu_terminal
from parametros import Parametro
from Cenas import CenaSimulacao

if __name__ == "__main__":

    parametros : Parametro = Parametro(  )
    parametros = menu_terminal( parametros )
    
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    FPS = parametros.FPS
    
    pygame.init(  )
    pygame.mixer.init(  )
    clock = pygame.time.Clock(  )
    screen = pygame.display.set_mode( ( SCREEN_WIDTH, SCREEN_HEIGHT ) )
    pygame.display.set_caption( "Agentes" )

    cena = CenaSimulacao( None, parametros )
    Stop_simulation = False

    target = False

    run = True

    while run:
        for event in pygame.event.get(  ):
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                Stop_simulation = not Stop_simulation

            if event.type == pygame.QUIT:
                pygame.quit(  )
                sys.exit(  )

        if not Stop_simulation:
            cena.run(  )
        
        if cena.simulador.estado_simulacao == "FINALIZADA":
            break

        screen.blit( cena.surface, ( 0, 0 ) )

        pygame.display.update(  )
        clock.tick( FPS )