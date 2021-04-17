import numpy as np

class Pendulum:
    def __init__(self):
        self.score = 0
        self.dir = np.array([0, 1])
        self.angular_vel = 0

    def applyForces(self, gravity, friction):
        if self.dir[0] < 0:
            self.angular_vel -= gravity*np.abs(self.dir[0])
        else:
            self.angular_vel += gravity*np.abs(self.dir[0])
        if self.angular_vel > 0:
            self.angular_vel -= friction[0] + friction[1]*np.abs(self.angular_vel)
        elif self.angular_vel < 0:
            self.angular_vel += friction[0] + friction[1]*np.abs(self.angular_vel)
        self.dir = rot(self.dir, self.angular_vel)
        self.score += self.dir[1]

def rot(vector, theta):
    return np.dot(np.array([[np.cos(theta), -1*np.sin(theta)], [np.sin(theta), np.cos(theta)]]), vector)
