#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
# from logging.handlers import RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler

from youart.screen import Style

class LogStream:
    ''' LogStream class '''

    def __init__(self):
        self.record = ''
        self.stylist = Style()

    def write(self, text):
        ''' write to log '''
        self.record = text

    def flush(self):
        ''' flush '''
        return

    def to_screen(self, style=None, silent=False, flush=True, **kwargs):
        ''' to string '''
        msg = self.record
        if not silent:
            if style:
                msg = self.stylist.render(style, msg)
            print(str(msg), flush=flush, **kwargs)


log_string = LogStream()


def configure_logger():
    ''' prepare a logger to use by other functions '''
    filename = 'youart.log'

    logger = logging.getLogger('YouArt')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("[%(asctime)s][%(threadName)s] %(message)s")

    to_string = logging.StreamHandler(log_string)
    to_string.setFormatter(formatter)
    to_string.name = 'string'
    logger.addHandler(to_string)

    to_file = TimedRotatingFileHandler(filename, when='m', interval=20, encoding='utf-8')
    to_file.setFormatter(formatter)
    to_file.name = 'file'
    logger.addHandler(to_file)
