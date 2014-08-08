# -*- coding: utf-8 -*-

from sys import argv, exit

import raflib

def help():
    print "Usage: -u or --unpack: Unpacks the content of RAF (Riot Archive File).\n" \
          "Example: python rafpy.py -u Archive.raf Archive.raf.dat"

if __name__ == "__main__":
    print "RAFPy 1"
    if len(argv) == 4:
        if argv[1] == "-u" or argv[1] == "--unpack":
            raflib.RAFLib(argv[2], argv[3]).unpack_content()
            exit()
        else:
            help()
            exit()
    else:
        help()
        exit()