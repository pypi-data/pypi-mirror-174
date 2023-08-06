__version__ = '0.2'

# NUMBERS
def isdecimal(var):
    if var.is_integer():
        decimal = False
    else:
        decimal = True
    return decimal
def factorial(num):
    if num < 0:
        factorial = "InputError: Factorial does not exist for negative numbers"
    elif num == 0:
       factorial = 1
    else:
        factorial = 1
        for i in range(1, num + 1):
           factorial = factorial * i
    return factorial
# PRINTING
def println(var, num = 1):
    print("\n"*num + var)
def printsln(var):
    print(var, end='')
def printx(var, num):
    for i in range(0, num):
        print(var)

# TEXT FORMATTING
def bold(var):
    text = "\033[1m" + var + "\033[0m"
    return text
def b(var):
    text = "\033[1m" + var + "\033[0m"
    return text
def italic(var):
    text = "\033[3m" + var + "\033[0m"
    return text
def i(var):
    text = "\033[3m" + var + "\033[0m"
    return text
def underline(var):
    text = "\033[4m" + var + "\033[0m"
    return text
def underl(var):
    text = "\033[4m" + var + "\033[0m"
    return text
def ul(var):
    text = "\033[4m" + var + "\033[0m"
    return text
def format(var = ''):
    if var == 'bold' or var == 'b':
        print("\033[1m", end='')
    elif var == 'italic' or var == 'i':
        print("\033[3m", end='')
    elif var == 'underline' or var == 'underl' or var == 'ul':
        print("\033[4m", end='')
    elif var == 'black':
        print("\033[0;30m", end='')
    elif var == 'red':
        print("\033[0;31m", end='')
    elif var == 'green':
        print("\033[0;32m", end='')
    elif var == 'yellow':
        print("\033[0;33m", end='')
    elif var == 'blue':
        print("\033[0;34m", end='')
    elif var == 'magenta':
        print("\033[0;35m", end='')
    elif var == 'cyan':
        print("\033[0;36m", end='')
    elif var == 'white':
        print("\033[0;37m", end='')
    elif var == 'bright_black':
        print("\033[0;90m", end='')
    elif var == 'bright_red':
        print("\033[0;91m", end='')
    elif var == 'bright_green':
        print("\033[0;92m", end='')
    elif var == 'bright_yellow':
        print("\033[0;93m", end='')
    elif var == 'bright_blue':
        print("\033[0;94m", end='')
    elif var == 'bright_magenta':
        print("\033[0;95m", end='')
    elif var == 'bright_cyan':
        print("\033[0;96m", end='')
    elif var == 'bright_white':
        print("\033[0;97m", end='')
    elif var == 'clear':
        print("\033[0m", end='')
        
def clear():
    print("\033[0m", end='')
### COLORS
def black(var = '', set = False):
    if var == '':
        print("\033[0;30m", end='')
        text = None
    else:
        if set:
            text = "\033[0;30m" + var
        else:
            text = "\033[0;30m" + var + "\033[0m"
    return text
def red(var = '', set = False):
    if var == '':
        print("\033[0;31m", end='')
        text = None
    else:
        if set:
            text = "\033[0;31m" + var
        else:
            text = "\033[0;31m" + var + "\033[0m"
    return text
def green(var = '', set = False):
    if var == '':
        print("\033[0;32m", end='')
        text = None
    else:
        if set:
            text = "\033[0;32m" + var
        else:
            text = "\033[0;32m" + var + "\033[0m"
    return text
def yellow(var = '', set = False):
    if var == '':
        print("\033[0;33m", end='')
        text = None
    else:
        if set:
            text = "\033[0;33m" + var
        else:
            text = "\033[0;33m" + var + "\033[0m"
    return text
def blue(var = '', set = False):
    if var == '':
        print("\033[0;34m", end='')
        text = None
    else:
        if set:
            text = "\033[0;34m" + var
        else:
            text = "\033[0;34m" + var + "\033[0m"
    return text
def magenta(var = '', set = False):
    if var == '':
        print("\033[0;35m", end='')
        text = None
    else:
        if set:
            text = "\033[0;35m" + var
        else:
            text = "\033[0;35m" + var + "\033[0m"
    return text
def cyan(var = '', set = False):
    if var == '':
        print("\033[0;36m", end='')
        text = None
    else:
        if set:
            text = "\033[0;36m" + var
        else:
            text = "\033[0;36m" + var + "\033[0m"
    return text
def white(var = '', set = False):
    if var == '':
        print("\033[0;37m", end='')
        text = None
    else:
        if set:
            text = "\033[0;37m" + var
        else:
            text = "\033[0;37m" + var + "\033[0m"
    return text
def color(var = '', text = ''):
    if text == '':
        if var == 'black':
            print("\033[0;30m", end='')
        elif var == 'red':
            print("\033[0;31m", end='')
        elif var == 'green':
            print("\033[0;32m", end='')
        elif var == 'yellow':
            print("\033[0;33m", end='')
        elif var == 'blue':
            print("\033[0;34m", end='')
        elif var == 'magenta':
            print("\033[0;35m", end='')
        elif var == 'cyan':
            print("\033[0;36m", end='')
        elif var == 'white':
            print("\033[0;37m", end='')
        elif var == 'bright_black':
            print("\033[0;90m", end='')
        elif var == 'bright_red':
            print("\033[0;91m", end='')
        elif var == 'bright_green':
            print("\033[0;92m", end='')
        elif var == 'bright_yellow':
            print("\033[0;93m", end='')
        elif var == 'bright_blue':
            print("\033[0;94m", end='')
        elif var == 'bright_magenta':
            print("\033[0;95m", end='')
        elif var == 'bright_cyan':
            print("\033[0;96m", end='')
        elif var == 'bright_white':
            print("\033[0;97m", end='')
        elif var == 'clear':
            print("\033[0m", end='')
    else:
        if var == 'black':
            text = "\033[0;30m" + text + "\033[0m"
        elif var == 'red':
            text = "\033[0;31m" + text + "\033[0m"
        elif var == 'green':
            text = "\033[0;32m" + text + "\033[0m"
        elif var == 'yellow':
            text = "\033[0;33m" + text + "\033[0m"
        elif var == 'blue':
            text = "\033[0;34m" + text + "\033[0m"
        elif var == 'magenta':
            text = "\033[0;35m" + text + "\033[0m"
        elif var == 'cyan':
            text = "\033[0;36m" + text + "\033[0m"
        elif var == 'white':
            text = "\033[0;37m" + text + "\033[0m"
        elif var == 'bright_black':
            text = "\033[0;90m" + text + "\033[0m"
        elif var == 'bright_red':
            text = "\033[0;91m" + text + "\033[0m"
        elif var == 'bright_green':
            text = "\033[0;92m" + text + "\033[0m"
        elif var == 'bright_yellow':
            text = "\033[0;93m" + text + "\033[0m"
        elif var == 'bright_blue':
            text = "\033[0;94m" + text + "\033[0m"
        elif var == 'bright_magenta':
            text = "\033[0;95m" + text + "\033[0m"
        elif var == 'bright_cyan':
            text = "\033[0;96m" + text + "\033[0m"
        elif var == 'bright_white':
            text = "\033[0;97m" + text + "\033[0m"
        else:
            text = None
        return text
def cprint(var, text):
    if var == 'bold' or var == 'b':
        print("\033[1m" + text + '\033[0m')
    elif var == 'italic' or var == 'i':
        print("\033[3m" + text + '\033[0m')
    elif var == 'underline' or var == 'underl' or var == 'ul':
        print("\033[4m" + text + '\033[0m')
    elif var == 'black':
        print("\033[0;30m" + text + "\033[0m")
    elif var == 'red':
        print("\033[0;31m" + text + "\033[0m")
    elif var == 'green':
        print("\033[0;32m" + text + "\033[0m")
    elif var == 'yellow':
        print("\033[0;33m" + text + "\033[0m")
    elif var == 'blue':
        print("\033[0;34m" + text + "\033[0m")
    elif var == 'magenta':
        print("\033[0;35m" + text + "\033[0m")
    elif var == 'cyan':
        print("\033[0;36m" + text + "\033[0m")
    elif var == 'white':
        print("\033[0;37m" + text + "\033[0m")
    elif var == 'bright_black':
        print("\033[0;90m" + text + "\033[0m")
    elif var == 'bright_red':
        print("\033[0;91m" + text + "\033[0m")
    elif var == 'bright_green':
        print("\033[0;92m" + text + "\033[0m")
    elif var == 'bright_yellow':
        print("\033[0;93m" + text + "\033[0m")
    elif var == 'bright_blue':
        print("\033[0;94m" + text + "\033[0m")
    elif var == 'bright_magenta':
        print("\033[0;95m" + text + "\033[0m")
    elif var == 'bright_cyan':
        print("\033[0;96m" + text + "\033[0m")
    elif var == 'bright_white':
        print("\033[0;97m" + text + "\033[0m")
    else:
        print(text)
    return text