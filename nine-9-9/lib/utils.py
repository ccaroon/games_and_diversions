from colorama import Fore, Style

def color_foreground(text, color):
    return F"{color}{text}{Style.RESET_ALL}"

def clear_screen():
    print(chr(27)+'[2j')
    print('\033c')
    print('\x1bc')
