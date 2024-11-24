import random
from collections import deque

from ..parametros import Parametro
from .Agente import Agente

class AgenteSimples:
    def __init__( self, id : int, parametro : Parametro, mapa, x, y, base_x, base_y,
                 espera_coleta_estrutura_antiga : dict[ tuple[ int ], set[ int ] ],
                  agentes : dict[ int, Agente ] ):
        self.id = id
        self.parametro : Parametro = parametro
        self.mapa : list[ list ] = mapa
        self.agentes : dict[ int, Agente ] = agentes

        self.x = x
        self.y = y

        self.direcao = ( 0, 0 )
        self.parado = False

        self.base_x = base_x
        self.base_y = base_y

        self.espera_coleta_estrutura_antiga : dict[ tuple[ int ], int ] = espera_coleta_estrutura_antiga

        self.carga_loc_encontrada : tuple[ int ] = None
        self.carga : int = None

        self.caminho_base : list[ tuple[ int ] ] = None
        self.tamanho_caminho_base : int = None
        self.idx_caminho_base : int = 0

        self.pontuacao_total : int = 0

    def nova_direcao( self ):
        self.direcao[ 0 ] = random.randint( -1, 1 )
        self.direcao[ 1 ] = random.randint( -1, 1 )

    def movimentar( self ):
        if self.caminho_base is not None:
            if self.idx_caminho_base < self.tamanho_caminho_base:
                x, y = self.caminho_base[ self.idx_caminho_base ]
                self.x = x
                self.y = y
                self.idx_caminho_base += 1
                self.parado = False
        elif not self.parado:
            self.x += self.direcao[ 0 ]
            self.y += self.direcao[ 1 ]

    def bfs(self, mapa, destino):
        """
        Implementa o BFS para encontrar o caminho até uma célula destino.
        
        :param mapa: Lista de listas representando o mapa onde -2 são obstáculos.
        :param destino: Tupla (x_dest, y_dest) indicando a célula de destino.
        :return: Lista de tuplas indicando o caminho do agente até o destino ou None se não houver caminho.
        """
        direcoes_carga_simples = [
            ( -1, 1 ), ( 0, 1 ), ( 1, 1 ),
            ( -1, 0 ), ( 1, 0 ),
            ( -1, -1 ), ( 0, -1 ), ( 1, -1 )
        ]
        direcoes_carga_antiga = [
            ( -1, 0 ), ( 1, 0 ), ( 0, 1 ), ( 0, -1 )
        ]

        direcoes = direcoes_carga_antiga if self.carga >= self.parametro.UTILIDADE_ESTRUTURA_ANTIGA else direcoes_carga_simples

        filas = deque([(self.x, self.y)])
        visitados = set([(self.x, self.y)])
        pai = {}  # Armazena o caminho de cada nó

        while filas:
            atual = filas.popleft()
            
            # Se chegarmos ao destino, reconstruímos o caminho
            if atual == destino:
                caminho = []
                while atual in pai:
                    caminho.append(atual)
                    atual = pai[atual]
                caminho.reverse()
                return caminho
            
            # Explorar vizinhos válidos
            for dx, dy in direcoes:
                nx, ny = atual[0] + dx, atual[1] + dy
                
                # Verifica limites do mapa e obstáculos
                if (0 < nx < len(mapa) and 0 < ny < len(mapa[0]) and
                        mapa[nx][ny] != self.parametro.OBSTACULO_PEDRA and
                        (nx, ny) not in visitados):
                    filas.append( ( nx, ny ) )
                    visitados.add( ( nx, ny ) )
                    pai[ ( nx, ny ) ] = atual  # Registra o nó pai
        
        # Se não houver caminho
        return None

    def colisao( self ):
        novo_x = self.x + self.direcao[ 0 ]
        novo_y = self.y + self.direcao[ 1 ]
        if self.caminho_base:
            novo_x, novo_y = self.caminho_base[ self.idx_caminho_base ]
        if self.mapa[ novo_x ][ novo_y ] == self.parametro.OBSTACULO_PEDRA:
            self.nova_direcao()
            self.parado = True
        elif self.mapa[ novo_x ][ novo_y ] > self.parametro.ESPACO_VAZIO and self.carga is None:
            if self.mapa[ novo_x ][ novo_y ] < self.parametro.UTILIDADE_ESTRUTURA_ANTIGA:
                self.carga = self.mapa[ novo_x ][ novo_y ]
                self.mapa[ novo_x ][ novo_y ] = self.parametro.ESPACO_VAZIO
                self.parado = False
            else:
                self.carga_loc_encontrada = ( novo_x, novo_y )
                em_espera = self.espera_coleta_estrutura_antiga[ ( novo_x, novo_y ) ]
                if em_espera == None:
                    self.espera_coleta_estrutura_antiga[ ( novo_x, novo_y ) ] = self.id
                    self.parado = True
                else:
                    agente_em_espera = self.agentes[ em_espera ]
                    self.caminho_base = self.bfs( self.mapa, ( self.base_x, self.base_y ) )
                    agente_em_espera.caminho_base = agente_em_espera.bfs( agente_em_espera.mapa, ( agente_em_espera.base_x, agente_em_espera.base_y ) )
                    agente_em_espera.parado = False
                    self.parado = False
        elif self.carga and self.mapa[ self.x ][ self.y ] == self.parametro.BLOCO_BASE:
            self.pontuacao_total += self.carga
            self.carga = None
            if self.carga_loc_encontrada:
                self.espera_coleta_estrutura_antiga.pop( self.carga_loc_encontrada )
                self.carga_loc_encontrada = None
            self.nova_direcao(  )
            self.parado = False
        else:
            self.parado = False
    
    def run( self ):
        self.colisao(  )
        self.movimentar(  )