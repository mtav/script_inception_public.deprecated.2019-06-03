#!/usr/bin/env python
import platform
import os

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

print getuserdir()
