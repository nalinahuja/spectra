#Developed by Nalin Ahuja, nalinahuja22

import os
import sys

from const import *

# End Imports-----------------------------------------------------------------------------------------------------------------------------------------------------------

def empty(obj):
    return (not(obj))

def perror(message, status = 1):
    print(message)
    sys.exit(status)

# End Utility Functions-------------------------------------------------------------------------------------------------------------------------------------------------

def mkdir(path):
    os.mkdir(path)

def move(src, dst):
    os.rename(src, dst)

def exists(path):
    return (os.path.isdir(str(path)))

def basename(path):
    return (os.path.basename(str(path)))

def absolute(path):
    return (os.path.realpath(str(path)))

def normalize(path):
    return (os.path.normpath(str(path)))

def get_lmod(path):
    return (os.stat(normalize(str(path))).st_mtime)

def dirname(path):
    return (os.path.dirname(os.path.abspath(str(path))))

def form_path(comps):
    dir = ""
    for path in comps:
        dir += (str(path) + SLASH)
    return (normalize(dir[:-1]))

# End File System Function----------------------------------------------------------------------------------------------------------------------------------------------
