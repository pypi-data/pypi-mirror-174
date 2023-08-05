CSI = '\033['  # CSI(Control Sequence Introducer) 相当于控制头
RESET_ALL = '\033[0m'


def code_to_str(code):
    return CSI + str(code) + 'm'


class CsiCodes:
    def __init__(self):
        for name_in_dir in dir(self):
            if not name_in_dir.startswith('_'):
                value = getattr(self, name_in_dir)
                setattr(self, name_in_dir + 's', code_to_str(value))


class CsiFore(CsiCodes):
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    PURPLE = 35
    CYAN = 36
    WHITE = 37
    RESET = 39

    """亮色"""
    LIGHTBLACK = 90
    LIGHTRED = 91
    LIGHTGREEN = 92
    LIGHTYELLOW = 93
    LIGHTBLUE = 94
    LIGHTPURPLE = 95
    LIGHTCYAN = 96
    LIGHTWHITE = 97


class CsiBack(CsiCodes):
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    PURPLE = 45
    CYAN = 46
    WHITE = 47
    RESET = 49

    """亮色"""
    LIGHTBLACK = 100
    LIGHTRED = 101
    LIGHTGREEN = 102
    LIGHTYELLOW = 103
    LIGHTBLUE = 104
    LIGHTPURPLE = 105
    LIGHTCYAN = 106
    LIGHTWHITE = 107


class CsiStyle(CsiCodes):
    BRIGHT = 1
    DIM = 2
    ITALIC = 3
    UNDERLINE = 4
    INVERSION = 7
    HIDE = 8
    DELETE = 9

    """关闭代码数值比开启代码大20"""
    RESET_ALL = 0
    NORMAL = 22  # 颜色或者亮度恢复正常（不好取名）
    ITALIC_OFF = 23
    UNDERLINE_OFF = 24
    INVERSION_OFF = 27
    HIDE_OFF = 28
    DELETE_OFF = 29


class CsiCursor:
    """
    光标控制代码的封装，
    带s_后缀的返回csi字符串，不带的直接执行
    """
    def hide_s(self):
        """隐藏光标"""
        return CSI + '?25l'

    def show_s(self):
        """显示光标"""
        return CSI + '?25h'

    def up_s(self, n=1):
        """光标上移n行"""
        return CSI + f'{n}A'

    def move_left_s(self, n=1):
        """光标左移n列"""
        return CSI + f'{n}D'

    def move_right_s(self, n=1):
        """光标右移n列"""
        return CSI + f'{n}C'

    def down_s(self, n=1):
        """光标下移n行"""
        return CSI + f'{n}B'

    def moveto_linehead_s(self):
        """移动光标到该行行首"""
        return '\r'

    def pos_s(self, x=1, y=1):
        """移动光标到指定列行（x对应列，y对应行）"""
        return CSI + f'{y};{x}H'

    def hor_pos_s(self, x=1):
        """水平移动光标到指定列"""
        return CSI + f'{x}G'

    """下面的控制代码可能不适配于某些终端"""
    def moveto_next_line_s(self, n=1):
        """光标相对于当前位置，往上移动n行，并且回到行首"""
        return CSI + f'{n}E'

    def moveto_prev_line_s(self, n=1):
        """光标相对于当前位置，往下移动n行，并且回到行首"""
        return CSI + f'{n}F'

    def save_pos_s(self):
        """保存光标位置"""
        return CSI + 's'

    def restore_pos_s(self):
        """恢复光标位置（到之前保存的位置，如果没设置新的位置，默认屏幕开头）"""
        return CSI + 'u'

    """
    解释一下
    光标坐标最小是1，如果超出了范围，则会被限制为最小值或者最大值，
    对于光标的x，y坐标，有最大值的限制，具体数值看控制台的屏幕宽度，
    光标会在其所在位置打印新字符，
    """

    """以下作用同上，但不反回字符串直接执行"""

    def hide(self):
        print(CSI + '?25l', end='', flush=True)

    def show(self):
        print(CSI + '?25h', end='', flush=True)

    def up(self, n=1):
        if n <= 0:
            return
        print(CSI + f'{n}A', end='', flush=True)

    def move_left(self, n=1):
        if n <= 0:
            return
        print(CSI + f'{n}D', end='', flush=True)

    def move_right(self, n=1):
        if n <= 0:
            return
        print(CSI + f'{n}C', end='', flush=True)

    def down(self, n=1):
        if n <= 0:
            return
        print(CSI + f'{n}B', end='', flush=True)

    def moveto_linehead(self):
        print('\r', end='', flush=True)

    def pos(self, x=1, y=1):
        print(CSI + f'{y};{x}H', end='', flush=True)
    
    def hor_pos(self, x=1):
        print(CSI + f'{x}G', end='', flush=True)

    """下面的控制代码某些终端可能不支持"""
    def moveto_next_line(self, n=1):
        if n <= 0:
            return
        print(CSI + f'{n}E', end='', flush=True)

    def moveto_prev_line(self, n=1):
        if n <= 0:
            return
        print(CSI + f'{n}F', end='', flush=True)

    def save_pos(self):
        print(CSI + 's', end='', flush=True)

    def restore_pos(self):
        print(CSI + 'u', end='', flush=True)


Fore = CsiFore()
Back = CsiBack()
Style = CsiStyle()
Cursor = CsiCursor()
