#!/usr/bin/python3

import argparse
import sys
import aide

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('creds', help="file with ;) data")
    parser.add_argument('bin', help="file with used data")
    parser.add_argument('epoch', type=int, help="iteration counter epoch")
    parser.add_argument('-d','--debug',dest='headless', action='store_false', help="starts in debugging mode (chrome starts in GUI mode)")
    parser.set_defaults(headless=True)
    ns = parser.parse_args(sys.argv[1:])
    return ns.creds, ns.bin, ns.epoch, ns.headless

def main(creds, bin, epoch, hl):
    with open(creds) as f, open(bin,"a") as o:
        for l in f:
            un, pw = l.split(" ")
            print("\t\t########## Checking %s at epoch=%d. ##########" % (un.strip(), epoch))
            if aide.aide(un.strip(), pw.strip(), epoch, epoch+150, hl):
                epoch += 150
                o.write(l)

if __name__ == "__main__":
    [creds, bin, epoch, hl] = getArgs()
    with open("rc.aide", 'w') as f:
        f.write("%s %s %d".format(creds, bin, epoch))
    main(creds, bin, epoch, hl)

