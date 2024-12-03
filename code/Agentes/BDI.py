from collections import deque

from parametros import Parametro
from .Cooperativo import AgenteCooperativo
import random

class AgenteBDI(AgenteCooperativo):
    def __init__( self, id : int, parametro : Parametro, mapa,
                 espera_coleta_estrutura_antiga : dict[ tuple[ int ], set[ int ] ],
                  agentes : dict, bdi_recursos_descobertos = None ):
        super().__init__(id, parametro, mapa, espera_coleta_estrutura_antiga, agentes, bdi_recursos_descobertos)
        self.recursos_descobertos = self.BDI_recursos_descobertos