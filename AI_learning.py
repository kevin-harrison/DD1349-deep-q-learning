import math
import random
import numpy as np
import pygame

# Colors for the canvas drawings.
WHITE = (255,255,255)
BROWN = (151, 84, 69)
BLACK = (0,0,0)
screen = pygame.display.set_mode((800, 800))

class CartPole():
	"""Cartpol agent

	Cartpol is the physical envirement for the cartpol game. This enviremont is u
	used to give the calculations of the state dependent on the given action. The
	q-network is combined with the cartpol using an "state to action relation". So the
	training is initialized by the cartpol providing its state, and the q-network to
	give back its predicted action updating its state.

	Attributes
	----------
	totalMass, stickMass, table Mass: double
	Stores the mass of stick that is balanced, and the table that the table is
	balanced on. The total mass represnts the combined mass.
	x, dx, theta, dtheta, d2x, d2theta : double
	x is the center of the carts position on the path. dx is the x values velocity.
	theta is the angle of the stick in regards to its starting position.
	dtheta is the velocity of theta.
	d2theta and d2x is the acceleration of theta and x.
	eulerStep : double
	The length of the euler step used to calculate the next position.
	motor_force: double
	Given an action the motor_force will be applied to the direction of the action.
	stickWidth, stickHeight, tableWidth, tableHeight : double
	The length and width of the stick, and the length and width of the table.
	x_stick, y_stick : double
	position of the stick and table on the canvas to make be able to visualize it.
	rendering : boolean
	False if we dont want to visualise the game through a canvas. Otherwise true.
	"""
	def __init__(self):

		#Generall properties:
		self.totalMass = 1.1
		self.gravity = 9.8
		self.x = 400.0
		self.y = 600.0
		self.dx = 0.0
		self.d2x = 0.0
		self.theta = 0.0
		self.dtheta = 0.0
		self.d2theta = 0.0
		self.eulerStep = 0.02
		self.motor_force = 0
		#Stick properties:
		self.stickWidth = 3
		self.stickHeight = 70
		self.stickMass = 0.1
		self.x_stick = self.x -1.5
		self.y_stick = self.y - 70
		#Table properties:
		self.tableWidth = 50
		self.tableHeight = 10
		self.tableMass = 1
		self.x_table = self.x -25
		self.y_table = self.y -5
		#Toggles first render
		self.rendering = False

	def render(self):
		# If we want to visualize the path on a canvas or not.
		if not self.rendering:
			self.rendering = True
			pygame.init()

			screen.fill(WHITE)
		pygame.draw.line(screen, BROWN, (self.x, self.y), (self.x_stick, self.y_stick), 3)
		pygame.draw.rect(screen, BLACK, pygame.Rect(self.x_table, self.y_table, self.tableWidth, self.tableHeight))
		pygame.display.update()

	def step(self, act):
		# act = 1 gives a force on the direction to the right. Opposite for act = 0;
		if act == 1:
			self.motor_force= 80.0
		elif act == 0:
			self.motor_force = -80.0

		costheta = math.cos(self.theta)
		sintheta = math.sin(self.theta)
		#ODE-system implementation for solving differential equations in: FormulasForSolvingSystem.PNG:
		temp = (self.motor_force + self.stickMass*0.5 * self.dtheta * self.dtheta * sintheta) / self.totalMass
		self.d2theta = (self.gravity * sintheta - costheta* temp) / (self.stickHeight * (4.0/3.0 - self.stickMass * costheta * costheta / self.totalMass))
		self.d2x = temp - self.stickMass*0.5*self.d2theta*costheta / self.totalMass

		#Getting the state of the object using eulers method:
		self.theta = self.euler(self.theta, self.dtheta)
		self.dtheta = self.euler(self.dtheta, self.d2theta)
		self.x = self.euler(self.x, self.dx)
		self.dx = self.euler(self.dx, self.d2x)

		# Getting the angle in the right intervall and startvalue. This is in the intervall [-pi/2: pi/2]:
		angle = -self.theta + math.pi
		if angle > 0:
			angle = angle - 2*math.pi * math.ceil(angle/(2*math.pi))
			angle = math.fmod(angle-math.pi, 2*math.pi) + math.pi
		self.y_stick = self.y + self.stickHeight*math.cos(angle)
		self.x_stick = self.x + self.stickHeight*math.sin(angle)
		self.x_table = self.x -25

		# Check if game is in an end state
		reward = 1
		end_state = False

		if (200 > (self.x_table - 3) or (self.theta > math.pi/9 or  self.theta < -math.pi/9)):
			reward = -100 # reward zero means that we have breaken the boundaries.
			end_state = True
		if (600 - self.tableWidth < (self.x_table + 3) or (self.theta > math.pi/9 or self.theta < -math.pi/9)):
			end_state = True
			reward = -100 # reward zero means that we have breaken the boundaries.

		next_state = [self.x, self.dx, self.theta, self.dtheta]
		return next_state, reward, end_state



	def euler(self, value, dvalue):
		#Eulers fomula with one step, the eulerStep gives how big of a step we want to take.
		value = value + self.eulerStep*dvalue
		return value

	def reset(self):
		#Reset the state for  new test of the system. Used with the q-network when we need to to a new run.
		self.x = 400.0
		self.y = 600.0
		self.dx = 0.0
		self.d2x = 0.0
		self.theta = 0.0
		self.dtheta = 0.0
		self.d2theta = 0.0
		self.eulerStep = 0.02
		self.motor_force = 0

		return [self.x, self.dx, self.theta, self.dtheta]