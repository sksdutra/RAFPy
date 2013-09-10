# -*- coding: utf-8 -*-

import sys

import raflib

def help():
    print "RAFPy\n-u or --unpack: Unpacks the content of RAF (Riot Archive File).\n" \
          "Example: python rafpy.py -u Archive.raf Archive.raf.dat"

if __name__ == "__main__":
    if len(sys.argv) == 4:
        if sys.argv[1] == "-u" or sys.argv[1] == "--unpack": raflib.RAFLib(sys.argv[2], sys.argv[3]).extract_content()
        else: help()
    else: help()