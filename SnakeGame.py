import pygame
import random
import math
from collections import deque


WHITE = (255,255,255)
BROWN = (151, 84, 69)
BLACK = (0,0,0)

class SnakeGame:
	def __init__(self, size):
		self.size = size
		self.state_size = size * size
		self.action_size = 3
		self.rendering = False
		self.reset()
		self.relative_directions = {"left":["down","left", "up"],
									"right":["up", "right", "down"],
									"up":["left", "up", "right"],
									"down":["right", "down", "up"]
									}
		self.screen = pygame.display.set_mode((self.size*50, self.size*50))


	def render(self):
		# Only init pygame if first time rendering
		if not self.rendering:
			self.rendering = True

			pygame.init()

		# Draw rectangles for snake and apple
		self.screen.fill(BLACK)
		pygame.draw.rect(self.screen, (244, 66, 66), pygame.Rect(self.apple[1]*50, self.apple[0]*50, 50, 50))
		print(self.apple)
		for snake in self.snake:
			pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(snake[1]*50, snake[0]*50, 50, 50))
		pygame.display.update()


	def step(self, act):
		end_state = False
		reward = 0

		# Get next coords of snakes head
		self.direction = self.relative_directions[self.direction][act]
		if self.direction == "left":
			new_head = (self.snake[0][0], self.snake[0][1]-1)
		elif self.direction == "right":
			new_head = (self.snake[0][0], self.snake[0][1]+1)
		elif self.direction == "up":
			new_head = (self.snake[0][0], self.snake[0][1]-1)
		elif self.direction == "down":
			new_head = (self.snake[0][0], self.snake[0][1]+1)

		# Check if eaten apple
		if new_head == self.apple:
			reward = 100
			self.place_apple()
			self.snake.maxlen += 1 # TODO: doesn't work

		# Check boundaries
		if new_head[0] < 0 or new_head[0] >= self.size or new_head[1] < 0 or new_head[1] >= self.size:
			end_state = True

		# Move snake
		self.snake.append(new_head)
		next_state = self.set_state()

		return next_state, reward, end_state

	def reset(self):

		# Create snake
		snake_start = (math.ceil(self.size/2)-1, math.ceil(self.size/2)-1)
		self.snake = deque(maxlen=1)
		self.snake.append(snake_start)
		self.direction = "right"

		# Create apple
		self.place_apple()

		# Calculate game state
		self.global_state = [1 if (i+3)%4 == 0 else 0 for i in range(self.size * self.size*4)]
		self.set_state()

		#print(self.global_state)
		self.print_state()



	def set_state(self):

		# Change snake's state
		head_coord = (self.snake[0][0]*self.size + self.snake[0][1])* 4
		end_coord = (self.snake[len(self.snake)-1][0]*self.size + self.snake[len(self.snake)-1][1])* 4
		if len(self.snake) > 1:
			previous_head_coord = (self.snake[1][0]*self.size + self.snake[1][1])* 4
			self.global_state[previous_head_coord:previous_head_coord+3] = [0,0,0,1]
		self.global_state[end_coord:end_coord+4] = [0,1,0,0]
		self.global_state[head_coord:head_coord+4] = [0,0,1,0]

		# Change apple's state
		apple_coord = (self.apple[0]*self.size + self.apple[1])*4
		self.global_state[apple_coord:apple_coord+4] = [1,0,0,0]

		# Change local state

	def place_apple(self):
		apple_coords = (random.randrange(self.size), random.randrange(self.size))
		collision = True

		while collision:
			if apple_coords in self.snake:
				collision = True
				apple_coords = (random.randrange(self.size), random.randrange(self.size))
			else:
				collision = False
		self.apple = apple_coords


	def print_state(self):
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


s = SnakeGame(3)
s.render()
input()
s.step(1)
s.render()
input()