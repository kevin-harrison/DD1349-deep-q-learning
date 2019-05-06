
import math
import random


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

                
        #Eulers fomula with one step:
        def euler(self, value, dvalue):
                value = value + self.eulerStep*dvalue
                return value
        
        #Assigning a force on the table:
        def action(self, act): 
                if act == 1:
                        self.motor_force= 300.0
                elif act == 0:
                        self.motor_force = -300.0
                self.step(act)



        #Methods used for the creation of the q-learning algorithm.  
        def random_state(self):
                
                self.x=(random.randrange(0,401) + 200)
                self.theta=(random.randrange(-pi/4, -pi/4))
                self.dx=(random.randrange(-360,360))
                self.dtheta=(random.randrange(-3.17, 3.17))

        def get_newState_and_reward(self, act):
                action(act)
                reward = 1
                if (200 > (cartpol.x_table - 3) or cartpol.y_stick > 580):
                        reward = 0 # reward zero means that we have breaken the boundaries.
                if (600 - cartpol.tableWidth < (cartpol.x_table + 3) or cartpol.y_stick > 580):
                        reward = 0 # reward zero means that we have breaken the boundaries.
                # State is provided by the x position(1), x-velocity(2), theta(3) and theta-velocity(4).
                state = [self.x, self.dx, self.theta, self.dtheta]
                return reward, state