import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, tile_size
from Cenas import Cena, CenaMenu, CenaSimulacao

from parametros import Parametro

class SceneManager:
    def __init__( self ):
        # Screen
        self.screen = pygame.display.set_mode( ( SCREEN_WIDTH, SCREEN_HEIGHT ) )

        # self.icon = pygame.image.load( path_icon ).convert_alpha()

        # pygame.display.set_icon( self.icon )
        pygame.display.set_caption( "Agentes coletores de recursos" )

        self.current_scene : Cena = None
        self.current_scene_pos : tuple[ int, int ] = None

        self.parametros : Parametro = None

        self.backup_scene = None

        self.click_button_start = pygame.time.get_ticks()
        self.click_button_time_delay = 400 # Número mágico. Consertar depois
        
        self.state = "start"

    def listen_input( self, mouse_pos, mouse_pressed, keys ):
        if not mouse_pressed[ 0 ]: # Se o botão esquerdo do mouse não estiver sendo pressionado, não faz nada
            return

        # Checa se cada botão da cena foi clicado
        # Se sim, chama o método "handle_event" de cada botão clicado
        for button in self.current_scene.buttons_set:
            if button.rect.collidepoint( mouse_pos[ 0 ], mouse_pos[ 1 ] ):

                current = pygame.time.get_ticks() # Pega o tempo atual do jogo
                if not ( current - self.click_button_start > self.click_button_time_delay ):
                    continue # Pula se o tempo entre o clique atual e o anterior for muito pequeno
                
                self.click_button_start = current # Atualiza o tempo do "último" clique
                button.handle_event()

    def run( self ):

        match self.state:
            case "start":
                self.current_scene = CenaMenu( self, ( SCREEN_WIDTH, SCREEN_HEIGHT ) )
                self.state = "menu"
            case "menu":
                pass
            case "loading":
                self.backup_scene = self.current_scene
                self.current_scene = CenaSimulacao( self, self.parametros )
            case "simulation":
                pass
            case _:
                self.current_scene = Cena( self, ( SCREEN_WIDTH, SCREEN_HEIGHT ) )

        self.current_scene.run(  )

        self.screen.blit( self.current_scene.surface, ( 0, 0 ) )