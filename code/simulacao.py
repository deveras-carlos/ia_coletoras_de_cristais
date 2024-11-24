from parametros import Parametro
from random import randint
from Agentes import Agente, AgenteSimples

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

        self.cristais = list(  )
        self.espera_coleta_estrutura_antiga : dict[ tuple[ int ], int ] = dict(  )

        self.gerar_obstaculos(  )
        self.gerar_cristais(  )

        self.agentes : dict[ int, Agente ] = dict(  )

        self.gerar_agentes(  )

        self.printar_mapa(  )
        print(  )
        self.print_grafo(  )
    
    def gerar_obstaculos( self ):
        for _ in range( self.parametro.QTD_REGIOES_OBSTACULOS ):
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

    def gerar_cristais( self ):
        for _ in range( self.parametro.QTD_CRISTAIS_ENERGETICOS ):
            x = randint( 1, self.parametro.TAMANHO_MAPA_HORIZONTAL )
            y = randint( 1, self.parametro.TAMANHO_MAPA_VERTICAL )

            while self.mapa[ x ][ y ] == self.parametro.OBSTACULO_PEDRA:
                x = randint( 1, self.parametro.TAMANHO_MAPA_HORIZONTAL )
                y = randint( 1, self.parametro.TAMANHO_MAPA_VERTICAL )
            
            self.mapa[ x ][ y ] = self.parametro.UTILIDADE_CRISTAL_ENERGETICO

            self.cristais.append( ( self.parametro.UTILIDADE_CRISTAL_ENERGETICO, x, y ) )
        
        for _ in range( self.parametro.QTD_CRISTAIS_METAL_RARO ):
            x = randint( 1, self.parametro.TAMANHO_MAPA_HORIZONTAL )
            y = randint( 1, self.parametro.TAMANHO_MAPA_VERTICAL )

            while self.mapa[ x ][ y ] == self.parametro.OBSTACULO_PEDRA:
                x = randint( 1, self.parametro.TAMANHO_MAPA_HORIZONTAL )
                y = randint( 1, self.parametro.TAMANHO_MAPA_VERTICAL )
            
            self.mapa[ x ][ y ] = self.parametro.UTILIDADE_CRISTAL_METAL_RARO

            self.cristais.append( ( self.parametro.UTILIDADE_CRISTAL_METAL_RARO, x, y ) )

        for _ in range( self.parametro.QTD_ESTRUTURAS_ANTIGAS ):
            x = randint( 1, self.parametro.TAMANHO_MAPA_HORIZONTAL )
            y = randint( 1, self.parametro.TAMANHO_MAPA_VERTICAL )

            while self.mapa[ x ][ y ] == self.parametro.OBSTACULO_PEDRA:
                x = randint( 1, self.parametro.TAMANHO_MAPA_HORIZONTAL )
                y = randint( 1, self.parametro.TAMANHO_MAPA_VERTICAL )
            
            self.mapa[ x ][ y ] = self.parametro.UTILIDADE_ESTRUTURA_ANTIGA
            
            self.cristais.append( ( self.parametro.UTILIDADE_ESTRUTURA_ANTIGA, x, y ) )
            self.espera_coleta_estrutura_antiga[ ( x, y ) ] = None

    def gerar_agentes( self ):
        for id in range( self.parametro.QTD_AGENTE_SIMPLES ):
            x = randint( 1, self.parametro.TAMANHO_MAPA_HORIZONTAL )
            y = randint( 1, self.parametro.TAMANHO_MAPA_VERTICAL )

            while self.mapa[ x ][ y ] == self.parametro.OBSTACULO_PEDRA:
                x = randint( 1, self.parametro.TAMANHO_MAPA_HORIZONTAL )
                y = randint( 1, self.parametro.TAMANHO_MAPA_VERTICAL )
            
            self.mapa[ x ][ y ] = self.parametro.AGENTE_SIMPLES_MAPA_ID
            
            agente = AgenteSimples( id, self.parametro, self.mapa, x, y, self.base_x, self.base_y,
                                   self.espera_coleta_estrutura_antiga, self.agentes )

            self.agentes[ id ] = agente

    def printar_mapa( self ):
        for l in self.mapa:
            print( *l )

    def print_grafo( self ):
        for l in self.grafo_mapa:
            print( *l )

    def run( self ):
        pass