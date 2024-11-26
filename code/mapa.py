from Agentes import Agente
from parametros import Parametro

from random import randint

class Mapa:
    def __init__( self, parametro : Parametro, agentes : dict[ int, Agente ] ):
        self.parametro : Parametro = parametro
        self.matriz : list[ list[ int ] ] = [ [ -1 for _ in range( self.parametro.TAMANHO_MAPA_HORIZONTAL + 2 ) ]
                       for _ in range( self.parametro.TAMANHO_MAPA_VERTICAL + 2 ) ]

        self.obstaculos : set = set(  )
        self.cristais   : dict[ int, set[ tuple[ int ] ] ] = {
            self.parametro.UTILIDADE_CRISTAL_ENERGETICO : set(  ),
            self.parametro.UTILIDADE_CRISTAL_METAL_RARO : set(  ),
            self.parametro.UTILIDADE_ESTRUTURA_ANTIGA   : set(  )
        }
        self.agentes    : dict[ int, Agente ] = agentes

        # Base
        self.blocos_base : set = set(  )
        self.centro_base : tuple[ int ] = ( self.parametro.BASE_X, self.parametro.BASE_Y )

        self.gerar_base(  )
        self.gerar_obstaculos(  )
        self.gerar_cristais(  )

    def gerar_base( self ):
        arredores = [
            ( -1, 1 ),  ( 0, 1 ),  ( 1, 1 ),
            ( -1, 0 ),  ( 0, 0 ),  ( 1, 0 ),
            ( -1, -1 ), ( 0, -1 ), ( 1, -1 )
        ]
        for coordenada in arredores:
            x = self.centro_base[ 0 ] + coordenada[ 0 ]
            y = self.centro_base[ 1 ] + coordenada[ 1 ]
            self.matriz[ x ][ y ] = self.parametro.BLOCO_BASE
            self.blocos_base.add( ( x, y ) )

    def gerar_obstaculos( self ):
        for i in range( self.parametro.TAMANHO_MAPA_HORIZONTAL ):
            self.matriz[ 0 ][ i ] = self.parametro.OBSTACULO_PEDRA
            self.matriz[ -1 ][ i ] = self.parametro.OBSTACULO_PEDRA
        
        for i in range( self.parametro.TAMANHO_MAPA_VERTICAL ):
            self.matriz[ i ][ 0 ] = self.parametro.OBSTACULO_PEDRA
            self.matriz[ i ][ -1 ] = self.parametro.OBSTACULO_PEDRA

        qtd_regioes_obstaculos = 0
        while qtd_regioes_obstaculos < self.parametro.QTD_REGIOES_OBSTACULOS:
            tamanho_obstaculo = randint( 1, self.parametro.TAMANHO_MAXIMO_OBSTACULOS )
            bloco_inicial = (
                randint( 1, self.parametro.TAMANHO_MAPA_HORIZONTAL - 2 ),
                randint( 1, self.parametro.TAMANHO_MAPA_VERTICAL - 2 )
            )
            if self.matriz[ bloco_inicial[ 0 ] ][ bloco_inicial[ 1 ] ] == self.parametro.OBSTACULO_PEDRA \
                or self.matriz[ bloco_inicial[ 0 ] ][ bloco_inicial[ 1 ] ] == self.parametro.BLOCO_BASE:
                continue

            self.matriz[ bloco_inicial[ 0 ] ][ bloco_inicial[ 1 ] ] = self.parametro.OBSTACULO_PEDRA

            bloco_atual = bloco_inicial
            tamanho_atual = 1

            self.obstaculos.add( bloco_atual )

            qtd_empacado = 0
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

                if x < 1 or x >= self.parametro.TAMANHO_MAPA_HORIZONTAL or \
                y < 1 or y >= self.parametro.TAMANHO_MAPA_VERTICAL or \
                self.matriz[ x ][ y ] == self.parametro.BLOCO_BASE:
                    if qtd_empacado >= self.parametro.MAXIMO_BLOQUEIOS_GERACAO_OBSTACULOS:
                        bloco_atual = bloco_inicial
                        qtd_empacado = 0
                    qtd_empacado += 1
                    continue

                if self.matriz[ x ][ y ] == self.parametro.ESPACO_VAZIO:
                    bloco_atual = ( x, y )
                    self.matriz[ x ][ y ] = self.parametro.OBSTACULO_PEDRA
                    self.obstaculos.add( bloco_atual )
                    tamanho_atual += 1
            
            qtd_regioes_obstaculos += 1
    
    def gerar_cristais( self ):
        qtd_cristais_energeticos = 0
        while qtd_cristais_energeticos < self.parametro.QTD_CRISTAIS_ENERGETICOS :
            x = randint( 1, self.parametro.TAMANHO_MAPA_HORIZONTAL - 2 )
            y = randint( 1, self.parametro.TAMANHO_MAPA_VERTICAL - 2 )

            if self.matriz[ x ][ y ] != self.parametro.ESPACO_VAZIO:
                continue
            
            self.matriz[ x ][ y ] = self.parametro.UTILIDADE_CRISTAL_ENERGETICO

            self.cristais[ self.parametro.UTILIDADE_CRISTAL_ENERGETICO ].add( ( x, y ) )
            qtd_cristais_energeticos += 1

        
        qtd_cristais_metal_raro = 0
        while qtd_cristais_metal_raro < self.parametro.QTD_CRISTAIS_METAL_RARO :
            x = randint( 1, self.parametro.TAMANHO_MAPA_HORIZONTAL - 2 )
            y = randint( 1, self.parametro.TAMANHO_MAPA_VERTICAL - 2 )

            if self.matriz[ x ][ y ] != self.parametro.ESPACO_VAZIO:
                continue
            
            self.matriz[ x ][ y ] = self.parametro.UTILIDADE_CRISTAL_METAL_RARO

            self.cristais[ self.parametro.UTILIDADE_CRISTAL_METAL_RARO ].add( ( x, y ) )
            qtd_cristais_metal_raro += 1
        
        qtd_estruturas_antigas = 0
        while qtd_estruturas_antigas < self.parametro.QTD_ESTRUTURAS_ANTIGAS :
            x = randint( 1, self.parametro.TAMANHO_MAPA_HORIZONTAL - 2 )
            y = randint( 1, self.parametro.TAMANHO_MAPA_VERTICAL - 2 )

            if self.matriz[ x ][ y ] != self.parametro.ESPACO_VAZIO:
                continue
            
            self.matriz[ x ][ y ] = self.parametro.UTILIDADE_ESTRUTURA_ANTIGA

            self.cristais[ self.parametro.UTILIDADE_ESTRUTURA_ANTIGA ].add( ( x, y ) )
            qtd_estruturas_antigas += 1