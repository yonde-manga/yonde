from colorama import init, Fore, Style


class Color(object):
    def __init__(self):
        init()
        self.black = Fore.BLACK
        self.green = Fore.GREEN
        self.yellow = Fore.LIGHTYELLOW_EX
        self.cyan = Fore.CYAN
        self.red = Fore.LIGHTRED_EX
        self.blue = Fore.LIGHTBLUE_EX
        self.white = Fore.WHITE
        self.magenta = Fore.LIGHTMAGENTA_EX
        self.bold = Style.BRIGHT
        self.reset = Style.RESET_ALL
        self.bright = Style.BRIGHT
