import pygame
from Scenes.button import Button
from settings import great_color
import os

"""Cena

Cria uma superfície em que tudo será desenhado
Possui um grupo de botões especializados em trocar de cenas

O método 'build' deve ser usado para criar os botões e adicioná-los ao grupo de botões

O método 'run' deve ser usado para realizar as mecânicas daquela cena (desenho e demais funcionalidades)

Esta classe é herdada para a criação das seguintes cenas:

Menu - cena inicial do jogo com botões de play, créditos e sair
CenaSimulacao - cena em que ocorre a simulação.
"""
class Cena:
    def __init__( self, gerenciador_cenas, size ):
        self.gerenciador_cenas = gerenciador_cenas
        self.surface = pygame.Surface( size, pygame.SRCALPHA )
        self.size = size

        self.buttons_set : pygame.sprite.Group = pygame.sprite.Group()

        self.font_button = os.getcwd() + "ACHAR FONTE BOA" # Caminho para fonte

        self.build(  )

    def build( self ):
        pass

    def run( self ):
        self.surface.fill( ( 0, 0, 0 ) )