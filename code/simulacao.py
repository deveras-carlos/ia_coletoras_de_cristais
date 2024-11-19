from parametros import Parametro
from random import randint

class Simulacao:
    def __init__(
            self,
            parametro : Parametro
        ):
        self.parametro = parametro
        self.mapa = [
            [ -1 for _ in range( self.parametro.TAMANHO_MAPA_VERTICAL + 2 ) ] \
                for _ in range( self.parametro.TAMANHO_MAPA_HORIZONTAL + 2 )
        ]

        self.gerar_obstaculos(  )

        self.printar_mapa(  )
    
    def gerar_obstaculos( self ):
        for i in range( self.parametro.QTD_REGIOES_OBSTACULOS ):
            tamanho_obstaculo = randint( 1, self.parametro.TAMANHO_MAXIMO_OBSTACULOS )
            bloco_inicial = (
                randint( 1, self.parametro.TAMANHO_MAPA_HORIZONTAL + 1 ),
                randint( 1, self.parametro.TAMANHO_MAPA_VERTICAL + 1 )
            )
            self.mapa[ bloco_inicial[ 0 ] ][ bloco_inicial[ 1 ] ] = self.parametro.OBSTACULO_PEDRA

            print( f"Tamanho do obstáculo: { tamanho_obstaculo }" )
            print( f"Bloco inicial: { bloco_inicial }" )

            bloco_atual = bloco_inicial
            tamanho_atual = 1

            while tamanho_atual <= tamanho_obstaculo:
                direcao = randint( 1, 2 )
                x = randint( 1, 2 )
                y = randint( 1, 2 )

                if x == 1:
                    x = bloco_atual[ 0 ] - 1
                else:
                    x = bloco_atual[ 0 ] + 1
                
                if y == 1:
                    y = bloco_atual[ 1 ] - 1
                else:
                    y = bloco_atual[ 1 ] + 1
                
                if direcao == 1:
                    y = bloco_atual[ 1 ]
                else:
                    x = bloco_atual[ 0 ]

                if self.mapa[ x ][ y ] == self.parametro.ESPACO_VAZIO:
                    bloco_atual = ( x, y )
                    self.mapa[ x ][ y ] = self.parametro.OBSTACULO_PEDRA
                    tamanho_atual += 1

    def printar_mapa( self ):
        for l in self.mapa:
            print( *l )

    def run( self ):
        pass