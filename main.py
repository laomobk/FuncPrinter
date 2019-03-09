from math import *
import fpconf

X_AXIS_ZOOM = fpconf.DEFAULT_X_AXIS_ZOOM
Y_AXIS_ZOOM = fpconf.DEFAULT_Y_AXIS_ZOOM

AXIS_X = fpconf.AXIS_X
AXIS_Y = fpconf.AXIS_Y

START_X = -AXIS_Y /  fpconf.DEFAULT_X_AXIS_ZOOM
START_Y =  AXIS_X /  fpconf.DEFAULT_Y_AXIS_ZOOM

EACH_X = 1 / fpconf.DEFAULT_X_AXIS_ZOOM
EACH_Y = 1 / fpconf.DEFAULT_Y_AXIS_ZOOM

class Screen:
    def __init__(self):
        self.__screen = [' ' for x in range(fpconf.SCREEN_WIDTH)]
        self.__screen = [self.__screen.copy() for i in range(fpconf.SCREEN_HEIGHT)]

        self.__pos = 0
        self.__line_no = 0

    def write_pos(self, ch='*', x=0, y=0):
        self.text(ch, x, y)

    def write(self, ch = '*'):
        if 0 <= self.__pos >= len(self.__screen):
            return None
        
        try:
            self.__screen[self.__line_no][self.__pos] = ch
        except:
            print(self.__line_no,self.__pos)

        self.__pos += 1

    def writenone(self):
        self.__pos += 1

    def reset(self):
        self.__pos = self.__line_no = 0

    def writeln(self):
        self.__line_no += 1
        self.__pos = 0

    def draw(self):
        print('\n' * 26*5)
        for ln in self.__screen:
            for pixel in ln:
                print(pixel, end = ' ')

            print()

    def clear(self):
        self.__screen = [' ' for x in range(fpconf.SCREEN_WIDTH)]
        self.__screen = [self.__screen.copy() for i in range(fpconf.SCREEN_HEIGHT)]

        self.reset()

    def text(self, string, x=0, y=0):
        temp_lineno = self.__line_no
        temp_pos = self.__pos

        self.__line_no = y
        self.__pos = x

        for ch in string:
            self.write(ch)

        self.__line_no = temp_lineno
        self.__pos = temp_pos

class AppMain:
    def __init__(self):
        self.__screen = Screen()
        self.__func_dict = {}

    def draw_func(self, *funcs):
        print('real funcs = ', funcs)

        for func in funcs:
            fname, fbody = self.parse_func(func)
            
            self.__func_dict[fname] = fbody

        for fname, fbody in self.__func_dict.items():
            pass
        
        self.__screen.clear()
        self.__draw_func()
        self.__draw_axis()
        self.__draw_func_name(*funcs)
        self.draw()

    def update(self):
        global START_X
        global START_Y

        global EACH_X
        global EACH_Y

        START_X = -AXIS_Y /  X_AXIS_ZOOM
        START_Y =  AXIS_X /  Y_AXIS_ZOOM

        EACH_X = 1 / X_AXIS_ZOOM
        EACH_Y = 1 / Y_AXIS_ZOOM
        
    def count_y(self, fbody, x):

        try:
            return eval(fbody)

        except (ZeroDivisionError, ValueError) as e:
            return 0

        except SyntaxError:
            self.__screen.text('SyntaxError:' + fbody, y = fpconf.SCREEN_HEIGHT - 1)

            return 0

    def __draw_func_name(self, *funcs):
        lno = 0

        for fname in funcs:
            self.__screen.text(fname, y=lno)

            lno += 1

    def __draw_axis(self):

        for i in range(fpconf.SCREEN_WIDTH - 1):
            self.__screen.write_pos('-', i, AXIS_X)

        self.__screen.write_pos('>',fpconf.SCREEN_WIDTH - 1, AXIS_X)

        for i in range(fpconf.SCREEN_HEIGHT):
            self.__screen.write_pos('|', AXIS_Y, i)

        self.__screen.write_pos('^', AXIS_Y)

    def __draw_each_func(self, func):
        self.__screen.reset()

        x = START_X
        y = START_Y

        for i in range(fpconf.SCREEN_HEIGHT):

            for j in range(fpconf.SCREEN_WIDTH + 1):

                ny = self.count_y(func, x)

                if y - 1 < ny < y + 1:
                    self.__screen.write('*')

                else:
                    self.__screen.writenone()

                x += EACH_X

            x = START_X
            y -= EACH_Y
            self.__screen.writeln()


    def __draw_func(self):
        print('fdict = ', self.__func_dict)

        for _, func in self.__func_dict.items():
            self.__draw_each_func(func)

    def parse_func(self, func):
        'return (func_name, func_body)'

        body = func.split('=')

        if len(body) != 2:
            self.__screen.text('This function is not support')
            return ('ERROR', '1+1')

        return (body[0], body[1])

    def draw(self):
        self.__screen.draw()

    def delete(self, func):
        try:
            #get correct index of deleting function
            keys = list(self.__func_dict.keys())
            index = keys.index(func)

            del self.__func_dict[func]

            return index

        except (KeyError, ValueError) as e:
            print('No such func')
            return -1
    
    def clear(self):
        self.__func_dict = {}
        self.__screen.clear()

import shlex

class Shell:

    def __init__(self):
        self.__app = AppMain()
        self.__funcs = []
        self.__screen = Screen()

    def __get_line(self):
        return input('>>')

    def __parse_line(self, line):
        return shlex.split(line)

    def __parse_cmd(self, tokens):
        if not len(tokens):
            return None

        if hasattr(self, tokens[0]):
            cmd = getattr(self, tokens[0])

        else:
            print('bad instruction')
            return None

        cmd(*tokens[1:])
    
    def __greet(self):
        self.__screen.text('Welcome To FuncPrinter', AXIS_X - 10, AXIS_Y)
        self.__screen.writeln()

        self.__screen.draw()

    def run(self):
        self.__greet()

        while True:
            ln = self.__get_line()
            ts = self.__parse_line(ln)
            self.__parse_cmd(ts)

    #DEFINE INSTRUCTIONS:

    def draw(self, *args):
        tp = tuple(self.__funcs)
        self.__app.draw_func(*tp)

    def add(self, *args):
        fs = ''.join(args)
        self.__funcs.append(fs)

    def clear(self, *args):
        self.__funcs = []
        self.__app.clear()

    def delete(self, *args):
        di = self.__app.delete(args[0])

        if di == -1:
            print('no such func')
            return None

        fn = self.__funcs.pop(di)

        print('func', fn, 'deleted!')

    def exit(self, *args):
        import sys
        sys.exit(0)

    def ml(self, *args):
        global AXIS_Y

        AXIS_Y -= 1
        self.__app.update()

        self.draw()

    def mr(self, *args):
        global AXIS_Y

        AXIS_Y += 1
        self.__app.update()

        self.draw()

    def mu(self, *args):
        global AXIS_X

        AXIS_X -= 1
        self.__app.update()

        self.draw()

    def md(self, *args):
        global AXIS_X

        AXIS_X += 1
        self.__app.update()

        self.draw()

    def zoomxin(self, *args):
        global X_AXIS_ZOOM

        if X_AXIS_ZOOM + fpconf.ZOOM_IN_STEP > fpconf.MAX_ZOOM:
            print('max zoom!')
            return None

        X_AXIS_ZOOM += fpconf.ZOOM_IN_STEP
        self.__app.update()

        self.draw()

    def zoomxout(self, *args):
        global X_AXIS_ZOOM

        if X_AXIS_ZOOM - fpconf.ZOOM_OUT_STEP < fpconf.MIN_ZOOM:
            print('min zoom!')
            return None

        X_AXIS_ZOOM -= fpconf.ZOOM_OUT_STEP

        self.__app.update()

        self.draw()

    def zoomyin(self, *args):
        global Y_AXIS_ZOOM

        if Y_AXIS_ZOOM + fpconf.ZOOM_IN_STEP > fpconf.MAX_ZOOM:
            print('max zoom!')
            return None
        
        Y_AXIS_ZOOM += fpconf.ZOOM_IN_STEP
        self.__app.update()

        self.draw()

    def zoomyout(self, *args):
        global Y_AXIS_ZOOM

        if Y_AXIS_ZOOM - fpconf.ZOOM_OUT_STEP < fpconf.MIN_ZOOM:
            print('min zoom!')
            return None

        Y_AXIS_ZOOM -= fpconf.ZOOM_OUT_STEP
        self.__app.update()

        self.draw()

    def zoomin(self, *args):
        self.zoomyin()
        self.zoomxin()

    def zoomout(self, *args):
        self.zoomyout()
        self.zoomxout()


if __name__ == '__main__':
    sh = Shell()
    sh.run()

    '''
    app = AppMain()
    app.draw_func('y = 100 / x**2')
    '''
    
