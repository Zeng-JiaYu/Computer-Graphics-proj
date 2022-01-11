import numpy as np
from OpenGL.GL import *
import math as m
from Points import *

PI = 3.14


class Lines:
    def __init__(self):
        self.n = 18
        self.r = 200
        self.p = np.zeros((self.n, 2), dtype=int)
        self.alpha = 0
        self.points = []
        self.BkClr = np.array([0, 0, 0])

    def setAngle(self, value):
        self.alpha = value

    def calculatePoint(self):
        self.points = []
        theta = 2 * PI / self.n
        for i in range(self.n):
            temp = Point(round(250 + self.r * m.cos(i * theta + self.alpha)),
                         round(250 + self.r * m.sin(i * theta + self.alpha)),
                         np.array([0, 0, 255]))
            self.points.append(temp)

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        self.calculatePoint()
        zero = Point(250, 250, np.array([255, 0, 0]))
        for i in range(self.n):
            self.drawLine(self.points[i], zero)

    def drawLine(self, p0, p1):
        # 绘制垂线
        if p0.x == p1.x:
            if p0.y < p1.y:  # 起点低于终点
                dy = p1.y - p0.y
                for i in range(dy):
                    color = self.interpolation(i, 0, dy, p0.color, p1.color)
                    temp = Point(p0.x, i, color)
                    self.putPixel(temp)
                    temp.y = temp.y + 1
            else:  # 起点高于终点
                dy = p0.y - p1.y
                for i in range(dy):
                    color = self.interpolation(i, 0, dy, p0.color, p1.color)
                    temp = Point(p0.x, i, color)
                    self.putPixel(temp)
                    temp.y = temp.y - 1
        # 绘制斜线
        else:
            e = 0
            k = (p1.y - p0.y) / (p1.x - p0.x)
            # 绘制 k > 1
            if k > 1:
                if p0.y < p1.y:
                    dx, dy = p1.x - p0.x, p1.y - p0.y
                    x, y = p0.x, p0.y
                    for i in range(dy):
                        color = self.interpolation(i, 0, dy, p0.color, p1.color)
                        c0 = (self.BkClr - color) * e + color
                        c1 = (self.BkClr - color) * (1 - e) + color
                        self.putPixel(Point(x, y, c0))
                        self.putPixel(Point(x + 1, y, c1))
                        e = e + 1 / k
                        if e >= 1.0:
                            x = x + 1
                            e = e - 1
                        y = y + 1
                else:
                    dx, dy = p0.x - p1.x, p0.y - p1.y
                    x, y = p0.x, p0.y
                    for i in range(dy):
                        color = self.interpolation(i, 0, dy, p0.color, p1.color)
                        c0 = (self.BkClr - color) * e + color
                        c1 = (self.BkClr - color) * (1 - e) + color
                        self.putPixel(Point(x, y, c0))
                        self.putPixel(Point(x - 1, y, c1))
                        e = e + 1 / k
                        if e >= 1:
                            x = x - 1
                            e = e - 1
                        y = y - 1
            # 绘制 0 < k < 1
            if 0 <= k <= 1:
                if p0.x < p1.x:
                    dx, dy = p1.x - p0.x, p1.y - p0.y
                    x, y = p0.x, p0.y
                    for i in range(dx):
                        color = self.interpolation(i, 0, dx, p0.color, p1.color)
                        c0 = (self.BkClr - color) * e + color
                        c1 = (self.BkClr - color) * (1 - e) + color
                        self.putPixel(Point(x, y, c0))
                        self.putPixel(Point(x, y + 1, c1))
                        e = e + k
                        if e > 1:
                            y = y + 1
                            e = e - 1
                        x = x + 1
                else:
                    dx, dy = p0.x - p1.x, p0.y - p1.y
                    x, y = p0.x, p0.y
                    for i in range(dx):
                        color = self.interpolation(i, 0, dx, p0.color, p1.color)
                        c0 = (self.BkClr - color) * e + color
                        c1 = (self.BkClr - color) * (1 - e) + color
                        self.putPixel(Point(x, y, c0))
                        self.putPixel(Point(x, y - 1, c1))
                        e = e + k
                        if e >= 0:
                            y = y - 1
                            e = e - 1
                        x = x - 1
            # 绘制  -1 < k < 0
            if -1 <= k <= 0:
                if p0.x < p1.x:
                    dx, dy = p1.x - p0.x, p1.y - p0.y
                    x, y = p0.x, p0.y
                    for i in range(dx):
                        color = self.interpolation(i, 0, dx, p0.color, p1.color)
                        c0 = (self.BkClr - color) * e + color
                        c1 = (self.BkClr - color) * (1 - e) + color
                        self.putPixel(Point(x, y, c0))
                        self.putPixel(Point(x, y - 1, c1))
                        e = e - k
                        if e >= 1:
                            y = y - 1
                            e = e - 1
                        x = x + 1
                else:
                    dx, dy = p0.x - p1.x, p0.y - p1.y
                    x, y = p0.x, p0.y
                    for i in range(dx):
                        color = self.interpolation(i, 0, dx, p0.color, p1.color)
                        c0 = (self.BkClr - color) * e + color
                        c1 = (self.BkClr - color) * (1 - e) + color
                        self.putPixel(Point(x, y, c0))
                        self.putPixel(Point(x, y + 1, c1))
                        e = e - k
                        if e >= 1:
                            y = y + 1
                            e = e - 1
                        x = x - 1
            # 绘制 k < -1
            if k < -1:
                if p0.y < p1.y:
                    dx, dy = p1.x - p0.x, p1.y - p0.y
                    x, y = p0.x, p0.y
                    for i in range(dy):
                        color = self.interpolation(i, 0, dy, p0.color, p1.color)
                        c0 = (self.BkClr - color) * e + color
                        c1 = (self.BkClr - color) * (1 - e) + color
                        self.putPixel(Point(x, y, c0))
                        self.putPixel(Point(x-1, y, c1))
                        e = e - 1 / k
                        if e >= 1:
                            x = x - 1
                            e = e - 1
                        y = y + 1
                else:
                    dx, dy = p0.x - p1.x, p0.y - p1.y
                    x, y = p0.x, p0.y
                    for i in range(dy):
                        color = self.interpolation(i, 0, dy, p0.color, p1.color)
                        c0 = (self.BkClr - color) * e + color
                        c1 = (self.BkClr - color) * (1 - e) + color
                        self.putPixel(Point(x, y, c0))
                        self.putPixel(Point(x +1 , y, c1))
                        e = e - 1 / k
                        if e >= 1.0:
                            x = x + 1
                            e = e - 1
                        y = y - 1

    @staticmethod
    def putPixel(temp):
        glBegin(GL_POINTS)
        glColor3f(temp.color[0]/256, temp.color[1]/256, temp.color[2]/256)
        glVertex2f(temp.x, temp.y)
        glEnd()
        glFlush()

    @staticmethod
    def interpolation(m2, m0, m1, c0, c1):
        c = (m2 - m1) / (m0 - m1) * c0 + (m2 - m0) / (m1 - m0) * c1
        c = np.around(c)
        return c
