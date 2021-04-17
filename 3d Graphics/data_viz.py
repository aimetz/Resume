from PIL import Image
import numpy as np
import math
from random import random

# Returns a 3x3 rotation matrix rotating (rots * pi/12) radians around desired axis
def rotate_z(rots):
    return np.asmatrix(np.array([[math.cos(rots*math.pi/12), -1*math.sin(rots*math.pi/12), 0], [math.sin(rots*math.pi/12), math.cos(rots*math.pi/12), 0], [0, 0, 1]]))

def rotate_x(rots):    
    return np.asmatrix(np.array([[1, 0, 0], [0, math.cos(rots*math.pi/12), -1*math.sin(rots*math.pi/12)], [0, math.sin(rots*math.pi/12), math.cos(rots*math.pi/12)]]))

def rotate_y(rots):    
    return np.asmatrix(np.array([[math.cos(rots*math.pi/12), 0, math.sin(rots*math.pi/12)], [0, 1, 0], [-1*math.sin(rots*math.pi/12), 0, math.cos(rots*math.pi/12)]]))


def check_shadow(x, y, z, map):
    a = 1250-x
    b = 2000-y
    c = 10000-z
    l = (a**2+b**2+c**2)**.5
    a /= l
    b /= l
    c /= l
    
    shadow = True
    yes = True
    dist = 0
    while shadow and yes:
        x += a
        y += b
        z += c
        dist += 1
        if 100<y<110 and 145 < x < 165 and 0 < z < 26:
            yes = False               
        if 100<y<110 and 85 < x < 105 and 0 < z < 24:
            yes = False              
        if 100<y<110 and 115 < x < 135 and 0 < z < 50:
            yes = False              
        if z < 0 or y < 0 or x < 0 or x>250 or y > 110 or dist > 200:
            shadow = False
            
    return shadow

width = 500
height = 500


view = np.asmatrix(np.array([[0], [1], [0]]))


views = [None]*width
for i in range(width):
    line = [None]*height
    off = np.dot(rotate_z(-2), view)
    for j in range(height):
        off = np.dot(rotate_x(2-i/125), off)
        line[j] = off
        off = np.dot(rotate_x(-2+i/125), off)
        off = np.dot(rotate_z(1/125), off)
    views[i] = line

print("Got Rays")
hits = [None] * 500
m = 0
cs=50
stat= 26
oth=24
for line in views:
    inner = [None]* 500
    n = 0
    for v in line:
        dx= v.item(0)
        dy = v.item(1)
        dz = v.item(2)
        px = 125
        py = 15
        pz = 25
        hit = False
        missed = False
        dist = 0
        shadow = True
        while not hit and not missed:
            px += dx
            py += dy
            pz += dz
            dist += 1
            if 100<py<110 and 145 < px < 165 and 0 < pz < 26:
                hit = True
                color = 1                
            if 100<py<110 and 85 < px < 105 and 0 < pz < 24:
                hit = True   
                color = 2
            if 100<py<110 and 115 < px < 135 and 0 < pz < 50:
                hit = True
                color = 3
            #if pz < 0:
            #    if (px-100)**2+(py-100)**2 < 2500:
            #        if dz< 0:
            #            dz *= -1
            #    else:
            #        missed = True
            if pz < 0 or py < 0 or px < 75 or px>175 or py > 110 or pz > 50:
                missed = True
            if dist >300:
                missed = True
        if missed:
            if pz<0:
                color = 4
            else:
                color = 5
                shadow = False
        if shadow:
            shadow = check_shadow(px, py, pz, map)
        inner[n] = (hit, shadow, color)
        n += 1
    hits[m] = inner
    m += 1
print("Checked Rays")        

array = [None]*500
q = 0
for a in hits:
    line = [None]*500
    r = 0
    for ray in a:
        if ray[0]:
            if ray[2]==1:
                c = [255, 100, 100]
                if ray[1]:
                    c = [195, 0, 0]
            elif ray[2] ==2:
                c = [100, 255, 100]
                if ray[1]:
                    c = [0, 195, 0]
            elif ray[2] ==3:
                c = [100, 100, 255]
                if ray[1]:
                    c = [0, 0, 195]
            line[r] = c
        else:
            if ray[2] == 4:
                if ray[1]:
                    line[r] = [0, 80, 0]
                else:
                    line[r] = [0, 129, 0]
            else:
                line[r] = [150, 150, 255]
        r += 1
    array[q] = line
    q += 1

print("Done")

array = np.array(array, dtype=np.uint8)

img = Image.fromarray(array)
img.save("random.png")

