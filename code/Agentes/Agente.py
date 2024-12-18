from collections import deque

from parametros import Parametro

class Agente:
    def __init__( self, id : int, parametro : Parametro, mapa,
                 espera_coleta_estrutura_antiga : dict[ tuple[ int ], set[ int ] ],
                  agentes : dict ):
        self.id = id
        self.parametro : Parametro = parametro
        self.mapa : list[ list ] = mapa.matriz
        self.agentes : dict[ int, Agente ] = agentes
        self.cristais : dict[ int, set[ tuple[ int ] ] ] = mapa.cristais
        self.espera_coleta_estrutura_antiga : dict[ tuple[ int ], set[ int ] ] = espera_coleta_estrutura_antiga

        self.centro_base : tuple[ int ] = mapa.centro_base
        self.blocos_base : set[ tuple[ int ] ] = mapa.blocos_base

        self.x : int = mapa.centro_base[ 0 ]
        self.y : int = mapa.centro_base[ 1 ]

        self.visao = [
            ( -1, -1 ),  ( 0, -1 ),  ( 1, -1 ),
            ( -1, 0 ),  ( 0, 0 ),  ( 1, 0 ),
            ( -1, 1 ), ( 0, 1 ), ( 1, 1 )
        ]

        # Movimento
        self.parado = True
        self.direcao : tuple[ int ] = None

        # Alvos?
        self.alvo = None

        # Coleta
        self.carga = None
        self.waiting_for_coordinate = None
        self.partner = None

        # Path
        self.path = None
        self.tamanho_path_base = 0
        self.idx_caminho_base = 0

        # Utilidade
        self.qtd_cristais : dict[ int, int ] = {
            self.parametro.UTILIDADE_CRISTAL_ENERGETICO : 0,
            self.parametro.UTILIDADE_CRISTAL_METAL_RARO : 0,
            self.parametro.UTILIDADE_ESTRUTURA_ANTIGA   : 0
        }
    
    def checa_cristal( self ):
        if self.carga is not None:
            return
        for utilidade in self.cristais:
            for dx, dy in self.visao:
                if ( self.x + dx, self.y + dy ) in self.cristais[ utilidade ]:
                    self.coletar( utilidade, self.x + dx, self.y + dy )
    
    def checa_base( self ):
        for dx, dy in self.visao:
            if ( self.x + dx, self.y + dy ) in self.blocos_base:
                if self.carga:
                    self.qtd_cristais[ self.carga ] += 1
                    self.carga = None
                    self.direcao = None
                    self.direcao_inicial(  )
                    self.path = None
                if self.carga == self.parametro.UTILIDADE_ESTRUTURA_ANTIGA:
                    self.espera_coleta_estrutura_antiga.pop( self.carga_loc_encontrada )
                    self.carga_loc_encontrada = None

    def coletar( self, utilidade, x, y ):
        if self.alvo and ( x, y ) != self.alvo:
            return
        if utilidade < self.parametro.UTILIDADE_ESTRUTURA_ANTIGA:
            self.carga = utilidade
            self.carga_loc_encontrada = ( x, y )
            self.mapa[ x ][ y ] = -1
            self.path = self.bfs( self.mapa, self.centro_base )
            if not self.path:
                print("Fallback to random movement after failed pathfinding.")
                self.nova_direcao()
            self.idx_caminho_base = 0
            if ( x, y ) in self.cristais.get( utilidade ):
                self.cristais.get( utilidade ).remove( ( x, y ) )
        elif not self.alvo and len( self.cristais[ self.parametro.UTILIDADE_CRISTAL_ENERGETICO ] | \
                 self.cristais[ self.parametro.UTILIDADE_CRISTAL_METAL_RARO ] ) > 0:
            return
        else:
            if self.espera_coleta_estrutura_antiga.get( ( x, y ) ):
                self.partner = self.espera_coleta_estrutura_antiga.get( ( x, y ) ).pop(  )
                self.espera_coleta_estrutura_antiga.pop( ( x, y ) )
                partner = self.agentes[ self.partner ]
                partner.partner = self.id
                partner.parado = False
                self.aguardando_na_coordenada = None
            else:
                self.espera_coleta_estrutura_antiga[ ( x, y ) ].add( self.id )
                self.aguardando_na_coordenada = ( x, y )
                self.parado = True
            
            self.carga_loc_encontrada = ( x, y )
            self.carga = utilidade
            self.path = self.bfs( self.mapa, self.centro_base )
            if not self.path:
                print("Fallback to random movement after failed pathfinding.")
                self.nova_direcao()
            self.idx_caminho_base = 0
            self.mapa[ x ][ y ] = -1
            if ( x, y ) in self.cristais.get( utilidade ):
                self.cristais.get( utilidade ).remove( ( x, y ) )

    def nova_direcao( self, visao = None ):
        pass

    def direcao_inicial( self ):
        pass

    def colisao( self ):
        # if not self.parado and self.path and self.idx_caminho_base < self.tamanho_path_base:
        #     return
        
        # novo_x = self.x + self.direcao[ 0 ]
        # novo_y = self.y + self.direcao[ 1 ]

        # if novo_x < 1 or novo_x >= self.parametro.TAMANHO_MAPA_HORIZONTAL or \
        # novo_y < 1 or novo_y >= self.parametro.TAMANHO_MAPA_VERTICAL:
        #     self.nova_direcao(  )
        #     self.parado = True
        #     return

        # if self.mapa[ novo_x ][ novo_y ] == self.parametro.OBSTACULO_PEDRA:
        #     self.nova_direcao(  )
        #     self.parado = True
        # else:
        #     self.parado = False
        novo_x = self.x + self.direcao[0]
        novo_y = self.y + self.direcao[1]

        if not (1 <= novo_x < self.parametro.TAMANHO_MAPA_HORIZONTAL - 1 and \
                 1 <= novo_y < self.parametro.TAMANHO_MAPA_VERTICAL - 1):
            self.nova_direcao()  # Try another direction
            return
        if self.mapa[novo_x][novo_y] == self.parametro.OBSTACULO_PEDRA:
            self.nova_direcao()  # Try another direction
            return
        self.parado = False

    def movimentar( self ):
        # if self.path is not None:
        #     if self.idx_caminho_base < self.tamanho_path_base:
        #         x, y = self.path[ self.idx_caminho_base ]
        #         self.x = x
        #         self.y = y
        #         self.idx_caminho_base += 1
        #         self.parado = False
        #     else:
        #         self.idx_caminho_base = 0
        # elif not self.parado:
        #     self.x += self.direcao[ 0 ]
        #     self.y += self.direcao[ 1 ]
        if self.path is not None and self.idx_caminho_base < self.tamanho_path_base:
            # Move along the path
            x, y = self.path[self.idx_caminho_base]
            self.x, self.y = x, y
            self.idx_caminho_base += 1
            self.parado = False
        elif self.path is None:
            # If no path, fallback to direction-based movement
            if self.direcao:
                novo_x = self.x + self.direcao[0]
                novo_y = self.y + self.direcao[1]
                if (1 <= novo_x < self.parametro.TAMANHO_MAPA_HORIZONTAL - 1 and
                    1 <= novo_y < self.parametro.TAMANHO_MAPA_VERTICAL - 1 and
                    self.mapa[novo_x][novo_y] != self.parametro.OBSTACULO_PEDRA):
                    self.x, self.y = novo_x, novo_y
                    self.parado = False
                else:
                    self.nova_direcao()  # Try a new direction if blocked
            else:
                self.nova_direcao()  # Initialize direction if not set

    # def bfs(self, mapa, destino):
    #     """
    #     Implementa o BFS para encontrar o caminho até uma célula destino.
        
    #     :param mapa: Lista de listas representando o mapa onde -2 são obstáculos.
    #     :param destino: Tupla (x_dest, y_dest) indicando a célula de destino.
    #     :return: Lista de tuplas indicando o caminho do agente até o destino ou None se não houver caminho.
    #     """
    #     direcoes_carga_simples = [
    #         ( -1, 1 ), ( 0, 1 ), ( 1, 1 ),
    #         ( -1, 0 ), ( 1, 0 ),
    #         ( -1, -1 ), ( 0, -1 ), ( 1, -1 )
    #     ]
    #     direcoes_carga_antiga = [
    #         ( -1, 0 ), ( 1, 0 ), ( 0, 1 ), ( 0, -1 )
    #     ]

    #     direcoes = direcoes_carga_antiga if self.carga >= self.parametro.UTILIDADE_ESTRUTURA_ANTIGA else direcoes_carga_simples

    #     filas = deque([(self.x, self.y)])
    #     visitados = set([(self.x, self.y)])
    #     pai = {}  # Armazena o caminho de cada nó

    #     while filas:
    #         atual = filas.popleft()
            
    #         # Se chegarmos ao destino, reconstruímos o caminho
    #         if atual == destino:
    #             caminho = []
    #             while atual in pai:
    #                 caminho.append(atual)
    #                 atual = pai[atual]
    #             caminho.reverse()
    #             caminho = caminho[ :-3 ]
    #             self.tamanho_path_base = len( caminho )
    #             print( caminho )
    #             return caminho
            
    #         # Explorar vizinhos válidos
    #         for dx, dy in direcoes:
    #             nx, ny = atual[0] + dx, atual[1] + dy
                
    #             # Verifica limites do mapa e obstáculos
    #             if (0 < nx < len(mapa) and 0 < ny < len(mapa[0]) and
    #                     mapa[nx][ny] != self.parametro.OBSTACULO_PEDRA and
    #                     (nx, ny) not in visitados):
    #                 filas.append( ( nx, ny ) )
    #                 visitados.add( ( nx, ny ) )
    #                 pai[ ( nx, ny ) ] = atual  # Registra o nó pai
        
    #     # Se não houver caminho
    #     return None
    
    def bfs(self, mapa, destino):
        """
        Implements BFS to find a path to the destination.
        If no path is found, fallback to random direction movement.
        """
        direcoes_carga_simples = [
            (-1, 1), (0, 1), (1, 1),
            (-1, 0), (1, 0),
            (-1, -1), (0, -1), (1, -1)
        ]
        direcoes_carga_antiga = [
            (-1, 0), (1, 0), (0, 1), (0, -1)
        ]

        direcoes = direcoes_carga_antiga if self.carga >= self.parametro.UTILIDADE_ESTRUTURA_ANTIGA else direcoes_carga_simples

        filas = deque([(self.x, self.y)])
        visitados = set([(self.x, self.y)])
        pai = {}  # Tracks the path for each node

        while filas:
            atual = filas.popleft()

            # If destination is reached, reconstruct the path
            if atual == destino:
                caminho = []
                while atual in pai:
                    caminho.append(atual)
                    atual = pai[atual]
                caminho.reverse()
                self.tamanho_path_base = len(caminho)
                return caminho

            # Explore neighbors
            for dx, dy in direcoes:
                nx, ny = atual[0] + dx, atual[1] + dy

                if (0 < nx < len(mapa) and 0 < ny < len(mapa[0]) and
                        mapa[nx][ny] != self.parametro.OBSTACULO_PEDRA and
                        (nx, ny) not in visitados):
                    filas.append((nx, ny))
                    visitados.add((nx, ny))
                    pai[(nx, ny)] = atual

        # If no path is found
        print("No path found, falling back to random movement.")
        self.nova_direcao()  # Fall back to random direction
        return None
    
    def run( self ):
        self.checa_cristal(  )
        self.checa_base(  )
        self.colisao(  )
        self.movimentar(  )