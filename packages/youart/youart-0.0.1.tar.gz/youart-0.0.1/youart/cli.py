'''
Command line tool for monitor and save uart logs
'''
#!/usr/bin/env python3
# coding: utf-8

import sys
import threading
import logging
from time import sleep

import serial

from youart.logger import log_string, configure_logger
from youart.arguments import get_arguments
from youart.screen import to_screen, motd
from youart.utils import get_available_ports, list_available_ports

# pylint: disable=line-too-long, disable=broad-except


def save_and_print(ser):
    ''' save to file and print received msg '''
    logger = logging.getLogger('YouArt')
    while True:
        try:
            if not ser.is_open:
                ser.open()
            line = ser.readline()
            if line:
                logger.info(repr(line)[2:-1])  # removes b''
                log_string.to_screen(end='')
            sleep(0.01)
        except (KeyboardInterrupt, SystemExit):
            logger.error("User Interrupt")
            log_string.to_screen(end='')
            break
        except Exception as err:
            logger.error(err)
            log_string.to_screen(end='')
            break


def manual_start(args):
    ''' start '''
    logger = logging.getLogger('YouArt')
    ports = args.ports
    baudrate = int(args.baudrate)
    threads = []
    for port in ports:
        try:
            ser = serial.Serial(port=port, baudrate=baudrate, timeout=1)
            logger.info("successfully opened %s\n\n", port)
            to_screen(f"successfully opened {port} with baudrate={baudrate}", style='green;bold')
            threads.append(
                threading.Thread(
                    name=port.upper(),
                    target=save_and_print,
                    args=(ser,)
                )
            )
        except Exception as err:
            logger.error(err)

    for thread in threads:
        thread.setDaemon(True)
        thread.start()

    flag = True
    while flag:
        for thread in threads:
            flag = flag and thread.is_alive()
        sleep(0.01)


def save_to_file(ser, port):
    ''' save received msg to file '''
    logger = logging.getLogger('YouArt')
    while True:
        try:
            if not ser.is_open:
                ser.open()
            line = ser.readline()
            if line:
                logger.info(repr(line)[2:-1])  # removes b''
            sleep(0.01)
        except (KeyboardInterrupt, SystemExit):
            logger.error("User Interrupt")
            break
        except Exception as err:
            logger.error(err)
            break
    to_screen(f" exit monitoring port: '{port}'", style='red;bold')


def auto_start():
    ''' auto_start '''
    logger = logging.getLogger('YouArt')
    while True:
        ports, _ = get_available_ports()
        threads = []
        for port, desc in ports:
            try:
                ser = serial.Serial(port=port, baudrate=115200, timeout=1)
                to_screen(f"start monitoring port: '{port}' [{desc}]", style='green;bold')
                logger.info("successfully opened %s", desc)
                threads.append(
                    threading.Thread(
                        name=port.upper(),
                        target=save_to_file,
                        args=(ser, port)
                    )
                )
            except Exception as err:
                logger.error(err)

        for thread in threads:
            thread.setDaemon(True)
            thread.start()
        sleep(1)


def main():
    ''' main '''
    motd()
    configure_logger()
    args = get_arguments()

    if args.command == 'list':
        list_available_ports()
        sys.exit()

    elif args.command == 'auto':
        to_screen("starting auto save", style='blue')
        try:
            auto_start()
        except KeyboardInterrupt:
            print("\r\nUser Interrupt.")
            sys.exit()

    elif args.command == 'start':
        try:
            manual_start(args)
        except KeyboardInterrupt:
            print("\r\nUser Interrupt.")
            sys.exit()


if __name__ == "__main__":
    main()
