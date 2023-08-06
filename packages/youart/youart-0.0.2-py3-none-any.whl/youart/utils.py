'''
utilities
'''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
from serial.tools.list_ports import comports

from youart.screen import to_screen

def get_available_ports():
    ''' try to open ports to check if they are available '''
    ports = comports()
    available = []
    not_available = []
    for port, desc, _ in sorted(ports):
        try:
            ser = serial.Serial(port=port, timeout=1)
            ser.close()
            available.append((port, desc))
        except Exception:  # pylint: disable=broad-except
            not_available.append((port, desc))
    return available, not_available


def list_available_ports():
    ''' list available uart ports '''
    ports_a, ports_na = get_available_ports()
    if ports_a:
        to_screen("available:")
        for port, desc in ports_a:
            to_screen(f"\t{port}: {desc}", style='green')
    if ports_na:
        to_screen("not available:")
        for port, desc in ports_na:
            to_screen(f"\t{port}: {desc}", style='red')
    print()
