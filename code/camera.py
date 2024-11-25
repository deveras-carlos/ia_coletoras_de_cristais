import pygame
from settings import tile_size
import os

class CameraGroup(pygame.sprite.Group):
	def __init__(self, display, surface : pygame.Surface, scenary):
		super().__init__()
		self.display_surface = display

		# camera offset 
		self.offset = pygame.math.Vector2()
		self.half_w = self.display_surface.get_size()[0] // 2
		self.half_h = self.display_surface.get_size()[1] // 2

		# box setup
		self.camera_borders = {'left': 500, 'right': 500, 'top': 250, 'bottom': 250}
		l = self.camera_borders['left']
		t = self.camera_borders['top']
		w = self.display_surface.get_size()[0]  - (self.camera_borders['left'] + self.camera_borders['right'])
		h = self.display_surface.get_size()[1]  - (self.camera_borders['top'] + self.camera_borders['bottom'])
		self.camera_rect = pygame.Rect(l,t,w,h)
		self.camera_rect_base = pygame.Rect( 0, 0, self.display_surface.get_size()[0], self.display_surface.get_size()[1] )

		# scenary
		self.scenary : pygame.sprite.Group = scenary

		# camera speed
		self.keyboard_speed = 5
		self.mouse_speed = 0.2

		# zoom 
		self.internal_surf = surface
		self.internal_surf_size = surface.get_size()
		self.internal_rect = self.internal_surf.get_rect(center = (self.half_w,self.half_h))
		self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surf_size)
		self.internal_offset = pygame.math.Vector2()
		self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
		self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h

	def center_target_camera(self, target):
		self.offset.x = target.rect.centerx - self.half_w
		self.offset.y = target.rect.centery - self.half_h

	def box_target_camera(self,target):
		if target.rect.left < self.camera_rect.left:
			self.camera_rect.left = target.rect.left
		if target.rect.right > self.camera_rect.right:
			self.camera_rect.right = target.rect.right
		if target.rect.top < self.camera_rect.top:
			self.camera_rect.top = target.rect.top
		if target.rect.bottom > self.camera_rect.bottom:
			self.camera_rect.bottom = target.rect.bottom

		self.offset.x = self.camera_rect.left - self.camera_borders['left']
		self.offset.y = self.camera_rect.top - self.camera_borders['top']

	def keyboard_control(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]: self.camera_rect.x -= self.keyboard_speed
		if keys[pygame.K_RIGHT]: self.camera_rect.x += self.keyboard_speed
		if keys[pygame.K_UP]: self.camera_rect.y -= self.keyboard_speed
		if keys[pygame.K_DOWN]: self.camera_rect.y += self.keyboard_speed

		self.offset.x = self.camera_rect.left - self.camera_borders['left']
		self.offset.y = self.camera_rect.top - self.camera_borders['top']

	def mouse_control(self):
		mouse = pygame.math.Vector2(pygame.mouse.get_pos())
		mouse_offset_vector = pygame.math.Vector2()

		left_border = self.camera_borders['left']
		top_border = self.camera_borders['top']
		right_border = self.display_surface.get_size()[0] - self.camera_borders['right']
		bottom_border = self.display_surface.get_size()[1] - self.camera_borders['bottom']

		if top_border < mouse.y < bottom_border:
			if mouse.x < left_border:
				mouse_offset_vector.x = mouse.x - left_border
				pygame.mouse.set_pos((left_border,mouse.y))
			if mouse.x > right_border:
				mouse_offset_vector.x = mouse.x - right_border
				pygame.mouse.set_pos((right_border,mouse.y))
		elif mouse.y < top_border:
			if mouse.x < left_border:
				mouse_offset_vector = mouse - pygame.math.Vector2(left_border,top_border)
				pygame.mouse.set_pos((left_border,top_border))
			if mouse.x > right_border:
				mouse_offset_vector = mouse - pygame.math.Vector2(right_border,top_border)
				pygame.mouse.set_pos((right_border,top_border))
		elif mouse.y > bottom_border:
			if mouse.x < left_border:
				mouse_offset_vector = mouse - pygame.math.Vector2(left_border,bottom_border)
				pygame.mouse.set_pos((left_border,bottom_border))
			if mouse.x > right_border:
				mouse_offset_vector = mouse - pygame.math.Vector2(right_border,bottom_border)
				pygame.mouse.set_pos((right_border,bottom_border))

		if left_border < mouse.x < right_border:
			if mouse.y < top_border:
				mouse_offset_vector.y = mouse.y - top_border
				pygame.mouse.set_pos((mouse.x,top_border))
			if mouse.y > bottom_border:
				mouse_offset_vector.y = mouse.y - bottom_border
				pygame.mouse.set_pos((mouse.x,bottom_border))

		self.offset += mouse_offset_vector * self.mouse_speed

	def draw_ui( self, simulacao, agente ):
		pass

	def custom_draw(self, agente):
		
		# self.center_target_camera(agente) # Sempre segue o centro do personagem
		self.box_target_camera(agente)  # Segue a caixa do personagem
		# self.keyboard_control()		  # Controla a câmera pelo teclado
		# self.mouse_control()			  # Controla a câmera pelo mouse

		self.internal_surf.fill( (20, 20, 20) )
		
		# Rotation
		cam_rect_base = self.camera_rect_base.topleft + self.offset
		agente_display_pos = agente.rect.center - cam_rect_base
		agente.camera_rect_base = cam_rect_base
		mouse_pos = pygame.mouse.get_pos()

		agente_to_mouse = pygame.math.Vector2( mouse_pos[ 0 ] - agente_display_pos[ 0 ], mouse_pos[ 1 ] - agente_display_pos[ 1 ] )
		agente_facing_angle = agente_to_mouse.angle_to( ( 0, -1 ) ) - 180
		agente.image = pygame.transform.rotate( agente.image, agente_facing_angle )

		for sprite in self.scenary[ "ground" ].sprites():
			spr_x = sprite.rect.centerx
			spr_y = sprite.rect.centery
			in_camera_horizontally = spr_x >= cam_rect_base[ 0 ] - tile_size and spr_x <= self.camera_rect_base.right + self.offset[ 0 ] + tile_size
			in_camera_vertically = spr_y >= cam_rect_base[ 1 ] - tile_size and spr_y <= self.camera_rect_base.bottom + self.offset[ 1 ] + tile_size
			if in_camera_horizontally and in_camera_vertically:
				offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
				self.internal_surf.blit(sprite.image, offset_pos)
		
		# active elements
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			spr_x = sprite.rect.centerx
			spr_y = sprite.rect.centery
			in_camera_horizontally = spr_x >= cam_rect_base[ 0 ] - tile_size and spr_x <= self.camera_rect_base.right + self.offset[ 0 ] + tile_size
			in_camera_vertically = spr_y >= cam_rect_base[ 1 ] - tile_size and spr_y <= self.camera_rect_base.bottom + self.offset[ 1 ] + tile_size
			if in_camera_horizontally and in_camera_vertically:
				offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
				self.internal_surf.blit(sprite.image, offset_pos)


		scaled_rect = self.internal_surf.get_rect(center = ( self.half_w, self.half_h ))

		self.display_surface.blit(self.internal_surf, scaled_rect )

		self.draw_ui(  )