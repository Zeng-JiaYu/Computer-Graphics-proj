# 栈

class Stack:
    """堆栈结构类"""

    def __init__(self):
        self._item = []

    def push(self, item):
        """
        添加新元素
        :param item
        :return:
        """
        self._item.append(item)

    def pop(self):
        """
        弹出栈顶元素
        :return:
        """
        return self._item.pop()

    def peek(self):
        """
        返回栈顶元素
        :return:
        """
        return self._item[-1]

    def isEmpty(self):
        """
        判断是否为空
        :return:
        """
        if not self._item:
            return True
        else:
            return False

    def count(self):
        return len(self._item)
