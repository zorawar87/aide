#!/usr/bin/python3

import argparse
import sys
import aide

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('creds', help="file with ;) data")
    parser.add_argument('epoch', type=int, help="iteration counter epoch")
    parser.add_argument('-d','--debug',dest='headless', action='store_false', help="starts in debugging mode (chrome starts in GUI mode)")
    parser.set_defaults(headless=True)
    ns = parser.parse_args(sys.argv[1:])
    return ns.creds, ns.epoch, ns.headless

def main(creds, epoch, hl):
    with open(creds) as f:
        for l in f:
            un, pw = l.split(" ")
            print("\t\t########## Checking %s at epoch=%d. ##########" % (un.strip(), epoch))
            aide.aide(un.strip(), pw.strip(), epoch, epoch+150, hl)
            epoch += 150

if __name__ == "__main__":
    [creds, epoch, hl] = getArgs()
    main(creds, epoch, hl)

