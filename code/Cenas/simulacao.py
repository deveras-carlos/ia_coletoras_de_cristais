import pygame
# from .button import Button
from .cena import Cena
from settings import great_color, tile_size
from tile import Block

from parametros import Parametro
from simulador import Simulador
from camera import CameraGroup
from Agentes import Agente, AgenteSimples

class Simulacao( Cena ):
    def __init__( self, gerenciador_cenas, parametros : Parametro ):
        super().__init__( gerenciador_cenas, ( parametros.TAMANHO_MAPA_HORIZONTAL * tile_size, parametros.TAMANHO_MAPA_VERTICAL * tile_size ) )
        self.parametros = parametros
        self.simulador : Simulador = Simulador( self.parametros )

        self.camadas = {
            "BACKGROUND" : pygame.sprite.Group(  ),
            "RECURSOS" : pygame.sprite.Group(  ),
            "AGENTES" : dict(  )
        }

        self.camera = CameraGroup( gerenciador_cenas.screen, self.surface, self.camadas )

        self.build(  )

        print( self.simulador.agentes )
        self.target = self.camadas[ "AGENTES" ][ 0 ]
    
    def build( self ):
        mapa = self.simulador.mapa.matriz
        
        # Mapa
        for x in range( self.parametros.TAMANHO_MAPA_VERTICAL + 2):
            for y in range( self.parametros.TAMANHO_MAPA_HORIZONTAL + 2 ):
                pos_x = x * tile_size
                pos_y = y * tile_size
                pos = ( pos_x, pos_y )
                if mapa[ x ][ y ] == self.parametros.OBSTACULO_PEDRA:
                    surface = None
                elif mapa[ x ][ y ] == self.parametros.BLOCO_BASE:
                    surface = None
                else:
                    surface = None
                bloco = Block( ( tile_size, tile_size ), pos, surface )
                self.camadas[ "BACKGROUND" ].add( bloco )

                if mapa[ x ][ y ] <= self.parametros.ESPACO_VAZIO:
                    continue

                if mapa[ x ][ y ] == self.parametros.UTILIDADE_CRISTAL_ENERGETICO:
                    surface = None
                elif mapa[ x ][ y ] == self.parametros.UTILIDADE_CRISTAL_ENERGETICO:
                    surface = None
                elif mapa[ x ][ y ] == self.parametros.UTILIDADE_CRISTAL_ENERGETICO:
                    surface = None

                recurso = Block( ( tile_size, tile_size ), pos, surface )
                self.camadas[ "RECURSOS" ].add( recurso )
        
        # Agentes
        for id_agente in self.simulador.agentes:
            agente = self.simulador.agentes[ id_agente ]
            surface = None
            if isinstance( agente, AgenteSimples ):
                surface = None
            # elif isinstance( agente,  ):
            #     surface = None
            
            pos = ( agente.x * tile_size, agente.y * tile_size )

            self.camadas[ "AGENTES" ][ id_agente ] = Block( ( tile_size, tile_size ), pos, surface )

    def run( self ):
        
        # Logic
        self.simulador.run(  )
        for id_agente in self.simulador.agentes:
            agente = self.simulador.agentes[ id_agente ]
            pos = ( agente.x * tile_size, agente.y * tile_size )
            self.camadas[ "AGENTES" ][ id_agente ].rect.topleft = pos
        
        for recurso in self.camadas[ "RECURSOS" ]:
            pos =  ( recurso.rect.topleft[ 0 ] // tile_size, recurso.rect.topleft[ 1 ] // tile_size )
            existe_recurso = False
            for cris in self.simulador.mapa.cristais:
                if pos in self.simulador.mapa.cristais[ cris ]:
                    existe_recurso = True
                    break
            
            if not existe_recurso:
                recurso.kill(  )

        # Visuals
        self.surface.fill( ( 0, 0, 0 ) )

        self.camera.custom_draw( self.target )