import sys
import time
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL.Image import *
import numpy as np

from Planet import *

window = 0
rot = 0.0
rot2 = 0.0
rot3 = 0.0
rot4 = 0.0
rot5 = 0.0
rot6 = 0.0
rot7 = 0.0
rot8 = 0.0

LightAmb = (0.7, 0.7, 0.7)
LightDif = (1.0, 1.0, 0.0)
LightPos = (4.0, 4.0, 6.0, 1.0)

textures = {}

IS_PERSPECTIVE = True  # 透视投影
VIEW = np.array([-0.8, 0.8, -0.8, 0.8, 1.0, 20.0])  # 视景体的left/right/bottom/top/near/far六个面
SCALE_K = np.array([1.0, 1.0, 1.0])  # 模型缩放比例
EYE = np.array([0.0, 0.0, 2.0])  # 眼睛的位置（默认z轴的正方向）
LOOK_AT = np.array([0.0, 0.0, 0.0])  # 瞄准方向的参考点（默认在坐标原点）
EYE_UP = np.array([0.0, 1.0, 0.0])  # 定义对观察者而言的上方（默认y轴的正方向）
WIN_W, WIN_H = 612, 540  # 保存窗口宽度和高度的变量
LEFT_IS_DOWNED = False  # 鼠标左键被按下
MOUSE_X, MOUSE_Y = 0, 0  # 考察鼠标位移量时保存的起始位置


def getPosture():
    global EYE, LOOK_AT

    dist = np.sqrt(np.power((EYE - LOOK_AT), 2).sum())
    if dist > 0:
        phi = np.arcsin((EYE[1] - LOOK_AT[1]) / dist)
        theta = np.arcsin((EYE[0] - LOOK_AT[0]) / (dist * np.cos(phi)))
    else:
        phi = 0.0
        theta = 0.0

    return dist, phi, theta


DIST, PHI, THETA = getPosture()  # 眼睛与观察目标之间的距离、仰角、方位角


# A general OpenGL initialization function.  Sets all of the initial parameters.
def InitGL(Width, Height):  # We call this right after our OpenGL window is created.
    glClearColor(0.0, 0.0, 0.0, 0.0)  # This Will Clear The Background Color To Black
    glClearDepth(1.0)  # Enables Clearing Of The Depth Buffer
    glClearStencil(0)
    glDepthFunc(GL_LEQUAL)  # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)  # Enables Depth Testing
    glShadeModel(GL_SMOOTH)  # Enables Smooth Color Shading

    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glEnable(GL_TEXTURE_2D)

    glLightfv(GL_LIGHT0, GL_AMBIENT, LightAmb)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, LightDif)
    glLightfv(GL_LIGHT0, GL_POSITION, LightPos)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()  # Reset The Projection Matrix

    glMatrixMode(GL_MODELVIEW)


# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
    if Height == 0:  # Prevent A Divide By Zero If The Window Is Too Small
        Height = 1

    glViewport(0, 0, Width, Height)  # Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def drawGLScene():
    global IS_PERSPECTIVE, VIEW
    global EYE, LOOK_AT, EYE_UP
    global SCALE_K
    global WIN_W, WIN_H

    # 清除屏幕及深度缓存
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # 设置投影（透视投影）
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    if WIN_W > WIN_H:
        if IS_PERSPECTIVE:
            glFrustum(VIEW[0] * WIN_W / WIN_H, VIEW[1] * WIN_W / WIN_H, VIEW[2], VIEW[3], VIEW[4], VIEW[5])
        else:
            glOrtho(VIEW[0] * WIN_W / WIN_H, VIEW[1] * WIN_W / WIN_H, VIEW[2], VIEW[3], VIEW[4], VIEW[5])
    else:
        if IS_PERSPECTIVE:
            glFrustum(VIEW[0], VIEW[1], VIEW[2] * WIN_H / WIN_W, VIEW[3] * WIN_H / WIN_W, VIEW[4], VIEW[5])
        else:
            glOrtho(VIEW[0], VIEW[1], VIEW[2] * WIN_H / WIN_W, VIEW[3] * WIN_H / WIN_W, VIEW[4], VIEW[5])

    # 设置模型视图
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # 几何变换
    glScale(SCALE_K[0], SCALE_K[1], SCALE_K[2])

    # 设置视点
    gluLookAt(
        EYE[0], EYE[1], EYE[2],
        LOOK_AT[0], LOOK_AT[1], LOOK_AT[2],
        EYE_UP[0], EYE_UP[1], EYE_UP[2]
    )

    # 设置视口
    glViewport(0, 0, WIN_W, WIN_H)

    # ---------------------------------------------------------------
    glBegin(GL_LINES)  # 开始绘制线段（世界坐标系）

    # 以红色绘制x轴
    glColor4f(1.0, 0.0, 0.0, 1.0)  # 设置当前颜色为红色不透明
    glVertex3f(-0.8, 0.0, 0.0)  # 设置x轴顶点（x轴负方向）
    glVertex3f(0.8, 0.0, 0.0)  # 设置x轴顶点（x轴正方向）

    # 以绿色绘制y轴
    glColor4f(0.0, 1.0, 0.0, 1.0)  # 设置当前颜色为绿色不透明
    glVertex3f(0.0, -0.8, 0.0)  # 设置y轴顶点（y轴负方向）
    glVertex3f(0.0, 0.8, 0.0)  # 设置y轴顶点（y轴正方向）

    # 以蓝色绘制z轴
    glColor4f(0.0, 0.0, 1.0, 1.0)  # 设置当前颜色为蓝色不透明
    glVertex3f(0.0, 0.0, -0.8)  # 设置z轴顶点（z轴负方向）
    glVertex3f(0.0, 0.0, 0.8)  # 设置z轴顶点（z轴正方向）

    glEnd()  # 结束绘制线段
    # ---------------------------------------------------------------
    # glBegin(GL_TRIANGLES)  # 开始绘制三角形（z轴负半区）
    #
    # glColor4f(1.0, 0.0, 0.0, 1.0)  # 设置当前颜色为红色不透明
    # glVertex3f(-0.5, -0.366, -0.5)  # 设置三角形顶点
    # glColor4f(0.0, 1.0, 0.0, 1.0)  # 设置当前颜色为绿色不透明
    # glVertex3f(0.5, -0.366, -0.5)  # 设置三角形顶点
    # glColor4f(0.0, 0.0, 1.0, 1.0)  # 设置当前颜色为蓝色不透明
    # glVertex3f(0.0, 0.5, -0.5)  # 设置三角形顶点
    #
    # glEnd()  # 结束绘制三角形
    #
    # # ---------------------------------------------------------------
    # glBegin(GL_TRIANGLES)  # 开始绘制三角形（z轴正半区）
    #
    # glColor4f(1.0, 0.0, 0.0, 1.0)  # 设置当前颜色为红色不透明
    # glVertex3f(-0.5, 0.5, 0.5)  # 设置三角形顶点
    # glColor4f(0.0, 1.0, 0.0, 1.0)  # 设置当前颜色为绿色不透明
    # glVertex3f(0.5, 0.5, 0.5)  # 设置三角形顶点
    # glColor4f(0.0, 0.0, 1.0, 1.0)  # 设置当前颜色为蓝色不透明
    # glVertex3f(0.0, -0.366, 0.5)  # 设置三角形顶点
    #
    # glEnd()  # 结束绘制三角形

    global rot, rot2, rot3, rot4, rot5, rot6, rot7, rot8
    mercury = Planet('res/mercury.bmp', 1.9, 0.2)
    venus = Planet('res/venus.bmp', 3, 0.3)
    earth = Planet('res/earth.bmp', 4, 0.4)
    mars = Planet('res/mars.bmp', 5.5, 0.45)
    jupiter = Planet('res/jupiter.bmp', 7, 0.6)
    saturn = Planet('res/saturn.bmp', 8.5, 0.55)
    uranus = Planet('res/uranus.bmp', 10, 0.55)
    neptune = Planet('res/neptune.bmp', 11.5, 0.45)
    sun = Planet('res/sun.tga', 0, 0.7)

    # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear The Screen And The Depth Buffer
    glLoadIdentity()  # Reset The View

    glTranslatef(0.0, 0.0, -20.0)  # Move Into The Screen

    glRotatef(rot, 1.0, 0.0, 0.0)  # Rotate The Cube On It's X Axis
    glRotatef(rot, 0.0, 1.0, 0.0)  # Rotate The Cube On Its's Y Axis
    glRotatef(-1, 0.0, 0.0, 1.0)  # Rotate The Cube On It's Z Axis
    mercury.drawPlanet()
    rot = (rot + 0.16) % 360  # rotation

    glRotatef(rot2, 1.0, 0.0, 0.0)  # Rotate The Cube On It's X Axis
    glRotatef(rot2, 0.0, 1.0, 0.0)  # Rotate The Cube On Its's Y Axis
    glRotatef(-1, 0.0, 0.0, 1.0)  # Rotate The Cube On It's Z Axis
    venus.drawPlanet()
    rot2 = (rot2 + 0.14) % 360

    glRotatef(rot3, 1.0, 0.0, 0.0)  # Rotate The Cube On It's X Axis
    glRotatef(rot3, 0.0, 1.0, 0.0)  # Rotate The Cube On Its's Y Axis
    glRotatef(-1, 0.0, 0.0, 1.0)  # Rotate The Cube On It's Z Axis
    earth.drawPlanet()
    rot3 = (rot3 + 0.12) % 360

    glRotatef(rot4, 1.0, 0.0, 0.0)  # Rotate The Cube On It's X Axis
    glRotatef(rot4, 0.0, 1.0, 0.0)  # Rotate The Cube On Its's Y Axis
    glRotatef(-1, 0.0, 0.0, 1.0)  # Rotate The Cube On It's Z Axis
    mars.drawPlanet()
    rot4 = (rot3 + 0.010) % 360

    glRotatef(rot5, 1.0, 0.0, 0.0)  # Rotate The Cube On It's X Axis
    glRotatef(rot5, 0.0, 1.0, 0.0)  # Rotate The Cube On Its's Y Axis
    glRotatef(-1, 0.0, 0.0, 1.0)  # Rotate The Cube On It's Z Axis
    jupiter.drawPlanet()
    rot5 = (rot3 + 0.008) % 360

    glRotatef(rot6, 1.0, 0.0, 0.0)  # Rotate The Cube On It's X Axis
    glRotatef(rot6, 0.0, 1.0, 0.0)  # Rotate The Cube On Its's Y Axis
    glRotatef(-1, 0.0, 0.0, 1.0)  # Rotate The Cube On It's Z Axis
    saturn.drawPlanet(True)
    rot6 = (rot3 + 0.006) % 360

    glRotatef(rot7, 1.0, 0.0, 0.0)  # Rotate The Cube On It's X Axis
    glRotatef(rot7, 0.0, 1.0, 0.0)  # Rotate The Cube On Its's Y Axis
    glRotatef(-1, 0.0, 0.0, 1.0)  # Rotate The Cube On It's Z Axis
    uranus.drawPlanet()
    rot7 = (rot3 + 0.004) % 360

    glRotatef(rot8, 1.0, 0.0, 0.0)  # Rotate The Cube On It's X Axis
    glRotatef(rot8, 0.0, 1.0, 0.0)  # Rotate The Cube On Its's Y Axis
    glRotatef(-1, 0.0, 0.0, 1.0)  # Rotate The Cube On It's Z Axis
    neptune.drawPlanet()
    rot8 = (rot8 + 0.002) % 360

    sun.drawPlanet()

    #  since this is double buffered, swap the buffers to display what just got drawn.
    glutSwapBuffers()

    time.sleep(0.002)


def idleGLScene():
    global rot, rot2, rot3, rot4, rot5, rot6, rot7, rot8
    mercury = Planet('res/mercury.bmp', 1.9, 0.2)
    venus = Planet('res/venus.bmp', 3, 0.3)
    earth = Planet('res/earth.bmp', 4, 0.4)
    mars = Planet('res/mars.bmp', 5.5, 0.45)
    jupiter = Planet('res/jupiter.bmp', 7, 0.6)
    saturn = Planet('res/saturn.bmp', 8.5, 0.55)
    uranus = Planet('res/uranus.bmp', 10, 0.55)
    neptune = Planet('res/neptune.bmp', 11.5, 0.45)
    sun = Planet('res/sun.tga', 0, 0.7)

    # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear The Screen And The Depth Buffer
    glLoadIdentity()  # Reset The View

    glTranslatef(0.0, 0.0, -20.0)  # Move Into The Screen

    glRotatef(rot, 1.0, 0.0, 0.0)  # Rotate The Cube On It's X Axis
    glRotatef(rot, 0.0, 1.0, 0.0)  # Rotate The Cube On Its's Y Axis
    glRotatef(-1, 0.0, 0.0, 1.0)  # Rotate The Cube On It's Z Axis
    mercury.drawPlanet()
    rot = (rot + 0.16) % 360  # rotation

    glRotatef(rot2, 1.0, 0.0, 0.0)  # Rotate The Cube On It's X Axis
    glRotatef(rot2, 0.0, 1.0, 0.0)  # Rotate The Cube On Its's Y Axis
    glRotatef(-1, 0.0, 0.0, 1.0)  # Rotate The Cube On It's Z Axis
    venus.drawPlanet()
    rot2 = (rot2 + 0.14) % 360

    glRotatef(rot3, 1.0, 0.0, 0.0)  # Rotate The Cube On It's X Axis
    glRotatef(rot3, 0.0, 1.0, 0.0)  # Rotate The Cube On Its's Y Axis
    glRotatef(-1, 0.0, 0.0, 1.0)  # Rotate The Cube On It's Z Axis
    earth.drawPlanet()
    rot3 = (rot3 + 0.12) % 360

    glRotatef(rot4, 1.0, 0.0, 0.0)  # Rotate The Cube On It's X Axis
    glRotatef(rot4, 0.0, 1.0, 0.0)  # Rotate The Cube On Its's Y Axis
    glRotatef(-1, 0.0, 0.0, 1.0)  # Rotate The Cube On It's Z Axis
    mars.drawPlanet()
    rot4 = (rot3 + 0.010) % 360

    glRotatef(rot5, 1.0, 0.0, 0.0)  # Rotate The Cube On It's X Axis
    glRotatef(rot5, 0.0, 1.0, 0.0)  # Rotate The Cube On Its's Y Axis
    glRotatef(-1, 0.0, 0.0, 1.0)  # Rotate The Cube On It's Z Axis
    jupiter.drawPlanet()
    rot5 = (rot3 + 0.008) % 360

    glRotatef(rot6, 1.0, 0.0, 0.0)  # Rotate The Cube On It's X Axis
    glRotatef(rot6, 0.0, 1.0, 0.0)  # Rotate The Cube On Its's Y Axis
    glRotatef(-1, 0.0, 0.0, 1.0)  # Rotate The Cube On It's Z Axis
    saturn.drawPlanet(True)
    rot6 = (rot3 + 0.006) % 360

    glRotatef(rot7, 1.0, 0.0, 0.0)  # Rotate The Cube On It's X Axis
    glRotatef(rot7, 0.0, 1.0, 0.0)  # Rotate The Cube On Its's Y Axis
    glRotatef(-1, 0.0, 0.0, 1.0)  # Rotate The Cube On It's Z Axis
    uranus.drawPlanet()
    rot7 = (rot3 + 0.004) % 360

    glRotatef(rot8, 1.0, 0.0, 0.0)  # Rotate The Cube On It's X Axis
    glRotatef(rot8, 0.0, 1.0, 0.0)  # Rotate The Cube On Its's Y Axis
    glRotatef(-1, 0.0, 0.0, 1.0)  # Rotate The Cube On It's Z Axis
    neptune.drawPlanet()
    rot8 = (rot8 + 0.002) % 360

    sun.drawPlanet()

    #  since this is double buffered, swap the buffers to display what just got drawn.
    glutSwapBuffers()

    time.sleep(0.0002)


def mouseclick(button, state, x, y):
    global SCALE_K
    global LEFT_IS_DOWNED
    global MOUSE_X, MOUSE_Y

    MOUSE_X, MOUSE_Y = x, y
    if button == GLUT_LEFT_BUTTON:
        LEFT_IS_DOWNED = state == GLUT_DOWN
    elif button == 3:
        SCALE_K *= 1.05
        glutPostRedisplay()
    elif button == 4:
        SCALE_K *= 0.95
        glutPostRedisplay()


def mouseMotion(x, y):
    global LEFT_IS_DOWNED
    global EYE, EYE_UP
    global MOUSE_X, MOUSE_Y
    global DIST, PHI, THETA
    global WIN_W, WIN_H

    if LEFT_IS_DOWNED:
        dx = MOUSE_X - x
        dy = y - MOUSE_Y
        MOUSE_X, MOUSE_Y = x, y

        PHI += 2 * np.pi * dy / WIN_H
        PHI %= 2 * np.pi
        THETA += 2 * np.pi * dx / WIN_W
        THETA %= 2 * np.pi
        r = DIST * np.cos(PHI)

        EYE[1] = DIST * np.sin(PHI)
        EYE[0] = r * np.sin(THETA)
        EYE[2] = r * np.cos(THETA)

        if 0.5 * np.pi < PHI < 1.5 * np.pi:
            EYE_UP[1] = -1.0
        else:
            EYE_UP[1] = 1.0

        glutPostRedisplay()


def keyDown(key, x, y):
    global DIST, PHI, THETA
    global EYE, LOOK_AT, EYE_UP
    global IS_PERSPECTIVE, VIEW

    if key in [b'x', b'X', b'y', b'Y', b'z', b'Z']:
        if key == b'x':  # 瞄准参考点 x 减小
            LOOK_AT[0] -= 0.01
        elif key == b'X':  # 瞄准参考 x 增大
            LOOK_AT[0] += 0.01
        elif key == b'y':  # 瞄准参考点 y 减小
            LOOK_AT[1] -= 0.01
        elif key == b'Y':  # 瞄准参考点 y 增大
            LOOK_AT[1] += 0.01
        elif key == b'z':  # 瞄准参考点 z 减小
            LOOK_AT[2] -= 0.01
        elif key == b'Z':  # 瞄准参考点 z 增大
            LOOK_AT[2] += 0.01

        DIST, PHI, THETA = getPosture()
        glutPostRedisplay()
    elif key == b'\r':  # 回车键，视点前进
        EYE = LOOK_AT + (EYE - LOOK_AT) * 0.9
        DIST, PHI, THETA = getPosture()
        glutPostRedisplay()
    elif key == b'\x08':  # 退格键，视点后退
        EYE = LOOK_AT + (EYE - LOOK_AT) * 1.1
        DIST, PHI, THETA = getPosture()
        glutPostRedisplay()
    elif key == b' ':  # 空格键，切换投影模式
        IS_PERSPECTIVE = not IS_PERSPECTIVE
        glutPostRedisplay()


def main():
    """主程序"""
    global window
    glutInit(sys.argv)  # 对GLUT进行初始化
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)  # 设置显示方式
    glutInitWindowSize(612, 540)  # 设置窗口大小
    glutInitWindowPosition(0, 0)  # 设置窗口在屏幕中的位置
    window = glutCreateWindow("Solar System")  # 创建窗口
    glutDisplayFunc(drawGLScene)  # 绘图
    # glutFullScreen()              # 全屏显示
    glutIdleFunc(drawGLScene)  # 重绘屏幕
    glutReshapeFunc(ReSizeGLScene)  # 初始化窗口
    glutMouseFunc(mouseclick)  # 注册响应鼠标点击的函数mouseclick()
    glutMotionFunc(mouseMotion)  # 注册响应鼠标拖拽的函数mousemotion()
    glutKeyboardFunc(keyDown)  # 注册键盘输入的函数keydown()
    InitGL(612, 540)
    glutMainLoop()  # 消息循环
    return window


if __name__ == "__main__":
    main()
