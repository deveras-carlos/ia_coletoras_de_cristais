# (-1, -1) (0, 1 ) (1, 1)
# (-1, 0 ) (0, 0 ) (1, 0)
# (-1, -1) (0, -1) (1, -1)

# visao
[
    [ -2, (10, x, y), -1 ],
    [ -2, 0, 50 ],
    [ -2, 20, -1 ]
]

import random

class AgenteSimples:
    def __init__( self, x, y ):
        self.x = x
        self.y = y
        self.direction = ( 0, 0 )
        self.velocidade = 1
        self.visao : list[ list ]= None
        self.parado = False

        self.base_x = None
        self.base_y = None

    def funcao_do_agente_( self ):
        pass

    def nova_direcao( self ):
        self.direction[ 0 ] = random.randint( -1, 1 )
        self.direction[ 1 ] = random.randint( -1, 1 )

    def movimentar( self ):
        if not self.parado:
            self.x += self.direction[ 0 ] * self.velocidade
            self.y += self.direction[ 1 ] * self.velocidade
    
    def acha_base( self ):
        # Usar dijkstra que ignora obstáculos
        pass

    def update( self, visao ):
        if visao[ self.direction[ 0 ] ][ self.direction[ 1 ] ] < -1:
            self.nova_direcao()
            self.parado = True
        else:
            self.parado = False
    
    def run( self ):
        self.movimentar(  )