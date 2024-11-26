import pygame
import settings

class Block( pygame.sprite.Sprite ):
    def __init__( self, size, pos, surface = None ):
        super(  ).__init__(  )
        if surface is None:
            self.image = pygame.Surface( size )
            self.image.fill( settings.accent_color )
        else:
            self.image = surface
        
        self.rect = self.image.get_rect( topleft = pos )