import pygame
import math
import random
screen = pygame.display.set_mode((800, 800))
pygame.init()
clock = pygame.time.Clock()
WHITE = (255,255,255)
BROWN = (151, 84, 69)
BLACK = (0,0,0)


class CartPole():
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
                self.acc_time = 0.2
                self.x_table = self.x -25
                self.y_table = self.y -5
                #Trials for limits:
                self.dxtrial = 0
                self.dthetatrial = 0
                
        def draw(self, screen):     
                pygame.draw.line(screen, BROWN, (self.x, self.y), (self.x_stick, self.y_stick), 3)
                pygame.draw.rect(screen, BLACK, pygame.Rect(self.x_table, self.y_table, self.tableWidth, self.tableHeight))
                print(self.dtheta)
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
                self.draw(screen)

                
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
        def get_state(self):
                return np.ndarray((4,1), buffer=np.array([self.x,self.dx,self.theta,self.dtheta]))
  

# The main loop that keeps the game running:
def game(human_player):
        cartpol = CartPole()
        num_runs= 0
        right_or_left = None
        done = False

        
        while not done:
                # Game exit:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                pressed = pygame.key.get_pressed()

                #Fail properties left-side of path
                        
                #Fail properties right-side of path:
                if 600 - cartpol.tableWidth < (cartpol.x_table + 3) or (cartpol.theta > math.pi/4 or  cartpol.theta < -math.pi/4) or 200 > (cartpol.x_table - 3):
                        pygame.quit()
                if pressed[pygame.K_RIGHT] and human_player:
                        right_or_left = 1
                if pressed[pygame.K_LEFT] and human_player:
                        right_or_left = 0
                if not human_player:
                        right_or_left = feedforward(cartpol.get_state)
                if pressed[pygame.K_SPACE]:
                        human_player = not human_player
                        
                # Reseting screen:
                screen.fill(WHITE)
                myfont = pygame.font.SysFont("space", 40)
                label = myfont.render("number runs: " + str(num_runs), 1, (BLACK))
                screen.blit(label, (320, 700))
                cartpol.action(right_or_left)
                num_runs += 1
                path = pygame.draw.line(screen, BLACK, (200,600), (600,600), 1)
                pygame.display.update()
                clock.tick(60)
if __name__ == "__main__":
    game(True)

