import pygame
import sys
import random
import math
import numpy as np

class Man:
    def __init__(self):
        self.pos = np.asmatrix(np.array([[250.0], [250.0], [0.0]]))
        self.view = np.asmatrix(np.array([[-1.0], [0.0], [0.0]]))
    def all(self):
        output = []
        offset = np.dot(rotate_z(-4), self.view)
        for i in range(100):
            line = []
            for j in range(50):
                mult = (100-j)/100
                a = offset.item(0)*mult
                b = offset.item(1)*mult
                try:
                    line += [np.asmatrix(np.array([[a], [b], [float((1-a**2-b**2)**.5)]]))]
                except:
                    line += [np.asmatrix(np.array([[a], [b], [0]]))]                
                try:            
                    line += [np.asmatrix(np.array([[a], [b], [float(-1*(1-a**2-b**2)**.5)]]))]
                except:
                    line += [np.asmatrix(np.array([[a], [b], [0]]))]   
            offset = np.dot(rotate_z(1/25), offset)
            output += [line]
        return output

def main():
    pygame.init()
    pygame.key.set_repeat(5)
    width = 500
    height = 500
    screen = pygame.display.set_mode((width, height))
    man = Man()
    green = (0,200,112)
    white = (255, 255, 255)
    b = (0, 0, 255)
    g = (0, 255, 0)
    red = (235, 0, 0)
    map = [[[1, 0, 1, 1, 1],
           [1, 0, 0, 0, 1],
           [1, 0, 0, 0, 1],
           [1, 0, 0, 0, 1],   
           [0, 0, 0, 0, 1],
           [1, 1, 1, 1, 1]], 
          [[1, 1, 1, 1, 1],
           [1, 0, 0, 0, 1],
           [1, 0, 0, 0, 1],
           [1, 0, 0, 0, 1],   
           [1, 0, 0, 0, 1],
           [1, 1, 1, 1, 1]]]          
           
    rz = 0
    ry = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    man.view = np.dot(rotate_z(-.1), man.view)
                    rz += 1
                if event.key == pygame.K_RIGHT:
                    man.view = np.dot(rotate_z(.1), man.view)

                    rz -= 1
                if event.key == pygame.K_UP:
                    a = man.view.item(0)*.9
                    b = man.view.item(1)*.9
                    try:
                        man.view = np.asmatrix(np.array([[a], [b], [float((1-a**2-b**2)**.5)]]))
                    except:
                        man.view = np.asmatrix(np.array([[a], [b], [0]]))
                    ry += 1
                if event.key == pygame.K_DOWN:
                    a = man.view.item(0)*.9
                    b = man.view.item(1)*.9
                    try:
                        man.view = np.asmatrix(np.array([[a], [b], [float(-1*(1-a**2-b**2)**.5)]]))
                    except:
                        man.view = np.asmatrix(np.array([[a], [b], [0]]))
                    ry += 1
                if event.key == pygame.K_SPACE:
                    man.pos += man.view
        screen.fill((0, 75, 0))
        #for i in range(6):
        #    for j in range(8):
        #        if map[i][j] == 1:
        #            pygame.draw.rect(screen, (0, 0, 0), (100*j+2, 100*i+2, 96, 96)) 
        #pygame.draw.line(screen, red, (man.pos.item(0), man.pos.item(1)), (man.pos.item(0)+100*man.view.item(0), man.pos.item(1)+100*man.view.item(1)))
        #pygame.draw.circle(screen, green, (man.pos.item(0), man.pos.item(1)), 10)
        dists = []
        for line in man.all():
            lv = []
            for thing in line:
                lv += [check_ray(man.pos.item(0), man.pos.item(1), man.pos.item(2), thing.item(0), thing.item(1), thing.item(2), thing, map)]
            dists += [lv]
        x = 0
        pygame.draw.rect(screen, (98, 221, 240), (0, 0, width, 200))
        color = (100, 100, 100)
        for x in range(100):
            for y in range(50):
                if dists[x][2*y]:
                    pygame.draw.rect(screen, (0, 0, 0), (5*x, 10*y, 5, 5))
                else:
                    pygame.draw.rect(screen, (255, 255, 255), (5*x, 10*y, 5, 5))
                if dists[x][2*y+1]:
                    pygame.draw.rect(screen, (0, 0, 0), (5*x, 10*y+5, 5, 5))
                else:
                    pygame.draw.rect(screen, (255, 255, 255), (5*x, 10*y+5, 5, 5))
        pygame.display.update()

    pygame.display.quit()

def check_ray(x, y, z, dx, dy, dz, angle, map):
    distance = 0
    unhit = True
    a = map[int(z//100)][int(y//100)][int(x//100)]
    while a == 0 and unhit:
        x += dx
        y += dy
        z += dz
        distance += 1
        if distance > 800:
            unhit = False
        try:
            a = map[int(z//100)][int(y//100)][int(x//100)]
        except:
            unhit = False
    #a = x - dx
    #b = y - dy
    #if a//100 == x//100 and b//100 != y//100:
    #        color =1
    #elif a//100 != x//100 and b//100 == y//100:
    #    color = 0
    #else:
    #    color = 3
    return unhit


# Returns a 3x3 rotation matrix rotating (rots * pi/12) radians around desired axis
def rotate_z(rots):
    return np.asmatrix(np.array([[math.cos(rots*math.pi/12), -1*math.sin(rots*math.pi/12), 0], [math.sin(rots*math.pi/12), math.cos(rots*math.pi/12), 0], [0, 0, 1]]))

def rotate_x(rots):    
    return np.asmatrix(np.array([[1, 0, 0], [0, math.cos(rots*math.pi/12), -1*math.sin(rots*math.pi/12)], [0, math.sin(rots*math.pi/12), math.cos(rots*math.pi/12)]]))

def rotate_y(rots):    
    return np.asmatrix(np.array([[math.cos(rots*math.pi/12), 0, math.sin(rots*math.pi/12)], [0, 1, 0], [-1*math.sin(rots*math.pi/12), 0, math.cos(rots*math.pi/12)]]))


if __name__ == '__main__':
    main()
