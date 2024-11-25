import pygame
from .button import Button
from .Cena import Cena
from settings import great_color
import os

class Menu( Cena ):
    def __init__( self, scene_manager, size ):
        super().__init__( scene_manager, size )

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