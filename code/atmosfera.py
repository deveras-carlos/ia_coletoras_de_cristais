import pygame

from parametros import Parametro

class Atmosfera:
    def __init__( self, parametro : Parametro ):
        self.parametro : Parametro = parametro
        self.tempo_inicial = pygame.time.get_ticks(  )
        self.tempo_atual = None

        self.tempo_final = None

    def run( self ):
        self.tempo_atual = pygame.time.get_ticks(  )

        if self.tempo_atual - self.tempo_inicial > self.parametro.DURACAO_CICLO_TEMPESTADE:
            self.tempo_final = self.tempo_atual