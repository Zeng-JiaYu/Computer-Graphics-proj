from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Lines import *
from Rect import *
import time

LEFT = 1
RIGHT = 2
BOTTOM = 4
TOP = 8

x0, y0, x1, y1 = 300, 20, 50, 450
rect = Rect(150, 400, 150, 400)


def lineClip(rect, x1, y1, x2, y2):
    global x, y
    cStart = compCode(x1, y1, rect)
    cEnd = compCode(x2, y2, rect)
    while cStart != 0 or cEnd != 0:     # 处理至少一个顶点在窗口之外的情况
        if (cStart & cEnd) != 0:
            return
        if cStart == 0:
            cStart, cEnd = cEnd, cStart
            x1, y1, x2, y2 = x2, y2, x1, y1
        code = cStart
        if LEFT & code != 0:        # 线段与左边界相交
            x = rect.xMin
            y = y1 + (y2-y1) * (rect.xMin - x1)/(x2 - x1)
        elif (RIGHT & code) != 0:   # 线段与右边界相交
            x = rect.xMax
            y = y1 + (y2 - y1) * (rect.xMax - x1) / (x2 - x1)
        elif (BOTTOM & code) != 0:  # 线段与下边界相交
            y = rect.yMin
            x = x1 + (x2 - x1) * (rect.yMin - y1)/(y2 - y1)
        elif (TOP & code) != 0:     # 线段与上边界相交
            y = rect.ymax
            x = x1 + (x2 - x1) * (rect.yMax - y1)/(y2 - y1)
        x1, y1 = x, y
        cStart = compCode(x, y, rect)

    print(x1, y1, x2, y2)
    glBegin(GL_LINES)
    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()
    glutSwapBuffers()


def compCode(x, y, rect):
    global LEFT, RIGHT, BOTTOM, TOP
    code = 0
    if y < rect.yMin:
        code = code | BOTTOM
    if y > rect.yMax:
        code = code | TOP
    if x > rect.xMax:
        code = code | RIGHT
    if x < rect.xMin:
        code = code | LEFT
    return code


def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, width, 0.0, height)


def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)
    glRectf(rect.xMin, rect.yMin, rect.xMax, rect.yMax)
    drawLine(x0, y0, x1, y1)
    glutSwapBuffers()


def Init():
    global rect, x0, y0, x1, y1
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glShadeModel(GL_FLAT)

    rect.xMin = 150
    rect.xMax = 400
    rect.yMin = 100
    rect.yMax = 400
    x0, y0, x1, y1 = 300, 20, 50, 450

    print("Press key '\\r' to Clip!")
    print("Press key ' ' to Restore!")


def drawLine(x0, y0, x1, y1):
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 1.0)
    glVertex2f(x0, y0)
    glVertex2f(x1, y1)
    glEnd()


def keyboard(key, x, y):
    global rect
    if key == b'\r':    # 回车键 裁剪
        lineClip(rect, x0, y0, x1, y1)
    if key == b' ':     # 空格键 恢复
        Init()
        glutPostRedisplay()
    if key == b'x':     # x：退出
        exit()


if __name__ == "__main__":
    glutInit()  # 启动glut
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("Cohen_Sutherland")  # 设定窗口标题

    Init()
    glutDisplayFunc(draw)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutMainLoop()
