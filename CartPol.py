import pygame
import gym 
import math
screen = pygame.display.set_mode((800, 800))
pygame.init()
clock = pygame.time.Clock()
done = False

class CartPole():
        def __init__(self):
                #Stick properties:
                self.stickWidth = 3
                self.stickHeight = 70
                self.stickMass = 0.1

                #Table properties:
                self.tableWidth = 50
                self.tableHeight = 10
                self.tableMass = 1

                #Generall properties:
                self.totalMass = 1.1
                self.gravity = 9.8
                self.path = 400
                


def game():
        while not done:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                done = True
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                                is_blue = not is_blue
                pressed = pygame.key.get_pressed()
                
                # Boundaries and movement
                if 0 < (y - 3):
                        # Manuall:
                         if pressed[pygame.K_UP]:
                                y -= 3 

                if 200 > (y + 3):
                        #Manuall:
                        if pressed[pygame.K_DOWN]:
                                y += 3
                if 0 < (x - 3):
                        #Manuall:
                        if pressed[pygame.K_LEFT]:
                                x -= 3
                if 200 > (x + 3):
                        # Manuall:
                        if pressed[pygame.K_RIGHT]:
                                x += 3

        screen.fill((0, 0, 0))
        pygame.display.flip()
        clock.tick(6)
