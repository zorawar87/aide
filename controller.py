#!/usr/bin/python3

"""
This module scales aide to run for N users
@see https://github.com/zorawar87/aide
@see https://medium.com/@zorawar87/scraping-trincolls-alumni-database-c671c8aa09b8
"""

import argparse
import sys
import logging

import coloredlogs as cl
import aide

logging.basicConfig(level=logging.DEBUG)
cl.install(level='DEBUG')


def get_args():
    """
    returns command line args
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('cred_file', help="file with ;) data")
    parser.add_argument('log_file', help="file to log used data")
    parser.add_argument('epoch', type=int, help="iteration counter epoch")
    parser.add_argument(
        '-d',
        '--debug',
        dest='headless',
        action='store_false',
        help="starts in debugging mode (chrome starts in GUI mode)")
    parser.set_defaults(headless=True)
    namespace = parser.parse_args(sys.argv[1:])
    return namespace.cred_file, namespace.log_file, namespace.epoch, namespace.headless


def controller(cred_file, log, epoch, hless):
    """
    controls iterations of aide
    """
    iterator = epoch
    with open(cred_file) as file, open(log, "a") as log_file:
        for line in file:
            with open("rc.aide", 'a') as file:
                file.write("started ./controller.py {} {} {}\n".format(cred_file, log_file, iterator))
            splits = line.split(" ")
            uname, pword = splits[0], splits[1]
            logging.debug(
                "########## Checking %s at epoch=%d. ##########",
                uname.strip(), iterator)
            new_epoch = aide.aide(
                uname.strip(),
                pword.strip(),
                iterator,
                iterator + 150,
                hless)
            if new_epoch != -1:
                iterator = new_epoch
                out_string = line.strip() + str(iterator) + str(iterator + 150) + "\n"
                log_file.write("{} {}\n".format(uname.strip(), pword.strip()))


def main():
    """
    initiates scaled extraction
    """
    [cred_file, log_file, epoch, hless] = get_args()
    controller(cred_file, log_file, epoch, hless)


if __name__ == "__main__":
    main()
