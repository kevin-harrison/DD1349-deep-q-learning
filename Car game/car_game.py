import pygame
from math import tan,radians, degrees,copysign
import random
import os
import numpy as np
from pygame.math import Vector2
WHITE = (255,255,255)
screen = pygame.display.set_mode((1478, 731))
pygame.init()

class Car:
    """Car-game is the third game we wanna try for our q-learning algorithm.
        The game consist of a rectangular road, a patch of grass in the middle
        and a car. The goal of the course is to return to the starting position without
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
        self.max_steering = 80
        self.max_velocity = 20
        self.free_deceleration = 2
        self.acceleration = 0.0
        self.steering = 0.0
        self.brake_deceleration = 10
        
    def step(self, h):
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
        
class Game():
    def 

    def boundaries_check(self,vector):
        # The boundaries of the grass patch and the canvas.
        broken_limit = False
        reward = 1
        if ((1249 > vector[0] and vector[0] > 230) and (200 < vector[1] and vector[1] < 542)):
            broken_limit = True
            reward = -100;
        return broken_limit
    
    def render(self,car_image, path_image, car, ppu, clock):
        # Called if we want to plot the game canvas.
        screen.blit(path_image, (0,0))
        rotated = pygame.transform.rotate(car_image, car.angle)
        rect = rotated.get_rect()
        screen.blit(rotated, car.position * ppu - (rect.width / 2, rect.height / 2))
        pygame.display.flip()
        clock.tick(60)
        return rect

    def run(self):
        car = Car(0,0)
        done = False
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "race_car.png")
        image_track_path = os.path.join(current_dir, "car-track.png")
        car_image = pygame.image.load(image_path)
        path_image = pygame.image.load(image_track_path)
        clock = pygame.time.Clock()
        ppu = 32

        while not done:
            h = clock.get_time() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_UP]:
                car.acceleration += 10 * h
            elif pressed[pygame.K_SPACE]:
                if car.velocity.x > 5000 * car.brake_deceleration:
                    car.acceleration = -copysign(car.brake_deceleration, car.velocity.x)
                else:
                    car.acceleration = -car.velocity.x / h
            else:
                if abs(car.velocity.x) > h * car.free_deceleration:
                    car.acceleration = -copysign(car.free_deceleration, car.velocity.x)
                else:
                    if h != 0:
                        car.acceleration = -car.velocity.x / h
                        car.acceleration = max(-car.max_acceleration, min(car.acceleration, car.max_acceleration))
            if pressed[pygame.K_RIGHT]:
                car.steering -= 80 * h
            elif pressed[pygame.K_LEFT]:
                car.steering += 80 * h
            else:
                car.steering = 0
            car.steering = max(-car.max_steering, min(car.steering, car.max_steering))
            car.step(h)
            # Reseting screen:
            rect = self.render(car_image, path_image, car, ppu, clock)
            done = self.boundaries_check(car.position * ppu - (rect.width / 2, rect.height / 2))
            
        pygame.quit()
        
if __name__ == "__main__":
    game = Game()
    game.run()
