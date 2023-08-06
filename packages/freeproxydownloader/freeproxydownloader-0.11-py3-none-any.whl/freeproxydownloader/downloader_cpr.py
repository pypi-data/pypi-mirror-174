import msvcrt
import subprocess
import ctypes
import sys
from ctypes import wintypes
import os
from math import floor
from random import choice

from cprinter import TC

kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
user32 = ctypes.WinDLL("user32", use_last_error=True)
SW_MAXIMIZE = 3
kernel32.GetConsoleWindow.restype = wintypes.HWND
kernel32.GetLargestConsoleWindowSize.restype = wintypes._COORD
kernel32.GetLargestConsoleWindowSize.argtypes = (wintypes.HANDLE,)
user32.ShowWindow.argtypes = (wintypes.HWND, ctypes.c_int)


def get_console_size():
    fd = os.open("CONOUT$", os.O_RDWR)
    X = 60
    Y = 100

    try:
        hCon = msvcrt.get_osfhandle(fd)
        max_size = kernel32.GetLargestConsoleWindowSize(hCon)
        X, Y = max_size.X, max_size.Y
    finally:
        os.close(fd)
    return X, Y


def maximize_console(cols, coly):
    try:
        _ = subprocess.run(
            "mode.com con cols={} lines={}".format(cols, coly), capture_output=True
        )

    except Exception as Fehler:
        pass


class ClearPrinter:
    def __init__(self, softwrap=0, lines=200):
        self.last_print = 0
        self.oldlines = lines
        self.softwrap = softwrap
        self.linestodelete = 0
        self.oldx, self.oldy = get_console_size()
        self.allcolors = [
            "fg_yellow",
            "fg_red",
            "fg_pink",
            "fg_orange",
            "fg_lightred",
            "fg_lightgreen",
            "fg_lightcyan",
            "fg_lightblue",
        ]

    def color_print(self, text, color=None):

        if color is None:
            color = choice(self.allcolors)
        func = getattr(TC(str(text).replace("\n", " ").replace("\r", " ")), color)
        self.pri(func.bg_black)

    def c_yellow(self, text):
        self.color_print(text, color="fg_yellow")

    def c_red(self, text):
        self.color_print(text, color="fg_red")

    def c_pink(self, text):
        self.color_print(text, color="fg_pink")

    def c_orange(self, text):
        self.color_print(text, color="fg_orange")

    def c_lightred(self, text):
        self.color_print(text, color="fg_lightred")

    def c_lightgreen(self, text):
        self.color_print(text, color="fg_lightgreen")

    def c_lightcyan(self, text):
        self.color_print(text, color="fg_lightcyan")

    def c_lightblue(self, text):
        self.color_print(text, color="fg_lightblue")

    def _howmanychars(self, v):
        self.last_print = len(str(v))
        self.linestodelete = floor(self.last_print / self.softwrap)

    def _format_print(self, v):
        toprint = ""
        if self.softwrap == 0:
            toprint = f"{v}".replace("\n", "\\n")
        else:
            v = str(v).replace("\n", " ")
            formatstr = str(v).splitlines()
            for _str in formatstr:
                if len(_str) <= self.softwrap:
                    _str = str(_str + self.softwrap * " " + " ")[: self.softwrap]
                    toprint = toprint + _str
                else:
                    for __str in map("".join, zip(*[iter(_str)] * self.softwrap)):
                        if len(__str) <= self.softwrap:
                            __str = str(__str + self.softwrap * " " + " ")[
                                : self.softwrap
                            ]
                        toprint = toprint + __str
        return toprint

    def pri(self, v=""):
        sys.stdout.write("\r")
        printthat = "".join(["\b" for _ in range(self.softwrap)])

        if self.linestodelete != 0:
            for l in range(self.linestodelete):

                sys.stdout.write("\r")

                sys.stdout.write(printthat)

        sys.stdout.flush()
        toprint = self._format_print(v)
        self._howmanychars(toprint)

        sys.stdout.write(f"\r{toprint}")
        sys.stdout.flush()
