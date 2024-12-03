from collections import deque

from parametros import Parametro
from .Objetivos import AgenteObjetivos
import random

class AgenteCooperativo(AgenteObjetivos):
    def __init__( self, id : int, parametro : Parametro, mapa,
                 espera_coleta_estrutura_antiga : dict[ tuple[ int ], set[ int ] ],
                  agentes : dict, bdi_recursos_descobertos = None ):
        super().__init__(id, parametro, mapa, espera_coleta_estrutura_antiga, agentes, bdi_recursos_descobertos)
        self.estruturas_descobertas = set(  )
        self.prioridades = []
        self.recurso_alvo = None

    def calcular_utilidade(self, recurso, posicao):
        """
        Calcula a utilidade de ajudar a coletar um recurso grande com base na distância
        e no número de agentes disponíveis para essa tarefa.
        """
        distancia = abs(self.x - posicao[0]) + abs(self.y - posicao[1])
        agentes_disponiveis = len(self.espera_coleta_estrutura_antiga.get(posicao, set()))
        # for agente in self.agentes.values(  ):
        #     if agente.carga is None:
        #         agentes_disponiveis += 1
        utilidade = (1 / (distancia + 1)) * ( ( 1 + agentes_disponiveis ) ) * recurso
        return utilidade

    def avaliar_ajuda(self):
        """
        Avalia se vale a pena ajudar outro agente a coletar um recurso grande.
        """
        agentes_livres = 0
        todo_agente_em_estrutura_antiga = True
        for agente in self.agentes.values(  ):
            livre = True
            for pos in self.espera_coleta_estrutura_antiga:
                if agente.id in self.espera_coleta_estrutura_antiga[ pos ]:
                    livre = False
                    break
            if livre:
                todo_agente_em_estrutura_antiga = False
                agentes_livres += 1

        if agentes_livres == 0:
            for agente in self.agentes.values(  ):
                agente.carga = None
                agente.alvo = None
                agente.path = None
                agente.idx_caminho_base = 0
                agente.parado = False

        self.recurso_alvo = None
        melhor_recurso = None
        melhor_utilidade = 0

        for recurso, posicao in self.recursos_descobertos:
            utilidade = self.calcular_utilidade(recurso, posicao)
            if utilidade > melhor_utilidade:
                melhor_utilidade = utilidade
                melhor_recurso = posicao
                self.recurso_alvo = recurso

        if melhor_recurso and self.recurso_alvo == self.parametro.UTILIDADE_ESTRUTURA_ANTIGA:
            if melhor_recurso not in self.cristais.get( self.recurso_alvo ):
                return

            if self.espera_coleta_estrutura_antiga.get( melhor_recurso ) is None:
                self.espera_coleta_estrutura_antiga[ melhor_recurso ] = set(  )
            self.espera_coleta_estrutura_antiga[ melhor_recurso ].add( self.id ) 
            self.path = self.bfs(self.mapa, melhor_recurso)
            self.idx_caminho_base = 0
            self.parado = False
            self.alvo = melhor_recurso
            print(f"Agente {self.id} decidiu ajudar na coleta em {melhor_recurso} com utilidade {melhor_utilidade:.2f}")

    def checa_cristal(self):
        """
        Prioriza ajudar em recursos grandes se não estiver carregando nada.
        """
        if self.carga is None:
            self.avaliar_ajuda()
        
        for utilidade in self.cristais:
            for dx, dy in self.visao_cristais:
                pos = (self.x + dx, self.y + dy)
                if pos in self.cristais[utilidade]:
                    if utilidade == self.parametro.UTILIDADE_ESTRUTURA_ANTIGA:
                        self.estruturas_descobertas.add( ( utilidade, pos ) )
                    if ( utilidade, pos ) not in self.recursos_descobertos and self.carga:
                        self.recursos_descobertos.append( ( utilidade, pos ) )  # Armazena a posição descoberta
                    # print( f"Cristal { utilidade } na posição { pos } encontrado por { self.id }" )
                    self.coletar(utilidade, *pos)

    def checa_base(self):
        """
        Atualiza lógica para priorizar continuar ajudando ou buscar novos cristais.
        """
        for dx, dy in self.visao:
            if (self.x + dx, self.y + dy) in self.blocos_base:
                if self.carga:
                    self.qtd_cristais[self.carga] += 1
                    self.carga = None
                    self.path = None
                    self.direcao = None

                    if self.espera_coleta_estrutura_antiga:
                        self.avaliar_ajuda()

                    # if self.recursos_descobertos:
                    #     utilidade, pos = self.recursos_descobertos.pop(  )
                    #     self.path = self.bfs( self.mapa, pos )
                    #     self.idx_caminho_base = 0
                    # else:
                    #     self.direcao_inicial(  )
                
                    # if self.carga == self.parametro.UTILIDADE_ESTRUTURA_ANTIGA:
                    #     self.espera_coleta_estrutura_antiga.pop( self.carga_loc_encontrada )
                    #     self.carga_loc_encontrada = None

        if self.path:
            return
        
        super(  ).checa_base(  )