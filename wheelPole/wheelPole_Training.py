import pygame
import sys
from DRLib.Generation import Generation
from Pendulum import *

""" CONSTANTS ONLY NEEDED FOR GRAPHICS
"""
WIDTH = 800
HEIGHT = 600
WHITE = (255,255,255)
BLACK = (0,0,0)
SIZE = [200, 10]
POS = np.array([WIDTH/2, HEIGHT/2])

""" More various graphics setup
"""
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))


""" CONSTANTS FOR REAL WORLD FORCES
"""
FRICTION = [.0000001, .0001] #index 0 is constant, index 1 is proportion of angular momentum
TORQUE = .000002
GRAVITY = .00001

""" MAKE INITIAL 100 Random neural networks and 100 pendulum objects
"""
pop = 100
pen = [None]*pop
for i in range(pop):
    pen[i] = Pendulum()
g = Generation(pop, [2, 4, 4, 1], True)


for q in range(5): # Go for 5 generations
    print("generation: " + str(q+1))
    for i in range(10000): # Go for 10000 gameloops per generation
        if i%1000==0:
            print(i) # Let me know how long is left in generation
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit() # Makes close button work for graphics window

        data = np.array([None]*len(pen)) # will be a list of inputs for each player based on their own data
        loopScore = np.zeros(len(pen)) # a list to hold the score for THIS loop.

        for j in range(len(pen)):
            pen[j].applyForces(GRAVITY, FRICTION) # First apply gravity and friction
            """ Input is 1x2 index 0: y component of direction vector, 0 is straight up and 1 is straight down
                index 1 is angular velocity made to be between -1 and 1
                It doesnt know what its x component is so it doesnt know what side of the y axis it is on. I made the
                observation that it should treat both sides with the exact same strategy except inverted so I multiply 
                all of the necesary values by -1 if it is on one side and and have it think that it is always on the 
                same side.
            """
            data[j] = (pen[j].dir[1]/2+.5, 500*(2*(1*(pen[j].dir[0]<0))-1)*(pen[j].angular_vel))

        plays = g.f_pass_sep_inputs(data) #Pass list of all inputs to generation object, return output

        """ Parse numerical output into game output
        """
        for j in range(len(pen)):
            if plays[j] < 0:
                pen[j].angular_vel -= (2*(1*(pen[j].dir[0]<0))-1)*TORQUE
            elif plays[j] > 0:
                pen[j].angular_vel += (2*(1*(pen[j].dir[0]<0))-1)*TORQUE
            loopScore[j] += pen[j].dir[1]
        g.update_score(loopScore)

        """ Print graphics for player at index 0 only, It is slow because around 600 other neural networks are also
        playing simaltaniously so overall training time is relatively fast
        who is unchanged best from previous generation
        """
        screen.fill(WHITE)
        pygame.draw.line(screen, BLACK, POS, POS+SIZE[0]*pen[0].dir, SIZE[1])
        pygame.display.update()

    """ Update generation and create new pendulum objects
    """
    g = g.next_gen()
    pop = len(g.pop)
    pen = [None]*pop
    for i in range(pop):
        pen[i] = Pendulum()
