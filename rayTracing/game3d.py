import pygame
import sys
import random
import math
import numpy as np

class Man:
    def __init__(self):
        self.pos = np.asmatrix(np.array([[300], [750], [0]]))
        self.view = np.asmatrix(np.array([[1], [0], [0]]))
    def step(self, direction):
        self.pos += np.asmatrix(np.array(direction))

def main():
    pygame.init()

    width = 800
    height = 600
    screen = pygame.display.set_mode((width, height))

    green = (0,200,112)
    white = (255, 255, 255)
    b = (0, 0, 255)
    g = (0, 255, 0)
    red = (235, 0, 0)
    x1 = -2500
    x2 = 2500
    y1 = -2500
    y2 = 2500
    trans = np.dot(np.asmatrix(np.array([[1, 0, 0], [0, 0, -1]])), rotate_x(1))
    #corns3 = [np.asmatrix(np.array([[0], [500], [0]])), np.asmatrix(np.array([[500], [500], [0]])), np.asmatrix(np.array([[500], [0], [0]])),
    #          np.asmatrix(np.array([[500], [0], [-2]])), np.asmatrix(np.array([[500], [500], [-10]])), np.asmatrix(np.array([[0], [500], [-8]]))]
    print("Use arrows to move around and z/x to look around")
    print("wasd still broken")

    man = Man()
    rotations = [0, 0, 0]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pygame.key.set_repeat(5)
                    x1 += 2
                    x2 += 2
                if event.key == pygame.K_RIGHT:
                    pygame.key.set_repeat(5)
                    x1 -= 2
                    x2 -= 2
                if event.key == pygame.K_DOWN:
                    pygame.key.set_repeat(5)
                    y1 += 2
                    y2 += 2
                if event.key == pygame.K_UP:
                    pygame.key.set_repeat(5)
                    y1 -= 2
                    y2 -= 2
                if event.key == pygame.K_z:
                    pygame.key.set_repeat()
                    rotations[2] -= 1
                    trans = np.dot(trans, rotate_x(-1))
                    print((1-(trans.item(0)**2+trans.item(3)**2) +(1- trans.item(1)**2+trans.item(4)**2)))
                    trans = np.dot(trans, rotate_z(1))
                    print((trans.item(0)**2+trans.item(3)**2) + trans.item(1)**2+trans.item(4)**2)

                    trans = np.dot(trans, rotate_x(1))
                    print((trans.item(0)**2+trans.item(3)**2) + trans.item(1)**2+trans.item(4)**2)

                if event.key == pygame.K_x:
                    pygame.key.set_repeat()
                    rotations[2] += 1
                    trans = np.dot(trans, rotate_x(-1))
                    trans = np.dot(trans, rotate_z(-1))
                    trans = np.dot(trans, rotate_x(1))
                if event.key == pygame.K_a:
                    pygame.key.set_repeat()
                    trans = np.dot(trans, rotate_x(.5))
                if event.key == pygame.K_d:
                    pygame.key.set_repeat()
                    trans = np.dot(trans, rotate_x(-.5))
        corns = [np.asmatrix(np.array([[x1], [y2], [0]])), np.asmatrix(np.array([[x2], [y2], [0]])), 
                 np.asmatrix(np.array([[x2], [y1], [0]])), np.asmatrix(np.array([[x1], [y1], [0]]))]
        po = []
        #po2 = []
        #po3 = []
        for i in range(4):
            pos =  np.dot(trans, corns[i])
            po += [(pos.item(0)+man.pos.item(0), pos.item(1)+man.pos.item(1))]
        #    pos2 =  np.dot(trans, corns2[i])
        #    po2 += [(pos2.item(0)+300, pos2.item(1)+400)]
        #for i in range(6):
        #    pos3 =  np.dot(trans, corns3[i])
        #    po3 += [(pos3.item(0)+300, pos3.item(1)+400)]
        
        screen.fill(white)
        pygame.draw.polygon(screen, g, po)

        lines = []
        for q in range(x1, x2, 100):
            a = np.dot(trans, np.asmatrix(np.array([[q], [y1], [0]])))
            aa = np.dot(trans, np.asmatrix(np.array([[q], [y2], [0]]))) 
            lines += [((a.item(0)+man.pos.item(0), a.item(1)+man.pos.item(1)), 
                      (aa.item(0)+man.pos.item(0), aa.item(1)+man.pos.item(1)))]
        for q in range(y1, y2, 100):
            b = np.dot(trans, np.asmatrix(np.array([[x1], [q], [0]])))
            bb = np.dot(trans, np.asmatrix(np.array([[x2], [q], [0]])))
            lines += [((b.item(0)+man.pos.item(0), b.item(1)+man.pos.item(1)), 
                      (bb.item(0)+man.pos.item(0), bb.item(1)+man.pos.item(1)))]
        for line in lines:
            pygame.draw.line(screen, red, line[0], line[1], 1)
        #pygame.draw.polygon(screen, b, po2)
        #pygame.draw.polygon(screen, green, po3)



        pygame.display.update()


    pygame.display.quit()

# Returns a 3x3 rotation matrix rotating (rots * pi/12) radians around desired axis
def rotate_z(rots):
    return np.asmatrix(np.array([[math.cos(rots*math.pi/12), -1*math.sin(rots*math.pi/12), 0], [math.sin(rots*math.pi/12), math.cos(rots*math.pi/12), 0], [0, 0, 1]]))

def rotate_x(rots):    
    return np.asmatrix(np.array([[1, 0, 0], [0, math.cos(rots*math.pi/12), -1*math.sin(rots*math.pi/12)], [0, math.sin(rots*math.pi/12), math.cos(rots*math.pi/12)]]))

def rotate_y(rots):    
    return np.asmatrix(np.array([[math.cos(rots*math.pi/12), 0, math.sin(rots*math.pi/12)], [0, 1, 0], [-1*math.sin(rots*math.pi/12), 0, math.cos(rots*math.pi/12)]]))



if __name__ == '__main__':
    main()
