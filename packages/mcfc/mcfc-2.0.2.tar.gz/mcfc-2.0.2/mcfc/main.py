# main.py
# Text formatting using Minecraft color codes.
# https://github.com/woidzero/MCFC.git


import os
import sys

from .colors import *


if sys.platform.lower() == "win32": 
    os.system('color')


def f_print(*__prompt):
    text = " ".join(__prompt)

    for code in colorCodes:
        text = text.replace(code, RESET + colorCodes[code])

    print(u"{}".format(text))
