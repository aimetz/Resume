import pygame
import sys
import random
import math
import numpy as np

class Man:
    def __init__(self):
        self.pos = np.asmatrix(np.array([[400.0], [300.0]]))
        self.view = np.asmatrix(np.array([[1.0], [0.0]]))
    def step(self, direction):
        self.pos += np.asmatrix(np.array(direction))
    def look(self, rots):
        self.view = np.dot(np.asmatrix(np.array([[math.cos(rots*math.pi/12), -1*math.sin(rots*math.pi/12)], [math.sin(rots*math.pi/12), math.cos(rots*math.pi/12)]])), self.view)
    def all(self):
        output = []
        offset = np.dot(np.asmatrix(np.array([[math.cos(-400*math.pi/2400), -1*math.sin(-400*math.pi/2400)], [math.sin(-400*math.pi/2400), math.cos(-400*math.pi/2400)]])), self.view)
        for i in range(800):
            output += [(np.dot(np.asmatrix(np.array([[math.cos(i*math.pi/2400), -1*math.sin(i*math.pi/2400)], [math.sin(i*math.pi/2400), math.cos(i*math.pi/2400)]])), offset), i-400)]
        return output            

def main():
    pygame.init()
    pygame.key.set_repeat(5)
    width = 800
    height = 600
    screen = pygame.display.set_mode((width, height))
    man = Man()
    green = (0,200,112)
    white = (255, 255, 255)
    b = (0, 0, 255)
    g = (0, 255, 0)
    red = (235, 0, 0)
    map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
           [1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
           [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
           [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1],           
           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
           [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
           [1, 1, 0, 1],
           [1, 1, 0, 1],
           [1, 1, 0, 1],
           [1, 1, 0, 1, 1, 1, 1, 1, 1],
           [1, 0, 0, 0, 0, 0, 0, 0, 1],
           [1, 0, 0, 0, 0, 0, 0, 0, 1],
           [1, 0, 0, 0, 0, 0, 0, 0, 1],  
           [1, 0, 0, 0, 0, 0, 0, 0, 1],  
           [1, 1, 1, 1, 1, 1, 1, 1, 1]]
    rotations = 0
    pu = False
    # create a font object.
    # 1st parameter is the font file
    # which is present in pygame.
    # 2nd parameter is size of the font
    font = pygame.font.Font('freesansbold.ttf', 64)
     
    # create a text suface object,
    # on which text is drawn on it.
    text = font.render('Test text', True, (0, 0, 0), (255, 255, 255))
     
    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()
     
    # set the center of the rectangular object.
    textRect.center = (width // 2, 3* height // 4)
     
    # 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pygame.key.set_repeat(5)
                    man.look(-.1)
                    rotations += 1/12
                if event.key == pygame.K_RIGHT:
                    pygame.key.set_repeat(5)
                    man.look(.1)
                    rotations -= 1/12
                if event.key == pygame.K_DOWN:
                    pygame.key.set_repeat(5)
                    man.pos -= man.view
                if event.key == pygame.K_UP:
                    pygame.key.set_repeat(5)
                    man.pos += man.view
                if event.key == pygame.K_SPACE:
                    pygame.key.set_repeat()
                    if pu:
                        pu = False
                    else:
                        if 500 <= man.pos.item(0) < 600 and 400 <= man.pos.item(1) < 500: 
                            pu = True
        screen.fill((0, 75, 0))
        #for i in range(6):
        #    for j in range(8):
        #        if map[i][j] == 1:
        #            pygame.draw.rect(screen, (0, 0, 0), (100*j+2, 100*i+2, 96, 96)) 
        #pygame.draw.line(screen, red, (man.pos.item(0), man.pos.item(1)), (man.pos.item(0)+100*man.view.item(0), man.pos.item(1)+100*man.view.item(1)))
        #pygame.draw.circle(screen, green, (man.pos.item(0), man.pos.item(1)), 10)
        dists = []
        for angle in man.all():
            dists += [check_ray(man.pos.item(0), man.pos.item(1), angle[0].item(0), angle[0].item(1), angle[1], map)]
        x = 0
        pygame.draw.rect(screen, (98, 221, 240), (0, 0, width, 200))
        color = (100, 100, 100)
        for dist in dists:
            if dist[0] > 0:
                line = 30000/dist[0]
            else:
                line = 650
            if dist[1] == 1:
                color = (75, 75, 75)
            elif dist[1] == 0:
                color = (100, 100, 100)
            pygame.draw.line(screen, color, (x, 200 - line/2), (x, 200+line/2))            
            if dist[2]:
                pygame.draw.line(screen, (255, 255, 255), (x, 200 - line/3), (x, 200))            
            if pu:
                pygame.draw.rect(screen, (255, 255, 255), (75, height/2, width-150, height/2))
                
                # copying the text surface object
                # to the display surface object
                # at the center coordinate.
                screen.blit(text, textRect)
             
            x += 1
        pygame.display.update()


    pygame.display.quit()

def check_ray(x, y, dx, dy, angle, map):
    distance = 0
    jc = False
    while map[int(y//100)][int(x//100)] == 0:
        x += dx
        y += dy
        distance += 1
    a = x - dx
    b = y - dy
    if a//100 == x//100 and b//100 != y//100:
        color =1
        if map[int(y//100)][int(x//100)] == 2:
            if 25<x%100<75:
                jc = True
    elif a//100 != x//100 and b//100 == y//100:
        color = 0
    else:
        color = 3
    return (distance*math.cos(angle*math.pi/2400), color, jc)


if __name__ == '__main__':
    main()
