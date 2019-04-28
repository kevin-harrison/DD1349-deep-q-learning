import pygame
import math
import random
screen = pygame.display.set_mode((800, 800))
pygame.init()
clock = pygame.time.Clock()
WHITE = (255,255,255)
BROWN = (98, 78, 44)
BLACK = (0,0,0)


class CartPole():
        def __init__(self):
                
                #Generall properties:
                self.totalMass = 1.5
                self.gravity = 9.8
                self.x = 400.0
                self.y = 600.0
                self.dx = 0.0
                self.d2x = 0.0
                self.theta = 0.0
                self.dtheta = 0.0
                self.d2theta = 0.0
                self.eulerStep = 0.01
                self.motor_force = 100.0
                #Stick properties:
                self.stickWidth = 3
                self.stickHeight = 70
                self.stickMass = 0.5
                self.x_stick = self.x -1.5
                self.y_stick = self.y - 70
                #Table properties:
                self.tableWidth = 50
                self.tableHeight = 10
                self.tableMass = 1
                self.acc_time = 0.2
                self.x_table = self.x -25
                self.y_table = self.y -5
                #Fail properties:
                
        def draw(self, screen):
                pygame.draw.rect(screen, BROWN, pygame.Rect(self.x_stick, self.y_stick, self.stickWidth, self.stickHeight))
                pygame.draw.rect(screen, BLACK, pygame.Rect(self.x_table, self.y_table, self.tableWidth, self.tableHeight))
        def step(self, act):
                costheta = math.cos(self.theta)
                sintheta = math.sin(self.theta)
                #Physics relation between stick and table:
                self.dtheta =self.d2theta
                self.d2theta = (self.gravity * sintheta + costheta*((-self.motor_force - self.stickMass*self.stickHeight*((self.dtheta)**2)*sintheta)/(self.totalMass))/self.stickHeight*(4/3 - self.stickMass*costheta**2/self.totalMass))
                self.dx = self.d2x
                self.d2x = (self.motor_force + self.stickMass*self.stickHeight*(sintheta*self.dtheta**2 - self.d2theta*costheta))/self.totalMass
                self.theta = self.euler(self.theta, self.dtheta) + math.pi
                self.dtheta = self.euler(self.dtheta, self.d2theta)                
                self.x = self.euler(self.x, self.dx)
                self.dx = self.euler(self.dx, self.d2x)
                self.x_stick = self.x + self.stickHeight*math.sin(self.theta)
                self.y_stick = self.y + self.stickHeight*math.cos(self.theta)
                self.x_table = self.x -25
                self.y_table = self.y -5
                self.draw(screen)

                
                #Eulers fomula with one step:
        def euler(self, value, dvalue):
                value = value + self.eulerStep*dvalue
                return value 
        
        def action(self, act): 
                if act == 1:
                        self.d2x = -self.motor_force/self.totalMass
                elif act == 0:
                        self.d2x = self.motor_force/self.totalMass
                self.dx = self.d2x*self.acc_time
                self.step(act)

def game():
        cartpol = CartPole()
        num_runs= 0
        right_or_left = random.randint(0,1)
        done = False
        
        while not done:
                num_runs += 1
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                done = True
                pressed = pygame.key.get_pressed()
                # Boundaries and movement
                if 200 < (cartpol.x_table - 3):
                        #Manuall:
                        if pressed[pygame.K_LEFT]:
                                right_or_left = 1

                if 600 - cartpol.tableWidth > (cartpol.x_table + 3):
                        # Manuall:
                        if pressed[pygame.K_RIGHT]:
                                right_or_left = 0

                
                screen.fill(WHITE)
                cartpol.action(right_or_left)
                path = pygame.draw.line(screen, BLACK, (200,600), (600,600), 1)
                pygame.display.flip()
                clock.tick(60)
if __name__ == "__main__":
    game()
