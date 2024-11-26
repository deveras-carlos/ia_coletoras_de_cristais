from collections import deque

from parametros import Parametro
from .Agente import Agente
import random

class AgenteObjetivos(Agente):
    def __init__(self, id, parametro, mapa, espera_coleta_estrutura_antiga, agentes):
        super().__init__(id, parametro, mapa, espera_coleta_estrutura_antiga, agentes)
        self.recursos_descobertos = list()  # Conjunto para armazenar recursos encontrados
        self.retorno_base = True  # Indica se o agente retornou à base com sucesso
    
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
                    self.coletar(utilidade, *pos)
                    if pos not in self.recursos_descobertos:
                        self.recursos_descobertos.append( ( utilidade, pos ))  # Armazena a posição descoberta
                    print( f"Cristal { utilidade } na posição { pos } encontrado por { self.id }" )

    def checa_base(self):
        # Extender a lógica de checar a base para registrar o retorno
        for dx, dy in self.visao:
            if (self.x + dx, self.y + dy) in self.blocos_base:
                if self.carga:
                    self.qtd_cristais[self.carga] += 1
                    self.carga = None
                    self.direcao = None
                    self.path = None
                if self.carga == self.parametro.UTILIDADE_ESTRUTURA_ANTIGA:
                    self.espera_coleta_estrutura_antiga.pop(self.carga_loc_encontrada)
                    self.carga_loc_encontrada = None
                self.retorno_base = True  # Marca que retornou à base com sucesso

    def movimentar(self):
    # Alterar o comportamento para priorizar recursos conhecidos após o retorno à base
        #print( self.carga )
        #print( self.recursos_descobertos )
        if not self.carga and self.recursos_descobertos:
            utilidade, destino = self.recursos_descobertos.pop(  )  # Remove um recurso do conjunto
            # a=input()
            while self.recursos_descobertos:
                print( self.recursos_descobertos )
                if destino not in self.cristais[ utilidade ]:
                    utilidade, destino = self.recursos_descobertos.pop(  )  # Remove um recurso do conjunto
                else:
                    print(f"AGENTE { self.id } ACHOU UM RECURSO")
                    self.path = self.bfs(self.mapa, destino)
                    self.idx_caminho_base = 0
                    break
            
            # Se não conseguir encontrar o caminho, tenta movimento aleatório
            if not self.path:
                print(f"Falha ao encontrar caminho para {destino}. Movimento aleatório.")
                self.nova_direcao()  # Tenta uma nova direção
        else:
            self.retorno_base = False  # Reinicia o ciclo após iniciar o movimento para o recurso

            # Se há caminho, segue o caminho
            if self.path is not None and self.idx_caminho_base < self.tamanho_path_base:
                x, y = self.path[self.idx_caminho_base]
                self.x, self.y = x, y
                self.idx_caminho_base += 1
                self.parado = False
                # print(f"[Movimento] Agente se moveu para o próximo ponto no caminho: ({x}, {y}).")

            # Caso não haja caminho
            elif self.path is None:
                # Se não tiver caminho, tenta se mover pela direção
                if not self.direcao or self.direcao == (0, 0):
                    # Direção inválida, redefine a direção
                    # print("[Erro] Direção inválida. Tentando redefinir direção.")
                    self.nova_direcao()  # Definir uma nova direção
                
                # Se tiver direção válida, move-se
                novo_x = self.x + self.direcao[0]
                novo_y = self.y + self.direcao[1]

                # Verifica se a nova posição é válida (dentro dos limites e sem obstáculos)
                if (1 <= novo_x < self.parametro.TAMANHO_MAPA_HORIZONTAL - 1 and
                    1 <= novo_y < self.parametro.TAMANHO_MAPA_VERTICAL - 1 and
                    self.mapa[novo_x][novo_y] != self.parametro.OBSTACULO_PEDRA):
                    self.x, self.y = novo_x, novo_y
                    self.parado = False
                    # print(f"[Movimento] Agente se moveu para ({self.x}, {self.y}).")
                else:
                    # Se houver colisão ou a movimentação for inválida, redefine a direção
                    # print(f"[Colisão] Movimentação bloqueada em ({novo_x}, {novo_y}).")
                    self.nova_direcao()  # Tenta uma nova direção
            elif self.path is not None and self.idx_caminho_base == self.tamanho_path_base:
                self.path = self.bfs(self.mapa, ( self.parametro.BASE_X, self.parametro.BASE_Y ) )
                self.idx_caminho_base = 0