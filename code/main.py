import sys
import pygame

from scene_manager import SceneManager

if __name__ == "__main__":
    pygame.init(  )
    pygame.mixer.init(  )
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    FPS = 1
    clock = pygame.time.Clock(  )
    screen = pygame.display.set_mode( ( SCREEN_WIDTH, SCREEN_HEIGHT ) )
    pygame.display.set_caption( "Agentes" )
    gerenciador_cenas = SceneManager(  )

    while True:
        for event in pygame.event.get(  ):
            if event.type == pygame.QUIT:
                pygame.quit(  )
                sys.exit(  )
        
        gerenciador_cenas.run(  )

        pygame.display.update(  )
        clock.tick( FPS )