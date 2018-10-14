from game_model import *
from game_view import *
import random, sys, time, pygame
from pygame.locals import *

FRAME_PER_SEC = 7
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20

assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."

# number of cells
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

WHITE = (255, 255, 255)
BLACK = ( 0, 0, 0)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
DARKGREEN = ( 0, 155, 0)
DARKGRAY = ( 40, 40, 40)
BGCOLOR = BLACK

class Controller:
	def __init__(self):
		self.board = Board(CELLWIDTH, CELLHEIGHT)
		self.apple = Apple(self.board)
		self.snake = Snake(3, self.board, self.apple)
		self.view = GameView(WINDOWWIDTH, WINDOWHEIGHT)
		self.fps_clock = pygame.time.Clock()
	def show_start_screen(self):
		self.view.draw_background(BGCOLOR)
		self.view.draw_text('Wormy!', GREEN, pygame.font.SysFont("comicsansms", 100), Position(WINDOWWIDTH / 2, WINDOWHEIGHT / 2), "center")
		self.view.draw_text('Press a key to play.', RED, pygame.font.SysFont("comicsansms", 18), Position(WINDOWWIDTH - 200, WINDOWHEIGHT - 30), "topleft")
		self.view.update_display()
    
		while True:
			if self.__check_for_key_press():
				pygame.event.get()
				return

	def run_game(self):
		self.snake = Snake(3, self.board, self.apple)
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					self.__terminate()
				elif event.type == KEYDOWN:
					if event.key == K_LEFT or event.key == K_a:
						self.snake.change_direction(Direction.LEFT)
					elif event.key == K_RIGHT or event.key == K_d:
						self.snake.change_direction(Direction.RIGHT)
					elif event.key == K_UP or event.key == K_w:
						self.snake.change_direction(Direction.UP)
					elif event.key == K_DOWN or event.key == K_s:
						self.snake.change_direction(Direction.DOWN)
					elif event.key == K_ESCAPE:
						self.__terminate()

			# move the snake
			if not self.snake.move():
				return

			self.update_game_stats_on_screen(self.apple.apple_position(), self.snake.get_snake_positions())
				
			# set frame per second
			self.fps_clock.tick(FRAME_PER_SEC)
    
	def update_game_stats_on_screen(self, _apple_position, _snake_positions):
		self.view.draw_background(BGCOLOR)

		# draw grid
		self.view.draw_grid(DARKGRAY, WINDOWWIDTH, WINDOWHEIGHT, CELLSIZE)

		# draw apple
		self.view.draw_cell(_apple_position, CELLSIZE, RED)
        
        # draw snake
		self.view.draw_list_of_cells(_snake_positions, CELLSIZE, DARKGREEN)
        
		self.view.draw_text('Score: %s' % (len(_snake_positions) - 3), WHITE, pygame.font.SysFont("comicsansms", 18), Position(WINDOWWIDTH - 120, 10), "topleft")

		self.view.update_display()

	def __terminate(self):
		pygame.quit()
		sys.exit()

	def __check_for_key_press(self):
		if len(pygame.event.get(QUIT)) > 0:
			self.__terminate()
		key_up_events = pygame.event.get(KEYUP)
		if len(key_up_events) == 0:
			return None
		if key_up_events[0].key == K_ESCAPE:
			self.__terminate()
		return key_up_events[0].key

	def show_gameover_screen(self):
		self.view.draw_text('Game Over', WHITE, pygame.font.SysFont("comicsansms", 50), Position(WINDOWWIDTH/2,  WINDOWHEIGHT/2), "midtop")
		self.view.update_display()
		pygame.time.wait(500)
		self.__check_for_key_press()

		while True:
			if self.__check_for_key_press():
				pygame.event.get()
				return

if __name__ == '__main__':
	pygame.init()
	controller = Controller()
	controller.show_start_screen()
    
	while True:  
		controller.run_game()
		controller.show_gameover_screen()
