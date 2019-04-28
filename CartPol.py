import pygame
import math
import random
screen = pygame.display.set_mode((800, 800))
pygame.init()
clock = pygame.time.Clock()
WHITE = (255,255,255)
GREEN = (0,255,0)
BLACK = (0,0,0)

class CartPole():
        def __init__(self):
                #Stick properties:
                self.stickWidth = 3
                self.stickHeight = 70
                self.stickMass = 0.1
                self.x_stick = 400 -1.5
                self.y_stick = 600 - 70
                #Table properties:
                self.tableWidth = 50
                self.tableHeight = 10
                self.tableMass = 1
                self.x_table = 400-25
                self.y_table = 600-5
                #Movement properties:
                
                #Generall properties:
                self.totalMass = 1.1
                self.gravity = 9.8
                self.path = 400
                
        def draw(self, screen):
                pygame.draw.rect(screen, GREEN, pygame.Rect(self.x_stick, self.y_stick, self.stickWidth, self.stickHeight))
                pygame.draw.rect(screen, WHITE, pygame.Rect(self.x_table, self.y_table, self.tableWidth, self.tableHeight))
                
def redrawScreen(cartpol):
      cartpol.draw(screen)
      

def game():
        done = False
        cartpol = CartPole()
        
        while not done:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                done = True
                pressed = pygame.key.get_pressed()
                # Boundaries and movement
                if 200 < (cartpol.x_table - 3):
                        #Manuall:
                        if pressed[pygame.K_LEFT]:
                                x -= 3
                if 600 > (cartpol.x_table + 3):
                        # Manuall:
                        if pressed[pygame.K_RIGHT]:
                                x += 3
                redrawScreen(cartpol)
                pygame.display.flip()
                clock.tick(6)
game()
