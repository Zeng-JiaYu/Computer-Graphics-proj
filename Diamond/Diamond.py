from OpenGL.GL import *
import numpy as np
import math as m

PI = 3.14


def drawLine(x1, y1, x2, y2):
    glBegin(GL_LINES)
    glVertex2d(x1, y1)
    glVertex2d(x2, y2)
    glEnd()
    glFlush()


class Diamond:
    def __init__(self):
        self.n = 20
        self.r = 200
        self.p = np.zeros((self.n, 2), dtype=int)
        self.alpha = 0

    def setAngle(self, value):
        self.alpha = value

    def calculatePoint(self):
        theta = 2 * PI / self.n
        for i in range(self.n):
            self.p[i][0] = round(250 + self.r * m.cos(i * theta + self.alpha))
            self.p[i][1] = round(250 + self.r * m.sin(i * theta + self.alpha))

    def draw(self):
        self.calculatePoint()
        glClear(GL_COLOR_BUFFER_BIT)
        for i in range(self.n - 1):
            for j in range(i + 1, self.n):
                drawLine(self.p[i][0], self.p[i][1], self.p[j][0], self.p[j][1])
