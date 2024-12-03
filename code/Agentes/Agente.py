from collections import deque

from parametros import Parametro

class Agente:
    def __init__( self, id : int, parametro : Parametro, mapa,
                 espera_coleta_estrutura_antiga : dict[ tuple[ int ], set[ int ] ],
                  agentes : dict, bdi_recursos_descobertos = None ):
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

        self.visao_cristais = [
            # Linha acima da posição central
            (-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2),
            # Linha à esquerda da posição central
            (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1),
            # Linha central
            (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0),
            # Linha à direita da posição central
            (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1),
            # Linha abaixo da posição central
            (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2)
        ]

        # Movimento
        self.parado = True
        self.direcao : tuple[ int ] = None

        # Alvos?
        self.alvo = None

        # Coleta
        self.carga = None
        self.waiting_for_coordinate = None
        self.partners = None

        # Path
        self.path = None
        self.tamanho_path = 0
        self.idx_caminho_base = 0

        # BDI
        if bdi_recursos_descobertos is None:
            self.BDI_recursos_descobertos = list(  )
        else:
            self.BDI_recursos_descobertos = bdi_recursos_descobertos
    
        # Estatísticas
        self.qtd_cristais : dict[ int, int ] = {
            self.parametro.UTILIDADE_CRISTAL_ENERGETICO : 0,
            self.parametro.UTILIDADE_CRISTAL_METAL_RARO : 0,
            self.parametro.UTILIDADE_ESTRUTURA_ANTIGA   : 0
        }

    def checa_cristal( self ):
        if self.carga is not None:
            return
        for utilidade in self.cristais:
            for dx, dy in self.visao_cristais:
                pos = (self.x + dx, self.y + dy)
                if ( self.x + dx, self.y + dy ) in self.cristais[ utilidade ]:
                    if ( utilidade, pos ) not in self.BDI_recursos_descobertos and self.carga:
                        self.BDI_recursos_descobertos.append( ( utilidade, pos ) )
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

    def __coletar_recurso( self, utilidade, x, y ):
        print( f"Agente { self.id } está coletando recurso { utilidade } em { ( x, y ) }" )
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
        self.alvo = None

    def __coletar_estrutura_antiga( self, utilidade, x, y ):
        print( f"Espera no { ( x, y ) } : { self.espera_coleta_estrutura_antiga.get( ( x, y ) ) }" )
        fila_antiga = self.espera_coleta_estrutura_antiga.get( ( x, y ) )
        if ( fila_antiga and self.id not in fila_antiga ) or len( fila_antiga ) > 1:
            while fila_antiga:
                partner_id = fila_antiga.pop(  )
                partner = self.agentes[ partner_id ]
                partner.partner = self.id
                partner.parado = False
                partner.__coletar_recurso( utilidade, x, y )
                self.aguardando_na_coordenada = None
                self.path = None
            self.__coletar_recurso( utilidade, x, y )
        else:
            self.espera_coleta_estrutura_antiga[ ( x, y ) ].add( self.id )
            self.aguardando_na_coordenada = ( x, y )
            self.parado = True
            self.path = None

    def coletar( self, utilidade, x, y ):
        if self.alvo:
            if self.alvo != ( x, y ): return
            if utilidade == self.parametro.UTILIDADE_ESTRUTURA_ANTIGA:
                self.__coletar_estrutura_antiga( utilidade, x, y )
            else:
                self.__coletar_recurso( utilidade, x, y )
        else:
            if self.espera_coleta_estrutura_antiga.get( ( x, y ), None ) is not None:
                self.__coletar_estrutura_antiga( utilidade, x, y )
            elif self.carga is None and utilidade < self.parametro.UTILIDADE_ESTRUTURA_ANTIGA:
                self.__coletar_recurso( utilidade, x, y )
            elif len( self.cristais[ self.parametro.UTILIDADE_CRISTAL_ENERGETICO ] | \
                    self.cristais[ self.parametro.UTILIDADE_CRISTAL_METAL_RARO ] ) > 0:
                return
            else:
                self.__coletar_estrutura_antiga( utilidade, x, y )

    def nova_direcao( self, visao = None ):
        pass

    def direcao_inicial( self ):
        pass

    def colisao( self ):
        if self.direcao!=None:
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
        # print(f'direção {self.direcao}')
        if self.path is not None and self.idx_caminho_base < self.tamanho_path:
            # Move along the path
            x, y = self.path[self.idx_caminho_base]
            self.x, self.y = x, y
            self.idx_caminho_base += 1
            self.parado = False
        elif self.path is not None and self.idx_caminho_base == self.tamanho_path:
            self.path = self.bfs( self.mapa, self.centro_base )
            self.idx_caminho_base = 0
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
            if self.direcao == (0,0) or not self.direcao:
                self.nova_direcao()  # Initialize direction if not set
        else:
            print(f"Agente {self.id} não conseguiu se mover.")
    
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
        
        direcoes = direcoes_carga_simples
        

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
                self.tamanho_path = len(caminho)
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