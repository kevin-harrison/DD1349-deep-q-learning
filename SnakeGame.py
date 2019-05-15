import pygame
import random
import math
from collections import deque


class SnakeGame:
	""" A classic snake game of variable size

	The SnakeGame class keeps track of and claculates the next step of the
	state of a snake game. The state of the game is described by the attributes
	of the class but only global_state is given to the player. The state is
	represented in such a convoluted way in order for the DeepLearner agents to
	learn how to play the game efficenty.

	Attributes
	----------
	size : int
		The size of the grid of the game
	state_size : int
		The length of self.global_state, required for the agent to know how to
		rehape the state vector
	action_size : int
		The number of possible actions a player can take. The snake has the option
		to go left, straight, or right at any state of the game.
	snake : deque
		Data structure holding tuples representing the coordinates of parts of the snake.
		The first element is always the head and the last always the tail
	snake_size : int
		Current size of the snake, grows by one with each apple eaten
	direction : string
		Current direction the snake is traveling
	relative_directions : dictionary
		Maps an action with the current direction and returns a new direction
	apple : tuple[int]
		Coordinates of the apple
	local_state : list[int]
		The first four elements encode the current direction of the snake (for example: [0,1,0,0] equals left).
		Elements 4,5,and 6 encode if there is a dangerous space directly to the left,front, and right of the head
	global_state : list[int]
		Encodes the state of the game for the agent to receive. Every 4 elements encodes one space in the game (for
		example [0,0,1,0] represents the snakes head residing in that space). The last 7 elements correspond to the
		local_state.

	"""

	def __init__(self, size):
		"""
		Parameters
		----------

		size : int
			The size of the grid of the game
		"""

		self.size = size
		self.state_size = (self.size * self.size*4) + 7
		self.action_size = 3
		self.reset()
		self.relative_directions = {"left":["down","left", "up"],
									"right":["up", "right", "down"],
									"up":["left", "up", "right"],
									"down":["right", "down", "left"]
									}
		self.screen = pygame.display.set_mode((self.size*50, self.size*50))
		pygame.init()

	def render(self):
		# Draw rectangles for snake and apple and display on screen

		self.screen.fill((0,0,0))
		pygame.draw.rect(self.screen, (244, 66, 66), pygame.Rect(self.apple[1]*50, self.apple[0]*50, 50, 50))
		for snake in self.snake:
			pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(snake[1]*50, snake[0]*50, 50, 50))
		pygame.display.update()


	def step(self, act):
		# Takes the current state of the game and an action parameter and calculates the next state of the game

		end_state = False
		reward = -0.005
		previous_head = self.snake[0]
		tail = None

		# Get next coords of snakes head
		self.direction = self.relative_directions[self.direction][act]
		if self.direction == "left":
			new_head = (previous_head[0], previous_head[1]-1)
		elif self.direction == "right":
			new_head = (previous_head[0], previous_head[1]+1)
		elif self.direction == "up":
			new_head = (previous_head[0]-1, previous_head[1])
		elif self.direction == "down":
			new_head = (previous_head[0]+1, previous_head[1])

		# Check boundaries
		if new_head[0] < 0 or new_head[0] >= self.size or new_head[1] < 0 or new_head[1] >= self.size:
			end_state = True
			#print("Out of bounds")

		# Check if moved into itself
		new_head_coords = (new_head[0]*self.size + new_head[1]) * 4
		encoded_coord = self.global_state[new_head_coords:new_head_coords+4]
		if encoded_coord == [0,0,0,1]:
			reward = -0.5
			end_state = True
			#print("Ate self")

		# Move snake
		if not end_state:
			self.snake.appendleft(new_head) # append left?
			if self.snake_size < len(self.snake):
				tail = self.snake.pop()

			# Check if eaten apple
			if new_head == self.apple:
				reward = 1
				self.place_apple()
				self.snake_size += 1

			# Update self.global_state to match new state
			self.set_state(new_head, previous_head, tail)
		next_state = self.global_state
		return next_state, reward, end_state


	def reset(self):
		# Sets the state of the game to its initial values

		# Create snake
		snake_start = (math.ceil(self.size/2)-1, math.ceil(self.size/2)-1)
		self.snake = deque()
		self.snake_size = 1
		self.snake.append(snake_start)
		self.direction = "right"

		# Create apple
		self.place_apple()

		# Calculate game state
		self.global_state = [1 if (i+3)%4 == 0 else 0 for i in range((self.size * self.size*4) + 7)]
		self.local_state = [0,0,0,0,0,0,0]
		self.set_state(snake_start, (snake_start[0], snake_start[1]-1), None)
		return self.global_state


	def set_state(self, head, previous_head, tail):
		# Encodes the state of the snake and apple in the list self.global_state

		# Get coordinates of changes
		head_coord = (head[0]*self.size + head[1])* 4
		previous_head_coord = (previous_head[0]*self.size + previous_head[1])* 4

		# Change snake's head state
		self.global_state[head_coord:head_coord+4] = [0,0,1,0]

		# Change snake's body state
		if len(self.snake) > 1:
			self.global_state[previous_head_coord:previous_head_coord+4] = [0,0,0,1]
		else:
			self.global_state[previous_head_coord:previous_head_coord+4] = [0,1,0,0]

		# Remove end of body state
		if tail != None:
			end_coord = (tail[0]*self.size + tail[1])* 4
			self.global_state[end_coord:end_coord+4] = [0,1,0,0]

		# Change apple's state
		apple_coord = (self.apple[0]*self.size + self.apple[1])*4
		self.global_state[apple_coord:apple_coord+4] = [1,0,0,0]

		# Change local state (relative to direction)
		if self.direction == "right":
			self.local_state[:4] = [1,0,0,0]
			left_sensor = (head[0]-1, head[1])
			front_sensor = (head[0], head[1]+1)
			right_sensor = (head[0]+1, head[1])
		if self.direction == "left":
			self.local_state[:4] = [0,1,0,0]
			left_sensor = (head[0]+1, head[1])
			front_sensor = (head[0], head[1]-1)
			right_sensor = (head[0]-1, head[1])
		if self.direction == "up":
			self.local_state[:4] = [0,0,1,0]
			left_sensor = (head[0], head[1]-1)
			front_sensor = (head[0]-1, head[1])
			right_sensor = (head[0], head[1]+1)
		if self.direction == "down":
			self.local_state[:4] = [0,0,0,1]
			left_sensor = (head[0], head[1]+1)
			front_sensor = (head[0]+1, head[1])
			right_sensor = (head[0], head[1]-1)

		# Change local state of sensors
		self.local_state[4:] = [0,0,0]
		# left sensor
		if self.out_of_bounds(left_sensor):
			self.local_state[4] = 1
		else:
			left_sensor = self.convert_coord(left_sensor)
			encoded_coord = self.global_state[left_sensor:left_sensor+4]
			if encoded_coord == [0,0,0,1]:
				self.local_state[4] = 1
		# front sensor
		if self.out_of_bounds(front_sensor):
			self.local_state[5] = 1
		else:
			front_sensor = self.convert_coord(front_sensor)
			encoded_coord = self.global_state[front_sensor:front_sensor+4]
			if encoded_coord == [0,0,0,1]:
				self.local_state[5] = 1
		# right sensor
		if self.out_of_bounds(right_sensor):
			self.local_state[6] = 1
		else:
			right_sensor = self.convert_coord(right_sensor)
			encoded_coord = self.global_state[right_sensor:right_sensor+4]
			if encoded_coord == [0,0,0,1]:
				self.local_state[6] = 1

		self.global_state[-7:] = self.local_state



	def place_apple(self):
		# Chooses a random, empty coordinate for the apple

		apple_coords = (random.randrange(self.size), random.randrange(self.size))
		collision = True

		while collision:
			if apple_coords in self.snake:
				collision = True
				apple_coords = (random.randrange(self.size), random.randrange(self.size))
			else:
				collision = False
		self.apple = apple_coords


	def convert_coord(self, xy_tuple):
		# Converts coordinates in the form (x,y) to there corresponding index in self.global_state

		return (xy_tuple[0]*self.size + xy_tuple[1]) * 4


	def out_of_bounds(self, xy_tuple):
		# Returns True if given coordinates are out of bounds, false otherwise

		if xy_tuple[0] < 0 or xy_tuple[0] >= self.size or xy_tuple[1] < 0 or xy_tuple[1] >= self.size:
			return True
		else:
			return False


	def print_state(self):
		# Prints an ascii representation of the state of the game. Usefull for debugging

		for j in range(self.size):
			row = []
			for i in range(self.size):
				index = (j*self.size+i)*4
				state = self.global_state[index:index+4]
				if state == [1,0,0,0]:
					row.append("A")
				elif state == [0,1,0,0]:
					row.append("_")
				elif state == [0,0,1,0]:
					row.append("H")
				elif state == [0,0,0,1]:
					row.append("B")
			print(row)
		print("Direction:", self.local_state[0:4])
		print("Danger left:", self.local_state[4])
		print("Danger front:", self.local_state[5])
		print("Danger right:", self.local_state[6])



"""
s = SnakeGame(8)

while True:
	s.reset()
	done = False
	while not done:
		#action = int(input()) - 1
		#_, _, done = s.step(action)

		_, _, done = s.step(random.randrange(3))
		s.render()
"""
