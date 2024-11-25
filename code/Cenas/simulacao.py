import pygame
from .button import Button
from .cena import Cena
from settings import great_color, tile_size
from tile import Block

from parametros import Parametro
from simulador import Simulador
from camera import CameraGroup

class Simulacao( Cena ):
    def __init__( self, gerenciador_cenas, parametros : Parametro ):
        super().__init__( gerenciador_cenas, ( parametros.TAMANHO_MAPA_HORIZONTAL * tile_size, parametros.TAMANHO_MAPA_VERTICAL * tile_size ) )
        self.parametros = parametros
        self.simulacao = Simulador( self.parametros )

        self.cenario = {
            "BACKGROUND" : pygame.sprite.Group(  )
        }

        self.camera = CameraGroup( gerenciador_cenas.screen, self.surface,  )
    
    def build( self ):
        pass

    def run( self ):
        
        # Logic
        self.simulacao.run(  )

        # Visuals
        self.surface.fill( ( 0, 0, 0 ) )