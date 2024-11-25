import pygame

# Define um botão baseado no tamanho do texto em questão
class Botao( pygame.sprite.Sprite ):
    def __init__(self,
                 text,
                 font,
                 font_size,
                 color,
                 position, scene_manager, new_state, sprite = None, sprite_pos = None):
        super().__init__()
        self.text = text
        self.font = pygame.font.Font(font, font_size)
        self.color = color
        self.position = position
        self.scene_manager = scene_manager

        self.image = self.font.render(self.text, False, self.color, (240, 230, 240) )
        self.rect = self.image.get_rect(center=self.position)
    
        self.new_state = new_state

    def notify_scene( self ):
        self.scene_manager.estado = self.new_state

    def handle_event( self ):
        self.notify_scene(  )