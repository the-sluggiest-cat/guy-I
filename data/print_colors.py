class print_colors:
    '''Colors class:reset all colors with colors.reset; two
    sub classes fg for foreground
    and bg for background; use as colors.subclass.colorname.
    i.e. colors.fg.red or colors.bg.greenalso, the generic bold, disable,
    underline, reverse, strike through,
    and invisible work with the main class i.e. colors.bold'''
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'
 
    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'
    
    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'

import datetime
import random

def iprint(msg: object, function_name: str=None):
    if function_name is None:
        function_name = ""
    pprint("INFO   ", msg, function_name, print_colors.fg.blue)

def wprint(msg: object, function_name: str=None):
    if function_name is None:
        function_name = ""
    pprint("WARNING", msg, function_name, print_colors.fg.yellow)

def eprint(msg: object, function_name: str=None):
    if function_name is None:
        function_name = ""
    pprint("ERROR  ", msg, function_name, print_colors.fg.red)

def tprint(msg: object, function_name: str=None):
    if function_name is None:
        function_name = ""
    pprint("TODO   ", msg, function_name, print_colors.fg.orange)

def mprint(msg: object, function_name:str=None):
    if function_name is None:
        function_name = ""
    pprint("MESSAGE", msg, function_name, print_colors.fg.cyan)

def bprint(msg: object, function_name:str=None):
    if function_name is None:
        function_name = ""
    pprint("BOOTUP ", msg, function_name, print_colors.fg.green)

def dprint(msg: object, function_name:str=None):
    if function_name is None:
        function_name = ""
    pprint("DEBUG  ", msg, function_name, print_colors.fg.blue)

def sprint(function_name:str=None):
    if function_name is None:
        function_name = ""
    function_name+="."+"".join([random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZQ1234567890") for i in range(0, random.randint(8, 16))])
    messages = open("data/phrases.txt", "r").read().splitlines()
    to_text = random.choice(messages)
    to_text = to_text.split("_RAND;")
    if len(to_text)>1:
        rand_int = random.randint(1, int(to_text[1]))
        to_text[1] = str(rand_int)
    to_text = "".join(to_text)
    if random.randint(0, 9)==3:
        to_text = "".join([random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZQ1234567890") for i in range(0, random.randint(16, 64))])
    pprint("SILLY  ", to_text, function_name, print_colors.fg.pink)

def pprint(level: str, msg: object, function_name:str=None, color:str=None, end=None):
    if len(function_name)!=0:
        function_name = "."+function_name
    if color is None:
        color = print_colors.fg.darkgrey
    print(print_colors.bold +
          print_colors.fg.darkgrey +
          str(datetime.datetime.now().replace(microsecond=0))+" "+
          print_colors.reset +
          print_colors.bold +
          color +
          level +
          print_colors.reset +
          print_colors.fg.darkgrey +
          "  " +
          print_colors.reset +
          print_colors.fg.cyan +
          "guy%s" %function_name +
          print_colors.reset +" "+
          msg, end=end)

if __name__ == "__main__":
    eprint("this class is used only in other files! this cannot run on its own!", "print_colors")
    exit()
