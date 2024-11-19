from dataclasses import dataclass

@dataclass
class Parametro:
    FPS : int = 60

    # Simulação
    QTD_AGENTE_SIMPLES = 1

    TAMANHO_MAPA_HORIZONTAL : int = 10
    TAMANHO_MAPA_VERTICAL : int = 10

    TAMANHO_MAXIMO_OBSTACULOS : int = 10
    QTD_REGIOES_OBSTACULOS : int = 1

    QTD_CRISTAIS_ENERGETICOS : int = 10
    QTD_CRISTAIS_METAL_RARO : int = 5
    QTD_ESTRUTURAS_ANTIGAS : int = 2

    UTILIDADE_CRISTAL_ENERGETICO : int = 10
    UTILIDADE_CRISTAL_METAL_RARO : int = 20
    UTILIDADE_ESTRUTURA_ANTIGA : int = 50
    
    ESPACO_VAZIO : int = -1
    OBSTACULO_PEDRA : int = -2
    BLOCO_BASE : int = -3
    BLOCO_SPAWN : int = -4

    # Visual
    SCREEN_WINDOW_WIDTH = 1280
    SCREEN_WINDOW_HEIGHT = 720