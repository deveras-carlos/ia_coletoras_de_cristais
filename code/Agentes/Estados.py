from collections import deque

from parametros import Parametro
from .Agente import Agente
import random 
class AgenteEstados( Agente ):
    def __init__( self, id : int, parametro : Parametro, mapa,
                 espera_coleta_estrutura_antiga : dict[ tuple[ int ], set[ int ] ],
                  agentes : dict[ int, Agente ] ):
        super(  ).__init__( id, parametro, mapa, espera_coleta_estrutura_antiga, agentes )
        self.visitados = set()
        self.direcao_inicial(  )

    def nova_direcao(self, visao=None):
        """Escolhe uma nova direção com base em locais não visitados."""
        if visao is None:
            visao = self.visao
        if not hasattr(self, 'locais_visitados'):
            self.locais_visitados = set()

        # Adicionar a posição atual como visitada
        self.visitados.add((self.x, self.y))   
        # Filtra direções não visitadas
        direcoes_nao_visitadas = [
            (dx, dy) for dx, dy in visao
            if (self.x + dx, self.y + dy) not in self.visitados
        ]
        
        if direcoes_nao_visitadas:
            # Escolhe aleatoriamente uma direção não visitada
            self.direcao = random.choice(direcoes_nao_visitadas)
        else:
            # Se todas as direções já foram visitadas, escolhe aleatoriamente
            self.direcao = random.choice(visao)
    
    def direcao_inicial(self):
        """Configura a direção inicial evitando blocos base e locais já visitados."""
        if self.carga is None:  # O agente não está carregando nada
            if self.parametro.BASE_X <= self.parametro.TAMANHO_MAPA_HORIZONTAL // 2:
                x_corrector = 1
            else:
                x_corrector = -1

            if self.parametro.BASE_Y <= self.parametro.TAMANHO_MAPA_VERTICAL // 2:
                y_corrector = -1
            else:
                y_corrector = 1
            
            # Filtra direções válidas
            directions = [
                (dx, dy) for dx, dy in self.visao
                if (
                    (self.x + dx + x_corrector, self.y + dy + y_corrector) not in self.blocos_base
                    and (self.x + dx, self.y + dy) not in self.visitados
                )
            ]
            self.nova_direcao(directions)