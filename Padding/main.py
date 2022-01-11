# 区域八邻域点泛填充算法
from cv2 import EVENT_LBUTTONDOWN
from Stack import *
from Point import *
import numpy as np
import cv2 as cv


class Padding:
    """
    区域八邻域点泛填充算法
    """
    oldClr, newClr, backClr = np.array([0, 0, 222]), np.array([0, 255, 0]), np.array([255, 255, 255])
    nodeStack = Stack()
    seed = Point()

    def __init__(self):
        self.image = cv.imread('example.bmp')
        self.height, self.width = self.image.shape[:2]  # 获取宽和高
        cv.imshow("demo", self.image)
        cv.setMouseCallback("demo", self.OnMouseAction)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def OnMouseAction(self, event, x, y, flag, param):
        if event == EVENT_LBUTTONDOWN:
            self.setSeed(x, y)

    def setSeed(self, x, y):
        self.seed.x, self.seed.y = x, y
        self.image = self.image[:, :, 0:3]
        if np.all(self.image[self.seed.y, self.seed.x] == self.oldClr):
            self.floodFill8()

    def floodFill8(self):
        # i = 1
        self.nodeStack.push(self.seed)
        while not self.nodeStack.isEmpty():
            left, right, top, bottom = Point(), Point(), Point(), Point()
            leftTop, rightTop, leftBottom, rightBottom = Point(), Point(), Point(), Point()
            temp = self.nodeStack.pop()
            self.image[temp.y, temp.x] = self.newClr
            # left
            left.x, left.y = temp.x - 1, temp.y
            if np.all(self.image[left.y, left.x] == self.oldClr):
                self.nodeStack.push(left)
            # top
            top.x, top.y = temp.x, temp.y - 1
            if np.all(self.image[top.y, top.x] == self.oldClr):
                self.nodeStack.push(top)
            # right
            right.x, right.y = temp.x + 1, temp.y
            if np.all(self.image[right.y, right.x] == self.oldClr):
                self.nodeStack.push(right)
            # bottom
            bottom.x, bottom.y = temp.x, temp.y + 1
            if np.all(self.image[bottom.y, bottom.x] == self.oldClr):
                self.nodeStack.push(bottom)
            # leftTop
            leftTop.x, leftTop.y = temp.x - 1, temp.y - 1
            if np.all(self.image[leftTop.y, leftTop.x] == self.oldClr):
                self.nodeStack.push(leftTop)
            # leftBottom
            leftBottom.x, leftBottom.y = temp.x - 1, temp.y + 1
            if np.all(self.image[leftBottom.y, leftBottom.x] == self.oldClr):
                self.nodeStack.push(leftBottom)
            # rightTop
            rightTop.x, rightTop.y = temp.x + 1, temp.y - 1
            if np.all(self.image[rightTop.y, rightTop.x] == self.oldClr):
                self.nodeStack.push(rightTop)
            # rightBottom
            rightBottom.x, rightBottom.y = temp.x + 1, temp.y + 1
            if np.all(self.image[rightBottom.y, rightBottom.x] == self.oldClr):
                self.nodeStack.push(rightBottom)
            print('ok')
            # i = i+1
            # if i > 40000:
            #     break
        print("over")
        import cv2
        cv2.imshow("result", self.image)


if __name__ == "__main__":
    pad = Padding()
