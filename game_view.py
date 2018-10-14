import pygame

class GameView:
	def __init__(self, _window_width, _window_height):
		self.display_surf = pygame.display.set_mode((_window_width, _window_height))

	def update_display(self):
		pygame.display.update()

	def draw_background(self, _color):
		self.display_surf.fill(_color)

	def draw_grid(self, _color, _width, _height, _cell_size):
		for x in range(0, _width, _cell_size): # draw vertical lines
			pygame.draw.line(self.display_surf, _color, (x, 0), (x, _height))
		for y in range(0, _height, _cell_size): # draw horizontal lines
			pygame.draw.line(self.display_surf, _color, (0, y), (_width, y))

	def draw_cell(self, _cell_position, _cell_size, _color):
		x = _cell_position.getX() * _cell_size
		y = _cell_position.getY() * _cell_size
		cell_rect = pygame.Rect(x, y, _cell_size, _cell_size)
		pygame.draw.rect(self.display_surf, _color, cell_rect)

	def draw_list_of_cells(self, _cell_positions, _cell_size, _color):
		for pos in _cell_positions:
			self.draw_cell(pos, _cell_size, _color)
		
	def draw_text(self, _text, _color, _font, _pos, _pos_type):
		text_surf = _font.render(_text, True, _color)
		text_rect = text_surf.get_rect()
		if _pos_type == "midtop":
			text_rect.midtop = (_pos.getX(), _pos.getY())
		elif _pos_type == "topleft":
			text_rect.topleft = (_pos.getX(), _pos.getY())
		elif _pos_type == "center":
			text_rect.center = (_pos.getX(), _pos.getY())
		else:
			raise ValueError('Unexpected position type: ' + _pos_type)
		self.display_surf.blit(text_surf, text_rect)