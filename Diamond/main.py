from OpenGL.GLU import *
from OpenGL.GLUT import *
from Diamond import *
import time

angle = 0


def idle():
    global angle
    angle = angle + 1
    if angle == 360:
        angle = 0
    draw()
    time.sleep(0.05)


def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    diamond.setAngle(angle)
    diamond.draw()
    glutSwapBuffers()


if __name__ == "__main__":
    diamond = Diamond()
    glutInit()  # 启动glut
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(500, 500)
    glutCreateWindow("Diamond")  # 设定窗口标题
    glutDisplayFunc(draw)
    glutIdleFunc(idle)
    gluOrtho2D(0.0, 500.0, 0.0, 500.0)
    glutMainLoop()


