from BallDoc import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtGui import QOpenGLVersionProfile

IS_PERSPECTIVE = True  # 透视投影

# 光照
MAT_AMBIENT = [0.8, 0.8, 0.8, 1.0]
MAT_DIFFUSE = [0.8, 0.8, 0.8, 1.0]
MAT_SPECULAR = [0.1, 0.1, 0.1, 1.0]
MAT_SHININESS = [50]

LIGHT_DIFFUSE = [0.0, 1.0, 0.0, 1.0]
LIGHT_POSITION = [1.0, 1.0, 1.0, 0.0]


class BallView(QOpenGLWidget):
    ball = BallDoc()

    def __init__(self, parent=None):
        super(BallView, self).__init__(parent)
        self.ball.drawGeometry()  # 计算点表

        # 计时器
        self.timer = QTimer()
        self.timer.setInterval(10)  # 10ms
        self.timer.timeout.connect(self.moving)

    def moving(self):
        # 计算反弹边界值
        boundaryX, boundaryY, boundaryZ = 20 - self.ball.radius, 20 - self.ball.radius, 50 - self.ball.radius

        # x轴反弹
        self.ball.directionX = False if self.ball.translateX > boundaryX else self.ball.directionX
        self.ball.directionX = True if self.ball.translateX < -boundaryX else self.ball.directionX
        self.ball.translateX = self.ball.translateX + self.ball.speedX if self.ball.directionX \
            else self.ball.translateX - self.ball.speedX

        # y轴反弹
        self.ball.directionY = False if self.ball.translateY > boundaryY else self.ball.directionY
        self.ball.directionY = True if self.ball.translateY < -boundaryY else self.ball.directionY
        self.ball.translateY = self.ball.translateY + self.ball.speedY if self.ball.directionY \
            else self.ball.translateY - self.ball.speedY

        # z轴反弹
        self.ball.directionZ = False if self.ball.translateZ > -25 else self.ball.directionZ
        self.ball.directionZ = True if self.ball.translateZ < -35 else self.ball.directionZ
        self.ball.translateZ = self.ball.translateZ + self.ball.speedZ if self.ball.directionZ \
            else self.ball.translateZ - self.ball.speedZ

        # 旋转角变换
        self.ball.rotateX += self.ball.rateX
        self.ball.rotateY += self.ball.rateY
        self.ball.rotateZ += self.ball.rateZ

        # 更新
        self.update()
        self.grabFramebuffer()

    def initializeGL(self):
        # 设置渲染context,加载shader和资源等
        version_profile = QOpenGLVersionProfile()
        version_profile.setVersion(2, 0)
        self.gl = self.context().versionFunctions(version_profile)
        self.gl.initializeOpenGLFunctions()

        self.gl.glMatrixMode(self.gl.GL_MODELVIEW)  # 模型视图模式
        self.gl.glLoadIdentity()  # 重置当前指定的矩阵为单位矩阵
        # 深度测试
        self.gl.glEnable(self.gl.GL_DEPTH_TEST)

    def paintGL(self):
        self.gl.glDrawBuffer(GL_BACK)  # 指定在后台缓存中绘制图形
        self.gl.glLoadIdentity()  # 初始化变换矩阵

        self.gl.glClearColor(0, 0, 0, 1.0)  # 设置背景色
        self.gl.glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.gl.glPushMatrix()
        self.gl.glShadeModel(GL_SMOOTH)

        # 光照
        self.gl.glMaterialfv(GL_FRONT, GL_AMBIENT, MAT_AMBIENT)
        self.gl.glMaterialfv(GL_FRONT, GL_DIFFUSE, MAT_DIFFUSE)
        self.gl.glMaterialfv(GL_FRONT, GL_SPECULAR, MAT_SPECULAR)
        self.gl.glMaterialfv(GL_FRONT, GL_SHININESS, MAT_SHININESS)

        self.gl.glLightfv(GL_LIGHT0, GL_DIFFUSE, LIGHT_DIFFUSE)
        self.gl.glLightfv(GL_LIGHT0, GL_POSITION, LIGHT_POSITION)

        # 开启/关闭光照
        if self.ball.lighting == 0:
            self.gl.glDisable(GL_LIGHTING)
        else:
            self.gl.glEnable(GL_LIGHTING)
        self.gl.glEnable(GL_LIGHT0)     # 启用0号光源

        # 深度测试
        self.gl.glDepthFunc(GL_LESS)
        self.gl.glEnable(GL_DEPTH_TEST)

        # 平移变换
        self.gl.glTranslated(self.ball.translateX, 0.0, 0.0)
        self.gl.glTranslated(0.0, self.ball.translateY, 0.0)
        self.gl.glTranslated(0.0, 0.0, self.ball.translateZ)

        # 旋转变换
        self.gl.glRotated(self.ball.rotateX, 1.0, 0.0, 0.0)
        self.gl.glRotated(self.ball.rotateY, 0.0, 1.0, 0.0)
        self.gl.glRotated(self.ball.rotateZ, 0.0, 0.0, 1.0)

        # 画图
        self.gl.glBegin(GL_LINES)  # 开始绘制线段（世界坐标系）

        # 以红色绘制x轴
        self.gl.glColor4f(1.0, 0.0, 0.0, 1.0)  # 设置当前颜色为红色不透明
        self.gl.glVertex3f(-(self.ball.radius+5), 0.0, 0.0)  # 设置x轴顶点（x轴负方向）
        self.gl.glVertex3f((self.ball.radius+5), 0.0, 0.0)  # 设置x轴顶点（x轴正方向）

        # 以绿色绘制y轴
        self.gl.glColor4f(0.0, 1.0, 0.0, 1.0)  # 设置当前颜色为绿色不透明
        self.gl.glVertex3f(0.0, -(self.ball.radius+5), 0.0)  # 设置y轴顶点（y轴负方向）
        self.gl.glVertex3f(0.0, (self.ball.radius+5), 0.0)  # 设置y轴顶点（y轴正方向）

        # 以蓝色绘制z轴
        self.gl.glColor4f(0.0, 0.0, 1.0, 1.0)  # 设置当前颜色为蓝色不透明
        self.gl.glVertex3f(0.0, 0.0, -(self.ball.radius+5))  # 设置z轴顶点（z轴负方向）
        self.gl.glVertex3f(0.0, 0.0, (self.ball.radius+5))  # 设置z轴顶点（z轴正方向）
        self.gl.glEnd()  # 结束绘制线段

        # 绘制球体
        self.gl.glColor4f(1.0, 1.0, 1.0, 1.0)  # 设置当前颜色为蓝色不透明
        if self.ball.pattern == 0:
            self.ball.pattern = self.gl.GL_LINE_LOOP
        elif self.ball.pattern == 1:
            self.ball.pattern = self.gl.GL_TRIANGLES
        for i in range(len(self.ball.vertex)):
            self.gl.glBegin(self.ball.pattern)
            self.gl.glNormal3fv(self.ball.normal[i])
            self.gl.glVertex3d(self.ball.vertex[i][0][0], self.ball.vertex[i][0][1], self.ball.vertex[i][0][2])
            self.gl.glVertex3d(self.ball.vertex[i][1][0], self.ball.vertex[i][1][1], self.ball.vertex[i][1][2])
            self.gl.glVertex3d(self.ball.vertex[i][2][0], self.ball.vertex[i][2][1], self.ball.vertex[i][2][2])
            self.gl.glEnd()

        # 画图结束
        self.gl.glPopMatrix()
        self.gl.glFinish()  # 结束整个绘制

        # self.gl.glutSwapBuffers()   # 交换前后缓存
        self.gl.glDrawBuffer(GL_FRONT)  # 绘制前景

    def resizeGL(self, width, height):
        # 视点设置

        # 视口大小出错
        side = min(width, height)
        if side < 0:
            return

        # 设置视口大小
        self.gl.glViewport(0, 0, width, height)
        self.gl.glMatrixMode(self.gl.GL_PROJECTION)  # 投影模式
        self.gl.glLoadIdentity()  # 重置当前指定的矩阵为单位矩阵

        if width <= height:  # 根据窗口大小调整正射投影矩阵
            if IS_PERSPECTIVE:
                self.gl.glFrustum(-1.0, 1.0,
                                  -1.0 * height / width, 1 * height / width,
                                  1, 50.0)
            else:
                self.gl.glOrtho(-1.0, 1.0,
                                -1.0 * height / width, 1 * height / width,
                                1, 50.0)
        else:
            if IS_PERSPECTIVE:
                self.gl.glFrustum(-1.0 * width / height, 1 * width / height,
                                  -1.0, 1.0,
                                  1, 50.0)
            else:
                self.gl.glOrtho(-20.0 * width / height, 20 * width / height,
                                -20.0, 20.0,
                                -50, 50.0)
        self.gl.glMatrixMode(GL_MODELVIEW)  # 模型视图模式
        self.gl.glLoadIdentity()  # 重置当前指定的矩阵为单位矩阵
