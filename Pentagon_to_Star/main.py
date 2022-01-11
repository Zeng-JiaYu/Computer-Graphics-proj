from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import math as m
import time

N = 5
R = 0.5
PI = 3.14
times = 0
flag = 0
points = np.zeros((5, 2), dtype=float)


def starInit():
    """初始化：计算出五边形的起始点坐标"""
    for i in range(N):
        points[i][0] = R * m.cos(2 * PI / N * i)
        points[i][1] = R * m.sin(2 * PI / N * i)
    glBegin(GL_LINE_LOOP)  # 五边形绘制
    for i in range(N):
        glVertex2f(points[i][0], points[i][1])
    glEnd()


def tween(pointA, pointB, t):
    temp = [0] * 2
    temp[0] = (1 - t) * pointA[0] + pointB[0] * t
    temp[1] = (1 - t) * pointA[1] + pointB[1] * t
    return temp


def draw(t):
    global points
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_LINE_LOOP)
    # 计算五个点的变化过程
    for i in range(N):
        temp = tween(points[i], points[(2 * i + 1) % 5], t)
        glVertex2f(temp[0], temp[1])
    glEnd()
    glFlush()


def display():
    """绘图"""
    # 清空
    glClear(GL_COLOR_BUFFER_BIT)
    # 生成五边形坐标
    starInit()


def myIdle():
    global times, flag
    if times > 1:
        flag = 1
    if times < 0:
        flag = 0
    if flag == 0:
        times = times + 0.01
    else:
        times = times - 0.01
    time.sleep(0.02)
    draw(times)
    glFlush()  # 清空OpenGL命令缓冲区，执行OpenGL命令


if __name__ == '__main__':
    glutInit()  # 对GLUT进行初始化
    glutInitWindowSize(500, 500)  # 设置窗口大小
    glutInitWindowPosition(100, 100)  # 设置窗口在屏幕中的位置
    glutCreateWindow("Demo")  # 创建窗口
    glutDisplayFunc(display)
    glutIdleFunc(myIdle)
    glutMainLoop()  # 消息循环
