#!/usr/bin/env python
import platform
import os
import sys
import getopt

def getuserdir():
    if 'Windows' in platform.platform():
        # print('Windows detected')
        return os.environ['MYDOCUMENTS']
    else:
        # print('non-Windows detected')
        return os.path.expanduser('~')

    # alternative method on windows left for reference
    # import ctypes

    # dll = ctypes.windll.shell32
    # buf = ctypes.create_unicode_buffer(300)
    # dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False)
    # print(buf.value)

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error as msg:
             raise Usage(msg)
        # more code, unchanged
        print(getuserdir())
    except Usage as err:
        print(err.msg, file=sys.stderr)
        print("for help use --help", file=sys.stderr)
        return 2

if __name__ == "__main__":
    sys.exit(main())
