from parametros import Parametro
from mapa import Mapa
from random import randint
from Agentes import Agente, AgenteSimples
from Agentes.Estados import AgenteEstados
from Agentes.Objetivos import AgenteObjetivos
class Simulacao:
    def __init__(
            self,
            parametro : Parametro
        ):
        self.parametro = parametro
        self.espera_coleta_estrutura_antiga : dict[ tuple[ int ], int ] = dict(  )

        self.agentes : dict[ int, Agente ] = dict(  )

        self.mapa = Mapa( self.parametro, self.agentes )

        self.base_x = self.parametro.BASE_X
        self.base_y = self.parametro.BASE_Y

        self.gerar_agentes(  )

    def gerar_agentes( self ):
        for id in range( self.parametro.QTD_AGENTE_SIMPLES ):
            agente = AgenteSimples( id, self.parametro, self.mapa,
                                   self.espera_coleta_estrutura_antiga, self.agentes )

            self.agentes[ id ] = agente

    def printar_mapa( self ):
        for l in self.mapa.matriz:
            print( *l )

    def run( self ):
        for agente in self.agentes.values(  ):
            agente.run(  )
            print( f"Agente { agente.id } está em ( { agente.x }, { agente.y } ), direção: { agente.direcao } e carrega: { agente.carga }" )

        self.printar_mapa(  )
        print(  )