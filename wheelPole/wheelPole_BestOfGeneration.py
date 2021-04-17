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


# player = NN(3, [2, 4, 4, 1])
# player.layers[0].weights = [[ 1.04105281,  1.41965268,  0.24164059, -1.08015808],
#                             [ 1.02373352, -0.3299172,  -0.49380182,  1.14940579]]
# player.layers[0].bias =    [[-0.05863339, -0.00181791,  0.02863135,  0.06348731]]
# player.layers[1].weights = [[-2.11933215,  1.41457551, -1.30119171, -0.98632311],
#                             [-1.03620955,  0.65200167, -1.56971423,  1.28854099],
#                             [-1.08301761,  1.60073122,  0.29844105, -1.006978  ],
#                             [-0.43283162, -1.01874074,  1.60636639,  1.12808766]]
# player.layers[1].bias =    [[-0.08026357, -0.06809398, -0.1405554,  -0.01807309]]
# player.layers[2].weights = [[-1.59771158],
#                             [ 0.24303081],
#                             [-0.20603571],
#                             [-1.3503754 ]]
# player.layers[2].bias =    [[0.11509012]]
for q in range(0, 18, 3):

    player = loadIndex("saved.csv", q)
    pen = Pendulum()

    for i in range(15000):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_LEFT:
            #         pen.angular_vel -= 10*TORQUE
            #     if event.key == pygame.K_RIGHT:
            #         pen.angular_vel += 10*TORQUE

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