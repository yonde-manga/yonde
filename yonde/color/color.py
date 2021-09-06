from colorama import init, Fore, Style


class Color(object):
    def __init__(self):
        init()
        self.black = Fore.BLACK
        self.green = Fore.GREEN
        self.yellow = Fore.YELLOW
        self.cyan = Fore.CYAN
        self.white = Fore.WHITE
        self.magenta = Fore.MAGENTA
        self.bold = Style.BRIGHT
        self.reset = Style.RESET_ALL
        self.bright = Style.BRIGHT
