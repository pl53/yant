class Colors:
    # HEADER = '\033[95m'
    # OKBLUE = '\033[94m'
    # OKGREEN = '\033[92m'
    # WARNING = '\033[93m'
    # FAIL = '\033[91m'
    # ENDC = '\033[0m'
    # ANSI color codes
    RS = "\033[0m"    # reset
    HC = "\033[1m"    # hicolor
    UL = "\033[4m"    # underline
    INV = "\033[7m"   # inverse background and foreground
    FBLK = "\033[30m" # foreground black
    FRED = "\033[31m" # foreground red
    FGRN = "\033[32m" # foreground green
    FYEL = "\033[33m" # foreground yellow
    FBLE = "\033[34m" # foreground blue
    FMAG = "\033[35m" # foreground magenta
    FCYN = "\033[36m" # foreground cyan
    FWHT = "\033[37m" # foreground white
    BBLK = "\033[40m" # background black
    BRED = "\033[41m" # background red
    BGRN = "\033[42m" # background green
    BYEL = "\033[43m" # background yellow
    BBLE = "\033[44m" # background blue
    BMAG = "\033[45m" # background magenta
    BCYN = "\033[46m" # background cyan
    BWHT = "\033[47m" # background white

    @staticmethod
    def begin_fcolor(c):
        cl = c.lower()
        if cl == "black" or cl == "bk":
            font_color = Colors.FBLK
        elif cl == "red" or cl == "r":
            font_color = Colors.FRED
        elif cl == "green" or cl == "g":
            font_color = Colors.FGRN
        elif cl == "yellow" or cl == "y":
            font_color = Colors.FYEL
        elif cl == "blue" or cl == "b":
            font_color = Colors.FBLE
        elif cl == "magenta" or cl == "m":
            font_color = Colors.FMAG
        elif cl == "cyan" or cl == "c":
            font_color = Colors.FCYN
        elif cl == "white" or cl == "w":
            font_color = Colors.FWHT
        else: # e.g. plan texts are wanted
            font_color = ''
        return font_color

    @staticmethod
    def begin_bcolor(c):
        cl = c.lower()
        if cl == "black" or cl == "bk":
            bg_color = Colors.BBLK
        elif cl == "red" or cl == "r":
            bg_color = Colors.BRED
        elif cl == "green" or cl == "g":
            bg_color = Colors.BGRN
        elif cl == "yellow" or cl == "y":
            bg_color = Colors.BYEL
        elif cl == "blue" or cl == "b":
            bg_color = Colors.BBLE
        elif cl == "magenta" or cl == "m":
            bg_color = Colors.BMAG
        elif cl == "cyan" or cl == "c":
            bg_color = Colors.BCYN
        elif cl == "white" or cl == "w":
            bg_color = Colors.BWHT
        else: # e.g. plan texts are wanted
            bg_color = ''
        return bg_color

    @staticmethod
    def stop_color():
        return Colors.RS

    @staticmethod
    def colored(s, fc, bc=''):
        # color s with font color (fc) and background color (bc)
        return Colors.begin_fcolor(fc) + \
               Colors.begin_bcolor(bc) + \
               s + Colors.stop_color()
