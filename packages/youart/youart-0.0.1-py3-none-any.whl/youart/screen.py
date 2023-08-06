'''
Printing utilities
'''
#!/usr/bin/env python3
# coding: utf-8

import os
import platform

from youart.release import __version__


class Style:
    ''' Style class '''
    END = '\033[0m'
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    UNDERSCORE = '\033[4m'
    URL = UNDERSCORE
    REVERSE = '\033[7m'
    TITLE = REVERSE
    CROSSED = '\033[9m'
    OVERLINED = '\033[53m'
    BLUE = '\033[34m'
    RED = '\033[91m'
    FAIL = RED
    ERROR = RED
    GREEN = '\033[92m'
    SUCCESS = GREEN
    OK = GREEN
    YELLOW = '\033[93m'
    WARNING = YELLOW
    WARN = YELLOW
    INFO = '\033[94m'

    def __init__(self):
        if platform.system() == "Windows":
            os.system('color')

    def demo(self):
        ''' demo for style class '''
        print("------start demo----")
        variables = dir(self)
        for item in variables:
            try:
                print(getattr(self, item) + item + self.END)
                print()
            except Exception:  # pylint: disable=broad-except
                break
        print("------stop demo----")

    def render(self, styles, text):
        ''' render styles '''
        style_text = []
        for style in styles.split(';'):
            if hasattr(self, style.upper()):
                style_text.append(getattr(self, style.upper()))
        style_text.append(str(text))
        style_text.append(self.END)
        return "".join(style_text)


s = Style()


def to_screen(msg='', style=None, silent=False, flush=True, **kwargs):
    ''' print to screen with desired styles '''
    if not silent:
        if style:
            msg = s.render(style, msg)
        print(str(msg), flush=flush, **kwargs)


def motd():
    ''' motd '''
    to_screen(f"youart v{__version__}\n", style="bold;blue")
