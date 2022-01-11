from MainWindow_UI import *
from PyQt5.QtWidgets import *


class MainWindow(QMainWindow, Ui_MainWindow):
    """重写主窗体类"""
    # 初始化
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("三维动态球体")
        self.setupUi(self)

    def close(self):
        self.openGLWidget.timer.destroyed()
        return False

    def start(self):
        self.openGLWidget.timer.start()

    def stop(self):
        self.openGLWidget.timer.stop()

    # 设置改变，操作更新
    def draw(self):
        self.openGLWidget.ball.drawGeometry()   # 重新计算点表
        self.openGLWidget.update()
        self.openGLWidget.grabFramebuffer()

    # 设置半径 radius:0-20
    def setRadius(self):
        value = self.r_slider.value()
        self.openGLWidget.ball.radius = value
        self.draw()    # 更新

    # 设置分割级数 count:0-7
    def setCount(self):
        value = self.count_slider.value()
        self.openGLWidget.ball.count = value
        self.draw()    # 更新

    # 设置样式 线框/实体
    def setPattern(self):
        value = 0 if self.line_button.isChecked() else 1    # 线框
        value = 1 if self.entity_button.isChecked() else 0  # 实体
        self.openGLWidget.ball.pattern = value
        self.draw()     # 更新

    # 设置光照
    def setLight(self):
        value = 1 if self.off_light.isChecked() else 0  # 光照打开
        value = 0 if self.on_light.isChecked() else 1   # 光照关闭
        self.openGLWidget.ball.lighting = value
        self.draw()    # 更新

    # 设置X轴平移速度
    def setSpeedX(self):
        value = self.x_move.value()/10
        self.openGLWidget.ball.speedX = value
        self.draw()     # 更新

    # 设置Y轴平移速度
    def setSpeedY(self):
        value = self.y_move.value()/10
        self.openGLWidget.ball.speedY = value
        self.draw()     # 更新

    # 设置Z轴平移速度
    def setSpeedZ(self):
        value = self.z_move.value()/10
        self.openGLWidget.ball.speedZ = value
        self.draw()     # 更新

    # 设置X轴旋转率
    def setRateX(self):
        value = self.x_rotation.value()/10

        self.openGLWidget.ball.rateX = value
        self.draw()     # 更新

    # 设置Y轴旋转率
    def setRateY(self):
        value = self.y_rotation.value()/10
        self.openGLWidget.ball.rateY = value
        self.draw()     # 更新

    # 设置Z轴旋转率
    def setRateZ(self):
        value = self.z_rotation.value()/10
        self.openGLWidget.ball.rateZ = value
        self.draw()     # 更新


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
