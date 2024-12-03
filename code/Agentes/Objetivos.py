from collections import deque

from parametros import Parametro
from .Agente import Agente
import random

class AgenteObjetivos(Agente):
    def __init__( self, id : int, parametro : Parametro, mapa,
                 espera_coleta_estrutura_antiga : dict[ tuple[ int ], set[ int ] ],
                  agentes : dict, bdi_recursos_descobertos = None ):
        super().__init__(id, parametro, mapa, espera_coleta_estrutura_antiga, agentes, bdi_recursos_descobertos)
        self.recursos_descobertos = list()  # Conjunto para armazenar recursos encontrados
    
    def nova_direcao( self, visao = None ):
        if visao is None:
            visao = self.visao
        index = random.randint( 0, len( visao ) - 1 )
        self.direcao = visao[ index ]

    def direcao_inicial(self):
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

    def checa_cristal(self):
        # Extender a lógica de checar cristais para registrar suas posições
        # if self.carga is not None:
        #     return
        for utilidade in self.cristais:
            if utilidade == self.parametro.UTILIDADE_ESTRUTURA_ANTIGA:
                continue
            for dx, dy in self.visao_cristais:
                pos = (self.x + dx, self.y + dy)
                if pos in self.cristais[utilidade]:
                    if ( utilidade, pos ) not in self.recursos_descobertos and self.carga:
                        self.recursos_descobertos.append( ( utilidade, pos ) )  # Armazena a posição descoberta
                    # print( f"Cristal { utilidade } na posição { pos } encontrado por { self.id }" )
                    self.coletar(utilidade, *pos)
    
    def checa_base( self ):
        for dx, dy in self.visao:
            if ( self.x + dx, self.y + dy ) in self.blocos_base:
                if self.carga:
                    self.qtd_cristais[ self.carga ] += 1
                    self.carga = None
                    self.direcao = None
                    self.path = None
                    
                    print( f"Antes: { self.recursos_descobertos }" )
                    if self.recursos_descobertos:
                        utilidade, pos = self.recursos_descobertos.pop(  )
                        self.path = self.bfs( self.mapa, pos )
                        self.idx_caminho_base = 0
                    else:
                        self.direcao_inicial(  )
                    print( f"Depois: { self.recursos_descobertos }" )
                    
                    if self.carga == self.parametro.UTILIDADE_ESTRUTURA_ANTIGA:
                        self.espera_coleta_estrutura_antiga.pop( self.carga_loc_encontrada )
                        self.carga_loc_encontrada = None