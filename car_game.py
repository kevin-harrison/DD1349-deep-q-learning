import pygame
from math import tan,radians, degrees,copysign
import random
import os
import numpy as np
from pygame.math import Vector2
current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, "race_car.PNG")
image_track_path = os.path.join(current_dir, "car-track.png")
car_image = pygame.image.load(image_path)
path_image = pygame.image.load(image_track_path)
WHITE = (255,255,255)
screen = pygame.display.set_mode((1478, 731))




class Car:
    """Car-game is the third game we wanna try for our q-learning algorithm.
        The game consist of a rectangular road, a patch of grass in the middle
        and a car. The goal of the course is to return to finish the course without
        breaking the limits (the canvas and the patch of grass).
	Attributes
	----------
 	position : Vector2
		The position in the x, y plane of the car.
	velocity: Vector2
		The velocity in the x and y direction of the car.
	angle : double
		The angle from in respect to the initial position of the car.
	max_acceleration: double
	         The maximum acceleration of the car.
        max_acceleration, max_steering, max_velocity, : double
	         The maximum acceleration, steering (how fast the car turns) and
	         the velocity of the car.
	acceleration, steering: double
	         The current acceleration and steering/turning of the car.
	"""
    def __init__(self, x, y):
        """
        Parameters
        ----------
        x : double
            The x-coordinate position of the car.
        y : double
            The y-coordinate position of the car.
        """
        self.position = Vector2(x,y)
        self.velocity = Vector2(0.0,0.0)
        self.angle = 0.0
        self.length = 4
        self.max_acceleration = 5.0
        self.max_steering = 40
        self.max_velocity = 30
        self.free_deceleration = 2
        self.acceleration = 0.0
        self.steering = 0.0
        self.brake_deceleration = 10
        self.clock = pygame.time.Clock()
        self.rewarder = [100,300,1000]
        #Interaction with the q-learning  algorithm.
        self.state_size = 4
        self.action_size = 4

    def action(self, h):
        # state update after an action.
        self.velocity += (self.acceleration*h, 0)
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

        if self.steering:
            radius = self.length/tan(radians(self.steering))
            angular_velocity = self.velocity[0] / radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * h
        self.angle += degrees(angular_velocity) * h

        # Returning the cars position and velocity as state.
        state = [self.position[0], self.position[1], self.velocity[0], self.velocity[1]]
        return state

    def boundaries_check(self):
        # Controll if the car hos broken the limits of the game.
        broken_limit = False
        if ((16.25 > self.position[1] and self.position[1] > 7) and (-3 < self.position[0] and self.position[0] < 39.3)):
            broken_limit = True

        elif ((-0.34 > self.position[1] or self.position[1] > 26.53) or (-0.2 > self.position[0] or self.position[0] > 39.3)):
            broken_limit = True

        return broken_limit

    def additional_reward_calculation(self):
        reward =0;

        if self.position[1] < 11.62 and self.position[0] > 23.25 and (len(self.rewarder)==3):
            reward = self.rewarder[0]
            self.rewarder.pop(0)
        elif self.position[1] < 11.625 and self.position[0] > 23.25 and (len(self.rewarder)==2):
            reward = self.rewarder[0]
            self.rewarder.pop(0)
        elif self.position[1] > 11.625 and self.position[0] < 23.25 and (len(self.rewarder)==1):
            reward = self.rewarder[0]
            self.rewarder.pop(0)
        else:
            reward = 0
        return reward

    def render(self):
        ppu = 32
        screen.blit(path_image, (0,0))
        rotated = pygame.transform.rotate(car_image, self.angle)
        rect = rotated.get_rect()
        screen.blit(rotated, self.position * ppu - (rect.width / 2, rect.height / 2))
        pygame.display.update()

    def step(self, action):
    # actions: 0 = break, 1 = forward, 2 = left, 3 = right.
    # Provides the action for the car at given moment.
        h =0.017
        end_state = False
        reward = 0
        if action == 0:
            self.acceleration += 100000 * h
        elif action == 1:
            if self.velocity.x > 100000 * self.brake_deceleration:
                self.acceleration = -copysign(self.brake_deceleration, self.velocity.x)
            else:
                self.acceleration = -self.velocity.x / h
        else:
            if abs(self.velocity.x) > h * self.free_deceleration:
                self.acceleration = -copysign(self.free_deceleration, self.velocity.x)
            else:
                if h != 0:
                    self.acceleration = -self.velocity.x / h
                    self.acceleration = max(-self.max_acceleration, min(self.acceleration, self.max_acceleration))
        if action == 2:
            self.steering -= 30000 * h
        elif action == 3:
            self.steering += 30000 * h
        else:
            self.steering = 0
        self.steering = max(-self.max_steering, min(self.steering, self.max_steering))
        # Physical consequence of the given action.
        next_state = self.action(h)
        # Checks to see if crash has taken place, otherwise reward dependent on how long it has come on the path.
        has_crashed = self.boundaries_check()
        if has_crashed:
            end_state = True
            print(self.position[0])
            print(self.position[1])
            reward = -10
        else:
            if action == 0:
                reward = self.additional_reward_calculation()

        return next_state, reward, end_state

    def reset(self):
        self.position[0] = 0;
        self.position[1] = 0;
        self.velocity[0] = 0;
        self.velocity[1] = 0;
        state = [self.position[0], self.position[1], self.velocity[0], self.velocity[1]]
        return state


