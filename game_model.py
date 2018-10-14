from enum import Enum
import random

class Direction(Enum):
	LEFT = 1
	RIGHT = 2
	UP = 3
	DOWN = 4

class Position:
	def __init__(self, _x, _y):
		self.x = _x
		self.y = _y
	def __str__(self):
		return " Position(" + str(self.x) + "," + str(self.y) + ") "
	def __eq__(self, obj):
		return self.x == obj.x and self.y == obj.y
	def getX(self):
		return self.x
	def getY(self):
		return self.y

class Apple:
	def __init__(self, _board):
		self.board = _board
		self.__generate_apple()
	def maybe_eat_apple(self, _position):
		if self.position == _position:
			self.__generate_apple()
			return True
		else:
			return False
	def apple_position(self):
		return self.position
	def __generate_apple(self):
		self.position = Position(random.randint(0, self.board.getWidth() - 1), random.randint(0, self.board.getHeight() - 1))

class Board:
	def __init__(self, _board_width, _board_height):
		self.board_width = _board_width
		self.board_height = _board_height
	def getWidth(self):
		return self.board_width
	def getHeight(self):
		return self.board_height

class Snake:
	def __init__(self, _snake_length, _board, _apple):
		# apple
		self.apple = _apple
		# board
		self.board = _board
		# snake body
		startx = random.randint(_snake_length * 2, _board.getWidth() - _snake_length * 2)
		starty = random.randint(_snake_length * 2, _board.getHeight() - _snake_length * 2)
		self.body = [Position(startx, starty), Position(startx, starty + 1), Position(startx, starty + 2)]
		# current direction
		self.direction = Direction.LEFT
	def __str__(self):
		result = "snake: "
		for part in self.body:
			result += str(part)
		return result
	def get_snake_positions(self):
		return self.body
	def move(self):
		'''
		move in self.direction once
		'''
		next_head_position = self.__get_postion_given_direction(self.body[0], self.direction)
		#self.body = [next_head_position] + self.body[:-1]
		if next_head_position in self.body[:-1]:
			print 'touch itself'
			return False
		if self.__reach_boundary(next_head_position):
			print "reach boundary"
			return False
		if self.apple.maybe_eat_apple(next_head_position):
			self.body = [next_head_position] + self.body
		else:
			self.body = [next_head_position] + self.body[:-1]
		return True
	def change_direction(self, _direction):
		'''
		change current direction
		'''
		if self.__is_invalid_next_direction(_direction):
			print "invalid next direction, keep current direction: ", _direction
			return
		self.direction = _direction
	def __is_invalid_next_direction(self, _direction):
		next_position = self.__get_postion_given_direction(self.body[0], _direction)
		return next_position == self.body[1]
	def __get_postion_given_direction(self, old_position, direction):
		if direction == Direction.LEFT:
			return Position(old_position.getX() - 1, old_position.getY())
		elif direction == Direction.RIGHT:
			return Position(old_position.getX() + 1, old_position.getY())
		elif direction == Direction.UP:
			return Position(old_position.getX(), old_position.getY() - 1)
		else:
			assert(direction == Direction.DOWN)
			return Position(old_position.getX(), old_position.getY() + 1)
	def __reach_boundary(self, position):
		if position.x < 0 or position.x >= self.board.getWidth() or position.y < 0 or position.y >= self.board.getHeight():
			return True
		return False
