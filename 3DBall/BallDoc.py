import math


class BallDoc:
    radius = 15
    count = 4
    vertex = []
    normal = []

    pattern = 0
    lighting = 0

    speedX = 0.1
    speedY = 0.1
    speedZ = 0.1

    rateX = 0.1
    rateY = 0.1
    rateZ = 0.1

    translateX = 0
    translateY = 0
    translateZ = -20

    rotateX = 0.1
    rotateY = 0.1
    rotateZ = 0.1

    directionX = True
    directionY = True
    directionZ = True

    def drawGeometry(self):
        """绘制球体"""
        self.vertex = []
        self.normal = []
        r = self.radius
        # 初始点坐标
        vdata = [[r, 0.0, 0.0], [-r, 0.0, 0.0],
                 [0.0, r, 0.0], [0.0, -r, 0.0],
                 [0.0, 0.0, r], [0.0, 0.0, -r]]
        # 初始面构造
        tindices = [[2, 4, 0], [2, 0, 5], [2, 5, 1], [2, 1, 4],
                    [3, 0, 4], [3, 5, 0], [3, 1, 5], [3, 4, 1]]

        for i in range(8):
            self.subDivide(vdata[tindices[i][0]],
                           vdata[tindices[i][1]],
                           vdata[tindices[i][2]],
                           self.count)

    def subDivide(self, v1, v2, v3, count):
        """把count为级数，对一个三角形面的子划分"""
        if count <= 0:  # count=0,则画由三点构成的三角形
            self.drawTriangle(v1, v2, v3)
        else:
            v12, v23, v31 = [0] * 3, [0] * 3, [0] * 3
            for i in range(3):
                v12[i] = (v1[i] + v2[i]) / 2
                v23[i] = (v2[i] + v3[i]) / 2
                v31[i] = (v3[i] + v1[i]) / 2
            v12 = self.normalize(v12, self.radius)  # 扩展模长
            v23 = self.normalize(v23, self.radius)
            v31 = self.normalize(v31, self.radius)

            self.subDivide(v1, v12, v31, count - 1)
            self.subDivide(v2, v23, v12, count - 1)
            self.subDivide(v3, v31, v23, count - 1)
            self.subDivide(v12, v23, v31, count - 1)

    def drawTriangle(self, v1, v2, v3):
        """以三点为顶点画三角形"""
        normal = self.normalTriangle(v1, v2, v3)  # 求取面法向量
        newVertex = [v1, v2, v3]
        self.vertex.append(newVertex)
        self.normal.append(normal)

    @staticmethod
    def normalize(v, radius):
        """向量的标准化, 以模长为radius进行标准化"""
        d = math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
        if d == 0:
            return v
        v = [i / d for i in v]
        v = [i * radius for i in v]
        return v

    def normalTriangle(self, v1, v2, v3):
        """求三点构成的三角形面的法向量"""
        vOut, v12, v23 = [0] * 3, [0] * 3, [0] * 3
        for i in range(3):
            v12[i] = v2[i] - v1[i]
            v23[i] = v3[i] - v2[i]
        vOut[0] = v12[1] * v23[2] - v12[2] * v23[1]
        vOut[1] = -(v12[0] * v23[2] - v12[2] * v23[0])
        vOut[2] = v12[0] * v23[1] - v12[1] * v23[0]
        vOut = self.normalize(vOut, 1)
        return vOut
