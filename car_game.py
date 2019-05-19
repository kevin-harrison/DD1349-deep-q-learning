import pygame
from math import tan,radians, degrees,copysign
import random
import os
import numpy as np
from pygame.math import Vector2
# Visualisation of the path, indluding the track and car. 
current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, "race_car.PNG")
image_track_path = os.path.join(current_dir, "car-track.png")
car_image = pygame.image.load(image_path)
path_image = pygame.image.load(image_track_path)
WHITE = (255,255,255)
screen = pygame.display.set_mode((1478, 731))

class RewardGate:
    # The paths reward system, getting inside a reward gate gives a reward 1 time.
    def __init__(self, x, y, x_length, y_length):
        self.x = x
        self.y = y
        self.x_length = x_length
        self.y_length = y_length

    def collide(self, x_coord, y_coord):
        collide = False
        if x_coord > self.x and x_coord < self.x + self.x_length:
            if y_coord > self.y and y_coord < self.y + self.y_length:
                collide = True
        return collide


class Car:
    """Car-game is the third game we wanna try for our q-learning algorithm.
        The game consist of a rectangular road, a patch of grass in the middle
        and a car. The goal of the course is to return to initial position without
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
	break_deceleration:
	         The breaking force. 
	"""
    def __init__(self, x, y):
        """
        Parameters
        ----------
        x : double
            The initial x-coordinate position of the car.
        y : double
            The intial y-coordinate position of the car.
        """
        # Car position and characteristics
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
        self.brake_deceleration = 1000
        # Rewards positioning.
        self.rewards = [RewardGate(7,0,7,7),RewardGate(1,0,4,7),RewardGate(4,0,4,7), RewardGate(6,0,4,7), RewardGate(33,0,7,7), RewardGate(10,0,7,7), RewardGate(20,0,4,7), RewardGate(33,10,6,6), RewardGate(33,15,6,6), RewardGate(20,16,6,6)]
        # Ratio for transforming force of the vector2 to pixels on the screen.
        self.ratiopixels = 0.026
        #Interaction with the q-learning  algorithm.
        self.state_size = 4
        self.action_size = 4

    def action(self, h):
        # state update after an action, also making sure to controll the limits of velocity.
        self.velocity += (self.acceleration*h, 0)
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))
        # The angle of the cars movement is equal to the vector of its position (hypotenuse) divided by the tangent angle.
        if self.steering:
            radius = self.length/tan(radians(self.steering))
            angular_velocity = self.velocity[0] / radius
        else:
            angular_velocity = 0
        # After the calculation of the steering, the position and angle is changed accordingly. h is the time the acceleration acts during one run.
        self.position += self.velocity.rotate(-self.angle) * h
        self.angle += degrees(angular_velocity) * h

        # Returning the cars position and velocity as state.
        state = [self.position[0], self.position[1], self.velocity[0], self.velocity[1]]
        return state

    def boundaries_check(self):
        # Controll if the car hos broken the limits of the game.
        broken_limit = False
        if ((16.25 > self.position[1] and self.position[1] > 7) and (-3 < self.position[0] and self.position[0] < 33.3)):
            broken_limit = True

        elif ((-0.34 > self.position[1] or self.position[1] > 22.53) or (-0.2 > self.position[0] or self.position[0] > 39.3)):
            broken_limit = True

        return broken_limit
    
    def additional_reward_calculation(self, reward):
        #Provides rewards if the car reaches a reward gate, only ones though for each gate.
        
        for i in range(len(self.rewards)):

            if self.rewards[i].collide(self.position[0], self.position[1]):
                reward = 1000
                self.rewards.pop(i)
                print("milestone reached!")
                break

        return reward

    def render(self):
        # Only activated by the q-learning if a preview of the game is wanted(slows training a lot).
        ppu = 32
        screen.blit(path_image, (0,0))
        rotated = pygame.transform.rotate(car_image, self.angle)
        rect = rotated.get_rect()
        screen.blit(rotated, self.position * ppu - (rect.width / 2, rect.height / 2))
       # for gate in self.rewards:
        #    pygame.draw.rect(screen, (244, 66, 66), pygame.Rect(gate.x/self.ratiopixels, gate.y/self.ratiopixels, gate.x_length/self.ratiopixels, gate.y_length/self.ratiopixels))
        pygame.display.update() 

    def step(self, action):
    # actions: 0 = forward, 1 = brake, 2 = left turn, 3 = right turn.
    # Provides the action for the car at given moment. h is the time of an ection (needed when calculating velocity from acceleration).
    # Reward is initialy only given for forward movement.
        h =0.017
        end_state = False
        reward = None
        if action == 0:
            self.acceleration += 100000 * h
            reward = 10
        elif action == 1:
            reward = -10
            if self.velocity.x > 1000 * self.brake_deceleration:
                # Switches the value to the opposite of its direction.
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
            reward = -1
            self.steering -= 30000 * h
        elif action == 3:
            reward = -1
            self.steering += 30000 * h
        else:
            self.steering = 0
        self.steering = max(-self.max_steering, min(self.steering, self.max_steering))
        # Physical consequence of the given action.
        next_state = self.action(h)
        # Checks to see if crash has taken place and if reward gate is reached. 
        has_crashed = self.boundaries_check()
        if has_crashed:
            end_state = True
            print(self.position[0])
            print(self.position[1])
            reward = -50
        else:
              reward = self.additional_reward_calculation(reward)

        return next_state, reward, end_state

    def reset(self):
        # Upon crashing, the game can be reset with proper intial conditions (position, velocity, rewards).
        self.position[0] = 0;
        self.position[1] = 0;
        self.velocity[0] = 0;
        self.velocity[1] = 0;
        self.rewards = [RewardGate(7,0,7,7),RewardGate(1,0,4,7),RewardGate(4,0,4,7), RewardGate(6,0,4,7), RewardGate(33,0,7,7), RewardGate(10,0,7,7), RewardGate(20,0,4,7), RewardGate(33,10,6,6), RewardGate(33,15,6,6), RewardGate(20,16,6,6)]
        state = [self.position[0], self.position[1], self.velocity[0], self.velocity[1]]
        return state


