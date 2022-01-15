import pygame
import sys
from DRLib.loadFuncs import loadIndex
from Pendulum import *

pygame.init()
WIDTH = 800
HEIGHT = 600
WHITE = (255,255,255)
BLACK = (0,0,0)
SIZE = [200, 10]
POS = np.array([WIDTH/2, HEIGHT/2])

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.key.set_repeat(1)



FRICTION = [.0000001, .0001]
TORQUE = .000002
GRAVITY = .00001


for q in range(0, 18, 3):
    print("Generation: "+ str(((q+1)//3)+1))

    player = loadIndex("saved.csv", q)
    pen = Pendulum()

    for i in range(15000):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


        screen.fill(WHITE)

        pen.applyForces(GRAVITY, FRICTION)

        data= (pen.dir[1]/2+.5, 500*(2*(1*(pen.dir[0]<0))-1)*(pen.angular_vel))
        plays = player.f_pass(data)

        if plays < 0:
            pen.angular_vel -= (2*(1*(pen.dir[0]<0))-1)*TORQUE
        elif plays > 0:
            pen.angular_vel += (2*(1*(pen.dir[0]<0))-1)*TORQUE

        pygame.draw.line(screen, BLACK, POS, POS+SIZE[0]*pen.dir, SIZE[1])
        pygame.draw.circle(screen, BLACK, POS+SIZE[0]*pen.dir, 30)
        pygame.display.update()