from parametros import Parametro
from atmosfera import Atmosfera
from mapa import Mapa
from Agentes import Agente, AgenteSimples, AgenteEstados, AgenteObjetivos, AgenteCooperativo, AgenteBDI
from random import randint

class Simulador:
    def __init__(
            self,
            parametro : Parametro
        ):
        self.estado_simulacao = "RODANDO"
        self.parametro = parametro
        self.atmosfera = Atmosfera( self.parametro )
        self.espera_coleta_estrutura_antiga : dict[ tuple[ int ], set[int] ] = dict(  )

        self.agentes : dict[ int, Agente ] = dict(  )

        self.mapa = Mapa( self.parametro, self.agentes )

        self.base_x = self.parametro.BASE_X
        self.base_y = self.parametro.BASE_Y

        self._recursos_descobertos = list(  )

        self.gerar_agentes(  )

    def print_estatisticas( self ):
        total_recursos_coletados = 0
        utilidade_total = 0
        for agente in self.agentes.values(  ):
            utilidade_total += sum( [ util * qtd for util, qtd in agente.qtd_cristais.items(  ) ] )
            total_recursos_coletados += sum( agente.qtd_cristais.values(  ) )
        
        print( "====================================================" )
        print( "Estatísticas Gerais" )
        print( "====================================================" )
        print( f"Total de recursos coletados: { total_recursos_coletados }" )
        print( f"Utilidade total: { utilidade_total }" )
        print( "====================================================" )
        for agente in self.agentes.values(  ):
            print( "----------------------------------------------------" )
            print( f"Dados de coleta do agente { agente.id } - tipo: { type( agente ) }" )
            for recurso in agente.qtd_cristais:
                print( f"Total de recursos coletados do tipo { recurso }: { agente.qtd_cristais[ recurso ] }" )
            print( f"Total de utilidade { sum( [ util * qtd for util, qtd in agente.qtd_cristais.items(  ) ] ) }" )
            print( "----------------------------------------------------" )
        print( "====================================================" )

    def gerar_agentes( self ):
        contar = 0
        for id in range( self.parametro.QTD_AGENTE_BDI ):
            agente = AgenteBDI( id, self.parametro, self.mapa,
                                   self.espera_coleta_estrutura_antiga, self.agentes, self._recursos_descobertos )

            self.agentes[ id ] = agente
            contar += 1
        
        for id in range( contar, contar + self.parametro.QTD_AGENTE_COOPERATIVO ):
            agente = AgenteCooperativo( id, self.parametro, self.mapa,
                                   self.espera_coleta_estrutura_antiga, self.agentes, self._recursos_descobertos )

            self.agentes[ id ] = agente
            contar += 1
        
        for id in range( contar, contar + self.parametro.QTD_AGENTE_OBJETIVOS ):
            agente = AgenteObjetivos( id, self.parametro, self.mapa,
                                   self.espera_coleta_estrutura_antiga, self.agentes, self._recursos_descobertos )

            self.agentes[ id ] = agente
            contar += 1
        
        for id in range( contar, contar + self.parametro.QTD_AGENTE_ESTADOS ):
            agente = AgenteEstados( id, self.parametro, self.mapa,
                                   self.espera_coleta_estrutura_antiga, self.agentes, self._recursos_descobertos )

            self.agentes[ id ] = agente
            contar += 1
        
        for id in range( contar, contar + self.parametro.QTD_AGENTE_SIMPLES ):
            agente = AgenteSimples( id, self.parametro, self.mapa,
                                   self.espera_coleta_estrutura_antiga, self.agentes, self._recursos_descobertos )

            self.agentes[ id ] = agente

    def printar_mapa( self ):
        for l in self.mapa.matriz:
            print( *l )

    def run( self ):
        if self.estado_simulacao == "FINALIZADA":
            return
        self.atmosfera.run(  )
        if self.atmosfera.tempo_final is not None:
            print( "Aconteceu a tempestade!!!" )
            self.estado_simulacao = "FINALIZADA"
            self.print_estatisticas(  )
            
        for agente in self.agentes.values(  ):
            agente.run(  )
            # print( f"Agente { agente.id } está em ( { agente.x }, { agente.y } ), direção: { agente.direcao } e carrega: { agente.carga }" )

        #self.printar_mapa(  )
        # print(  )
