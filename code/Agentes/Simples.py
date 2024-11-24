import random
from collections import deque

from parametros import Parametro
from .Agente import Agente

class AgenteSimples( Agente ):
    def __init__( self, id : int, parametro : Parametro, mapa,
                 espera_coleta_estrutura_antiga : dict[ tuple[ int ], set[ int ] ],
                  agentes : dict[ int, Agente ] ):
        super(  ).__init__( id, parametro, mapa, espera_coleta_estrutura_antiga, agentes )
        self.direcao_inicial(  )

    def nova_direcao( self, visao = None ):
        if visao is None:
            visao = self.visao
        print( visao )
        index = random.randint( 0, len( visao ) - 1 )
        self.direcao = visao[ index ]
    
    def direcao_inicial( self ):
        if self.carga is None:  # Ensure the agent is not carrying any resource
            if self.parametro.BASE_X <= self.parametro.TAMANHO_MAPA_HORIZONTAL // 2:
                x_corrector = 1
            else:
                x_corrector = -1
            
            if self.parametro.BASE_Y <= self.parametro.TAMANHO_MAPA_VERTICAL // 2:
                y_corrector = -1
            else:
                y_corrector = 1

            directions = [
                (dx, dy) for dx, dy in self.visao 
                if ( self.x + dx + x_corrector , self.y + dy + y_corrector ) not in self.blocos_base
            ]
            self.nova_direcao(directions)