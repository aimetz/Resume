import sys
import random
import numpy as np
import pygame

class Layer:
    def __init__(self, n_inputs, n_neurons):
        self.weights = np.random.randn(n_inputs, n_neurons)
        self.bias = np.zeros((1, n_neurons))
      
    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.bias
     
    def lin_rect_act(self):
        self.output_act = np.maximum(0, self.output)


class Bird:
    def __init__(self, x, y, num_birds):
        self.p = [Vector(x, y)] * num_birds
        self.v = [Vector(0.0, 0.0)] * num_birds
      
    def delete(self, i):
        self.p.pop(i)
        self.v.pop(i)
    
    def get(self, i):
        return (self.p[i], self.v[i])

    def update_v(self, i):
        self.v[i] = Vector(0.0, -.666)

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        if type(self) == type(other) == Vector:
            return Vector(self.x + other.x, self.y+other.y)
        else:
            raise TypeError
    
    def __repr__(self):
        return "Vector({}, {})".format(self.x, self.y)

class Wall:
    def __init__(self, width, height):
        self.w1 = random.randint(.3*height//1, .9*height//1)
        self.w2 = random.randint(.3*height//1, .9*height//1)
        self.x1 = width
        self.x2 = None
    
    def step(self, velocity, width, height):
        self.x1 += velocity
        if self.x2 is None and self.x1<width/2:
            self.x2 = width
        if self.x2 is not None:
            self.x2 += velocity
        if self.x1 < -75:
            self.w1 = random.randint(.3*height//1, .9*height//1)
            self.x1 = width

        if self.x2 is not None and self.x2 < -75:
            self.w2 = random.randint(.3*height//1, .9*height//1)
            self.x2 = width        

class NN:
    def __init__(self):
        self.l1 = Layer(2, 4)
        self.l2 = Layer(4, 4)
        self.l3 = Layer(4, 1)
    def calc(self, inputs):
        self.l1.forward(inputs)
        self.l1.lin_rect_act()
        self.l2.forward(self.l1.output_act)
        self.l2.lin_rect_act()
        self.l3.forward(self.l2.output_act)
        self.output = self.l3.output

class Strat:
    def __init__(self, l1w, l2w, l3w, l1b, l2b, l3b, i=0):
        self.w1 = l1w
        self.w2 = l2w
        self.w3 = l3w
        self.b1 = l1b
        self.b2 = l2b
        self.b3 = l3b
        self.fit = i
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
      
    def __lt__(self, other):
        return self.fit<other.fit
        
    def __add__(self, other):
        a = Strat((self.w1+other.w1)/2,(self.w2+other.w2)/2, (self.w3+other.w3)/2, (self.b1+other.b1)/2, (self.b2+other.b2)/2, (self.b3+other.b3)/2)
        a.color = ((self.color[0]+other.color[0])//2, (self.color[1]+other.color[1])//2, (self.color[2]+other.color[2])//2)
        return a                      
          
    def __repr__(self):
        return "Weights:\n{}\n{}\n{}\nBias:\n{}\n{}\n{}\nFitness: {}\nColor: {}\n".format(self.w1, self.w2, self.w3, self.b1, self.b2, self.b3, self.fit, self.color) 
      

def draw_wall(wall_height, x, hole, color, screen, height):
    pygame.draw.rect(screen, color, (x, 0, hole, wall_height-2.4*hole))
    pygame.draw.rect(screen, color, (x, wall_height, hole, height - wall_height))



def train(num, strats=None, by=5000):
    pygame.init() # Uncomment for graphics



    width = 800
    height = 600
    screen = pygame.display.set_mode((width, height)) # Uncomment for graphics
    green = (0,200,112)
    white = (255, 255, 255)
    red = (235, 0, 0)

    # create a font object.
    # 1st parameter is the font file
    # which is present in pygame.
    # 2nd parameter is size of the font
    font = pygame.font.Font('freesansbold.ttf', 32)
     
     

    if strats is not None: # otherwise num wil be initial number of players
        print("Generation", num) # uses num to also store generation if not initial batch
        num = len(strats)
    best = []
    saved = open("saved_strategies2.txt", "a")
    players = [None] * num
    for lmk in range(num):
        players[lmk] = NN()
        if strats is not None: # sets each player to strategy in strats
            players[lmk].l1.weights = strats[lmk].w1
            players[lmk].l2.weights = strats[lmk].w2
            players[lmk].l3.weights = strats[lmk].w3
            players[lmk].l1.bias = strats[lmk].b1
            players[lmk].l2.bias = strats[lmk].b2
            players[lmk].l3.bias = strats[lmk].b3
    if strats is None: # Starts training with a strategy previously found
        strats = [None]*num
        for klas in range(num):
            strats[klas] = Strat(None, None, None, None, None, None)
    size = 25
    speed = .2
    gravity = Vector(0.0, .001666)
    birds = Bird(width /5, height/2, num)
    i = 0
    walls = Wall(width, height)
    done = []
    while len(players) > len(done):
        for lol in range(len(players)):
            if players[lol] is not None:
                #Plays game for each NN in players[], once it dies adds that player to done and sets its index to None in players[]
                if i % 10:
                    cpu(players[lol], birds, walls, width, height, lol)
                if -95<(walls.x1-width/5)<20:
                    if not (22<(walls.w1-birds.p[lol].y)<155):
                        fin = Strat(players[lol].l1.weights, players[lol].l2.weights, players[lol].l3.weights, 
                                          players[lol].l1.bias, players[lol].l2.bias, players[lol].l3.bias, i)
                        fin.color = strats[lol].color
                        done.append(fin)
                        players[lol] = None
                elif walls.x2 is not None and -95<(walls.x2-width/5)<20:
                    if not (22<(walls.w2-birds.p[lol].y)<155):
                        fin = Strat(players[lol].l1.weights, players[lol].l2.weights, players[lol].l3.weights, 
                                          players[lol].l1.bias, players[lol].l2.bias, players[lol].l3.bias, i)
                        fin.color = strats[lol].color
                        done.append(fin)
                        players[lol] = None
                elif not (25 < birds.p[lol].y < height - 25):
                    fin = Strat(players[lol].l1.weights, players[lol].l2.weights, players[lol].l3.weights, 
                                      players[lol].l1.bias, players[lol].l2.bias, players[lol].l3.bias, i)
                    fin.color = strats[lol].color
                    done.append(fin)
                    players[lol] = None
                birds.v[lol] += gravity
                birds.p[lol] += birds.v[lol]
        if i > 1000000:#Goal, if reached print and save strategy and exit
            for lol in range(len(players)):
                if players[lol] is not None:
                    print("{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n".format(players[lol].l1.weights, players[lol].l2.weights, players[lol].l3.weights, 
                                      players[lol].l1.bias, players[lol].l2.bias, players[lol].l3.bias, i, strats[lol].color))
                    saved.write("{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n".format(players[lol].l1.weights, players[lol].l2.weights, players[lol].l3.weights, 
                                      players[lol].l1.bias, players[lol].l2.bias, players[lol].l3.bias, i, strats[lol].color))
                    sys.exit()
        #Uncomment all below for graphics... Much slower
        screen.fill(white) #fills screen black is actually white
        walls.step(-.333, width, height)
        draw_wall(walls.w1, walls.x1, 75, red, screen, height)
        if walls.x2 is not None:
            draw_wall(walls.w2, walls.x2, 75, red, screen, height)
        for lmk in range(len(players)):
            if players[lmk] is not None:
                pygame.draw.circle(screen, strats[lmk].color, (birds.p[lmk].x, birds.p[lmk].y), size)
        # create a text suface object,
        # on which text is drawn on it.
        text = font.render("Balls left: " + str(len(players)-len(done))+ " Fitness(x1000): " + str(int(i//1000)), True, (0, 0, 0), (255, 255, 255))
        # create a rectangular object for the
        # text surface object
        textRect = text.get_rect()
     
        # set the center of the rectangular object.
        textRect.center = (.6* width, .9* height)
     
        # copying the text surface object
        # to the display surface object
        # at the center coordinate.
        screen.blit(text, textRect)
             
        
        i += 1 # counts number of loops
        pygame.display.update()
    for ch in range(len(done)):
        if done[ch].fit > (by*1.5):
            print(done[ch])
            saved.write("{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n".format(done[ch].w1, done[ch].w2, done[ch].w3, done[ch].b1, done[ch].b2, done[ch].b3, done[ch].fit, strats[ch].color))
            by = done[ch].fit
    for a in range(10):
        good = max(done)
        done.remove(good)
        best.append(good)
    # Mutates best strategies
    best.append(best[0]+best[1])
    best.append(best[0]+best[2])
    best.append(best[1]+best[2])
    best.append(best[0]+best[3])
    best.append(best[0]+best[4])
    best.append(best[1]+best[3])
    best.append(best[1]+best[4])
    best.append(best[2]+best[3])
    best.append(best[2]+best[4])
    best.append(best[3]+best[4])
    for a in range(5):
        for b in range(3):
            #Adds 15 New randoms
            d = NN()
            best.append(Strat(d.l1.weights, d.l2.weights, d.l3.weights, d.l1.bias, d.l2.bias, d.l3.bias))
        for c in range(0, 100, 5):
            # 2nd mutation strategy
            index = random.randint(1, 9)
            
            new = Strat(best[a].w1+.001*c*np.random.randn(2, 4), best[a].w2+.001*c*np.random.randn(4, 4), best[a].w3+.001*c*np.random.randn(4, 1), 
                              best[a].b1+.001*c*np.random.randn(1, 4), best[a].b2+.001*c*np.random.randn(1, 4), best[a].b3+.001*c*np.random.randn(1, 1))
            new.color = [best[a].color[0], best[a].color[1], best[a].color[2]]
            if new.color[index%3]>(250-c):
                new.color[index%3] -= c
            elif new.color[index%3]<c:
                new.color[index%3] += c
            else:
                r2 = random.randint(0, 99)
                if r2%2 == 0:
                    new.color[index%3] += c
                else:
                    new.color[index%3] -= c
            new.color = tuple(new.color)
            best.append(new)
    saved.close()
    return best, by

#calculates if individual bird should jump, pushes normalized inputs through corresponding NN
def cpu(cpu1, birds, walls, width, height, i):
    bird = birds.get(i)
    if walls.x2 is None or bird[0].x-100 < walls.x1 < walls.x2 or walls.x2 < bird[0].x-100:
        wall = [(walls.x1-bird[0].x)/(width/2), (walls.w1 - bird[0].y)/height]
    else:
        wall = [(walls.x2-bird[0].x)/(width/2), (walls.w2 - bird[0].y)/height]    
    cpu1.calc(wall)
    if cpu1.output < 0:
        birds.v[i] = Vector(0, -.666)


# starts with 1000 in first batch and goes through 1000 generations or until goal is reached
strats, by = train(100)
for i in range(10000):
    strats, by = train(i, strats, by)
