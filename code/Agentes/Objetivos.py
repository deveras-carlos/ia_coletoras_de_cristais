from collections import deque

from parametros import Parametro
from .Agente import Agente





class AgenteObjetivos(Agente):
    def __init__(self, id, parametro, mapa, espera_coleta_estrutura_antiga, agentes):
        super().__init__(id, parametro, mapa, espera_coleta_estrutura_antiga, agentes)
        self.recursos_descobertos = set()  # Conjunto para armazenar recursos encontrados
        self.retorno_base = False  # Indica se o agente retornou à base com sucesso
    
    def nova_direcao( self, visao = None ):
        if visao is None:
            visao = self.visao
        print( visao )
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
        if self.carga is not None:
            return
        for utilidade in self.cristais:
            for dx, dy in self.visao:
                pos = (self.x + dx, self.y + dy)
                if pos in self.cristais[utilidade]:
                    self.recursos_descobertos.add(pos)  # Armazena a posição descoberta
                    self.coletar(utilidade, *pos)

    def checa_base(self):
        # Extender a lógica de checar a base para registrar o retorno
        for dx, dy in self.visao:
            if (self.x + dx, self.y + dy) in self.blocos_base:
                if self.carga:
                    self.qtd_cristais[self.carga] += 1
                    self.carga = None
                    self.direcao = None
                    self.path = None
                    self.retorno_base = True  # Marca que retornou à base com sucesso
                if self.carga == self.parametro.UTILIDADE_ESTRUTURA_ANTIGA:
                    self.espera_coleta_estrutura_antiga.pop(self.carga_loc_encontrada)
                    self.carga_loc_encontrada = None

    def movimentar(self):
        # Alterar o comportamento para priorizar recursos conhecidos após o retorno à base
        if self.retorno_base and self.recursos_descobertos:
            destino = self.recursos_descobertos.pop()  # Remove um recurso do conjunto
            self.path = self.bfs(self.mapa, destino)
            if not self.path:
                print(f"Falha ao encontrar caminho para {destino}. Movimento aleatório.")
                self.nova_direcao()
        else:
            self.retorno_base = False  # Reinicia o ciclo após iniciar o movimento para o recurso
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
                    print('Escolhendo nova direção')
                    self.nova_direcao()  # Initialize direction if not set