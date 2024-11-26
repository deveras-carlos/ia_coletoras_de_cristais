import sys
import pygame

from scene_manager import SceneManager

if __name__ == "__main__":
    pygame.init(  )
    pygame.mixer.init(  )
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    FPS = 5
    clock = pygame.time.Clock(  )
    screen = pygame.display.set_mode( ( SCREEN_WIDTH, SCREEN_HEIGHT ) )
    pygame.display.set_caption( "Agentes" )
    gerenciador_cenas = SceneManager(  )
    Stop_simulation=False
    while True:
        for event in pygame.event.get(  ):
            if event.type==pygame.KEYDOWN:
                Stop_simulation= not Stop_simulation
            
            if event.type == pygame.QUIT:
                pygame.quit(  )
                sys.exit(  )
        if not Stop_simulation:
            gerenciador_cenas.run(  )

        pygame.display.update(  )
        clock.tick( FPS )