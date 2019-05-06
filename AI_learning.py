import pygame
import math
import random
import NeuralNetwork
screen = pygame.display.set_mode((800, 800))
pygame.init()
clock = pygame.time.Clock()
WHITE = (255,255,255)
BROWN = (98, 78, 44)
BLACK = (0,0,0)
complete_data = []


class CartPole():
        def __init__(self):
                
                #Generall properties:
                self.totalMass = 1.7
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
                self.stickMass = 0.7
                self.x_stick = self.x -1.5
                self.y_stick = self.y - 70
                #Table properties:
                self.tableWidth = 50
                self.tableHeight = 10
                self.tableMass = 1
                self.acc_time = 0.2
                self.x_table = self.x -25
                self.y_table = self.y -5
                
        def draw_position(self, screen):
                pygame.draw.line(screen, BROWN, (self.x, self.y), (self.x_stick, self.y_stick), 3)
                pygame.draw.rect(screen, BLACK, pygame.Rect(self.x_table, self.y_table, self.tableWidth, self.tableHeight))
                
        def step(self, act):
                costheta = math.cos(self.theta)
                sintheta = math.sin(self.theta)
                #ODE-system implementation for solving differential equations in FormulasForSolvingSystem.PNG:
                temp = (self.motor_force + self.stickMass*0.5 * self.dtheta * self.dtheta * sintheta) / self.totalMass
                self.d2theta = (self.gravity * sintheta - costheta* temp) / (self.stickHeight * (4.0/3.0 - self.stickMass * costheta * costheta / self.totalMass))
                self.d2x = temp - self.stickMass*0.5*self.d2theta*costheta / self.totalMass

                #Getting the state of the object using eulers method:
                self.theta = self.euler(self.theta, self.dtheta)
                self.dtheta = self.euler(self.dtheta, self.d2theta)                
                self.x = self.euler(self.x, self.dx)
                self.dx = self.euler(self.dx, self.d2x)

                # Getting the angle in the right intervall and startvalue:
                angle = -self.theta + math.pi 
                if angle > 0:
                        angle = angle - 2*math.pi * math.ceil(angle/(2*math.pi))
                        angle = math.fmod(angle-math.pi, 2*math.pi) + math.pi
                self.y_stick = self.y + self.stickHeight*math.cos(angle)
                self.x_stick = self.x + self.stickHeight*math.sin(angle)
                self.x_table = self.x -25
                self.draw_position(screen)

                
        #Eulers fomula with one step:
        def euler(self, value, dvalue):
                value = value + self.eulerStep*dvalue
                return value
        
        #Assigning a force on the table:
        def action(self, act): 
                if act == 1:
                        self.motor_force= 1000.0
                elif act == 0:
                        self.motor_force = -1000.0
                self.step(act)
                
        def position_returning(self):
            return self.theta, self.x


                
# The main loop that keeps the game running:
def AI_training():
    
        cartpol = CartPole()
        network = NeuralNetwork([2,3,2])
        num_runs= 0
        done = False
        information_of_runs = []
        
        while not done:
                # Game exit:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT or number_of_training_runs == 50:
                                pygame.quit()
                theta,x = cartpol.position_returning()
                network.SGD([theta,x], 100, 0.8)
                # Decision making here should be implemented, input is the theta and x value. Output is either 0 or 1.
                # right_or_left = whatever is returned by the neural network and q-earning algorithm.
                #Fail properties left-side of path:
                if (200 > (cartpol.x_table - 3) or cartpol.y_stick > 580):
                    information_of_runs.append(num_runs)
                    AI_training()
                        
                #Fail properties right-side of path:
                if (600 - cartpol.tableWidth < (cartpol.x_table + 3) or cartpol.y_stick > 580):
                    information_of_runs.append(num_runs)
                    AI_training()
                        
                screen.fill(WHITE) # Reseting screen
                cartpol.action(right_or_left) # Applying the force in the cartpol.
                num_runs += 1 # Points scored this round.
                path = pygame.draw.line(screen, BLACK, (200,600), (600,600), 1) # Path drawing.
                pygame.display.update()
                clock.tick(60)
if __name__ == "__main__":
    AI_training()
