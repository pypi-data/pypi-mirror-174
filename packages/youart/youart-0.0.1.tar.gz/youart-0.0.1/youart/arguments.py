'''
Utilities
'''
#!/usr/bin/env python3
# coding: utf-8


import sys
import argparse
from youart.release import __version__


def parse_arguments():
    ''' get args '''
    parser = argparse.ArgumentParser(
        prog="youart",
        description='save uart logs',
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=True,
        epilog="")

    commands = parser.add_subparsers(
        title='commands',
        dest="command",
        required=True,
        metavar='COMMAND')

    parser.add_argument(
        "--version",
        action="version",
        version=f'%(prog)s version {__version__}',
        help="show version and exit")

    start = commands.add_parser(
        'start',
        help='start monitor on ports.')

    _ = commands.add_parser(
        'list',
        help='list available ports.')

    _ = commands.add_parser(
        'auto',
        help='auto save all connected and available uart ports.')

    start.add_argument(
        'ports',
        metavar="COMX [COMY ...]",
        nargs='+',
        help='ports')

    start.add_argument(
        '-b',
        '--baudrate',
        dest='baudrate',
        metavar="BAUDRATE",
        help='Baudrate')

    return parser.parse_args(sys.argv[1:])


def get_arguments():
    ''' process arguments '''
    args = parse_arguments()
    if 'baudrate' in args:
        if not args.baudrate:
            args.baudrate = "115200"
    else:
        args.baudrate = "115200"

    return args
