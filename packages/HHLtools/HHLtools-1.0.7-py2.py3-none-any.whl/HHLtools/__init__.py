#CONSTANTS
class fontstyle():
    DEFAULT = 0
    BOLD = 1
    UNDERLINE = 4
    BLINK = 5
    REVERSE = 7

class color():
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    PURPLE = 35
    CYAN = 36
    WHITE = 37

class backgroundcolor():
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    PURPLE = 45
    CYAN = 46
    WHITE = 47


def fibonacci(n):
    if n < 1 or int(n) != n:
        return "error, n should be a positive number which is greater than 1"
    if n < 3:
        return 1
    a, b = 1, 1

    for i in range(2, n):
        a = a + b if i % 2 == 0 else a
        b = a + b if i % 2 == 1 else b
    return a if a > b else b

def fibonacci_list(n):
    if n < 1 or int(n) != n:
        return "error, n should be a positive number which is greater than 1"
    if n == 1:
        return [1]
    if n == 2:
        return [1, 1]
    list = [1, 1]
    for i in range(2, n):
        list.append(list[i - 2] + list[i - 1])
    return list

class Queue():
    def __init__(self,size:int = -1):
        if size > 0:
            self.__size = size
            self.__queue = [0] * size
            self.__head = 0
            self.__tail = 0
            self.__count = 0
        else:
            self.__queue = []

    @property
    def val(self):
        return self.__queue

    @property
    def count(self):
        return self.__count

    def push(self, content):
        if self.__size > 0:
            if self.__count == self.__size:
                print('the queue is full, try pop()')
                return
            self.__queue[self.__tail] = content
            self.__tail = (self.__tail+1)%self.__size
            self.__count += 1
        else:
            try:
                self.__queue.append(content)
            except:
                print('invalid input')

    def pop(self):
        if self.__size > 0:
            if self.__count == 0:
                print('the queue is empty, try push()')
                return
            print('remove:', self.__queue[self.__head])
            self.__head = (self.__head + 1)%self.__size
            self.__count -= 1
        else:
            try:
                del self.__queue[0]
            except IndexError:
                print('warning : no value in the queue,try add(content) to add one')

class Stack():
    def __init__(self,size:int=-1):
        self.a = 0
        if size > 0:
            self.__stack = [0]*size
        else:
            self.__stack = []
        self.__size = size
        self.__top = -1

    @property
    def val(self):
        return self.__stack

    def push(self, content):
        if self.__size > 0:
            if self.__top < self.__size - 1:
                self.__top += 1
                self.__stack[self.__top] = content
            else:
                print('stack is full, try pop()')
        else:
            self.__stack.insert(0,content)
    def pop(self):
        if self.__size > 0:
            if self.__top > -1:
                print(self.__stack[self.__top])
                self.__top -= 1
            else:
                print('warning : stack is empty ,try push(content)')
        else:
            try:
                print(self.__stack[0])
                del self.__stack[0]
            except IndexError:
                print('warning : stack is empty ,try push(content)')

class Hmath():
    class Functions():
        def __init__(self, expression: str, variable: str):
            self.__expression = expression
            self.__var = variable

        def evaluate(self, value: (int, float)):
            expression = self.__expression.replace(self.__var, str(value))
            return eval(expression)

        def gradient(self, accuracy, value: (int, float)):
            x1 = value
            x2 = value + 10 ** -accuracy
            y1 = self.evaluate(x1)
            y2 = self.evaluate(x2)
            res = (y2 - y1) / (x2 - x1)
            return round(res, 1) if res - int(res) > 0.999 or res - int(res) < 0.001 else round(res, 3)


def prints(content,style=fontstyle.DEFAULT,fontColor=color.WHITE,back=''):
    print("\033[{};{};{}m{}\033[0m".format(style,fontColor,back,content))



