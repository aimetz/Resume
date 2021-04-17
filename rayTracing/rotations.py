import pygame
import sys
import math
import numpy as np

 

# Returns a 3x3 rotation matrix rotating (rots * pi/12) radians around desired axis
def rotate_z(rots):
    return np.asmatrix(np.array([[math.cos(rots*math.pi/12), -1*math.sin(rots*math.pi/12), 0], [math.sin(rots*math.pi/12), math.cos(rots*math.pi/12), 0], [0, 0, 1]]))

def rotate_x(rots):    
    return np.asmatrix(np.array([[1, 0, 0], [0, math.cos(rots*math.pi/12), -1*math.sin(rots*math.pi/12)], [0, math.sin(rots*math.pi/12), math.cos(rots*math.pi/12)]]))

def rotate_y(rots):    
    return np.asmatrix(np.array([[math.cos(rots*math.pi/12), 0, math.sin(rots*math.pi/12)], [0, 1, 0], [-1*math.sin(rots*math.pi/12), 0, math.cos(rots*math.pi/12)]]))



def main():
    pygame.init()

    print("\n\nThanks For viewing rotations.py created by Aiden Metz")
    print("The purpose of this file is to create realiztic 3D rotations on a gui that only has support for 2D\nPress q to quit")
    print("Use left/right arrows to rotate about the Green axis\nUp/down arrows for rotations about red axis\n'x'/'z' to rotate about Blue axis")



    width = 800
    height = 600
    screen = pygame.display.set_mode((width, height))

    game_over = False

    green = (0,200,112)
    white = (255, 255, 255)
    b = (0, 0, 255)
    g = (0, 255, 0)
    red = (235, 0, 0)

    # Started with an arbitrary 3x2 that I knew must be included in the set of possible translations
    trans = np.asmatrix(np.array([[1, 0, 0], [0, 0, -1]]))

    #100 pixels along every axis for the corners
    corns = [np.asmatrix(np.array([[0], [0], [0]])), np.asmatrix(np.array([[100], [0], [0]])), 
             np.asmatrix(np.array([[0], [100], [0]])), np.asmatrix(np.array([[0], [0], [100]]))]

    rotations = [0, 0, 0] # keeps track of how many pi/12 rotations have been done to each axis, not helpful as order matters
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            #Multiplies translation matrix by desired rotation matrix, updates that as new translation matrix
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    rotations[0] -= 1
                    trans = np.dot(trans, rotate_x(-1))
                if event.key == pygame.K_RIGHT:
                    rotations[0] += 1
                    trans = np.dot(trans, rotate_x(1))
                if event.key == pygame.K_DOWN:
                    rotations[1] -= 1
                    trans = np.dot(trans, rotate_y(-1))
                if event.key == pygame.K_UP:
                    rotations[1] += 1
                    trans = np.dot(trans, rotate_y(1))
                if event.key == pygame.K_z:
                    rotations[2] -= 1
                    trans = np.dot(trans, rotate_z(-1))
                if event.key == pygame.K_x:
                    rotations[2] += 1
                    trans = np.dot(trans, rotate_z(1))
                if event.key == pygame.K_q:
                    sys.exit()
        screen.fill(white)

        po = [] # a list to hold the 2d points
        for i in range(4):
            pos =  np.dot(trans, corns[i])
            po += [(pos.item(0)+400, pos.item(1)+300)] # creates list of tuples of 2d points, centers point (0,0) to middle of screen
        pygame.draw.line(screen, green, po[0], po[1], 3) # <vv draws each axis vv 
        pygame.draw.line(screen, red, po[0], po[2], 3)
        pygame.draw.line(screen, b, po[0], po[3], 3)

        pygame.display.update()


    pygame.display.quit()


if __name__ == '__main__': 
    main()


