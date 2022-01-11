from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Lines import *
import time

angle = 0


def idle():
    global angle
    angle = angle + 1
    if angle == 360:
        angle = 0
    draw()
    time.sleep(0.02)


def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    line.setAngle(angle)
    line.draw()
    glutSwapBuffers()


if __name__ == "__main__":
    line = Lines()
    glutInit()  # 启动glut
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(500, 500)
    glutCreateWindow("Bresenham")  # 设定窗口标题
    glutDisplayFunc(draw)
    glutIdleFunc(idle)

    glClearColor(0.0, 0.0, 0.0, 0.0)  # 清空颜色
    gluOrtho2D(0.0, 500.0, 0.0, 500.0)
    glutMainLoop()


