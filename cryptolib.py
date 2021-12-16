#!cryptoscriptsenv/bin/python

# library for crypto scripts


class colors:
    RED = '\033[0;31m'
    NONE = '\033[0m'
    TITLE = '\033[7;31m'
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    YELLOW = '\033[0;33m'


def cc(f):
    f = round(f, 2)
    if f < 0:
        return f'{colors.RED + "$" + str(abs(f)) + colors.NONE}'
    else:
        return f'{colors.GREEN + "$" + str(abs(f)) + colors.NONE}'
