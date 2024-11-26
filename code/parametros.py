from dataclasses import dataclass

@dataclass
class Parametro:
    FPS : int = 60

    # Simulação
    QTD_AGENTE_SIMPLES = 4

    AGENTE_SIMPLES_MAPA_ID = -10

    TAMANHO_MAPA_HORIZONTAL : int = 100
    TAMANHO_MAPA_VERTICAL : int = 100

    TAMANHO_MAXIMO_OBSTACULOS : int = 15
    QTD_REGIOES_OBSTACULOS : int = 10

    QTD_CRISTAIS_ENERGETICOS : int = 20
    QTD_CRISTAIS_METAL_RARO : int = 10
    QTD_ESTRUTURAS_ANTIGAS : int = 5

    UTILIDADE_CRISTAL_ENERGETICO : int = 10
    UTILIDADE_CRISTAL_METAL_RARO : int = 20
    UTILIDADE_ESTRUTURA_ANTIGA : int = 50
    
    ESPACO_VAZIO : int = -1
    OBSTACULO_PEDRA : int = -2
    BLOCO_BASE : int = -3
    BLOCO_SPAWN : int = -4

    MAXIMO_BLOQUEIOS_GERACAO_OBSTACULOS : int = 10

    DURACAO_CICLO_TEMPESTADE : int = 120_000

    # Base
    BASE_X : int = 1
    BASE_Y : int = 1