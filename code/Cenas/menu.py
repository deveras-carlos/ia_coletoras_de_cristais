import pygame
from .button import Button
from .cena import Cena
from settings import great_color
import os

from parametros import Parametro

class Menu( Cena ):
    def __init__( self, gerenciador_cenas, tamanho : tuple[ int ] ):
        super().__init__( gerenciador_cenas, tamanho )

        self.background = pygame.transform.scale(
            pygame.image.load(
                os.getcwd() + "ACHAR IMAGEM BOA"
            ),
            ( 1280, 720 )
        )
    
    def build( self ):
        pass

    def run( self ):
        self.surface.fill( ( 0, 0, 0 ) )