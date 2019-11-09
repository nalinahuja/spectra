#Developed by Nalin Ahuja, nalinahuja22

import os

_fslash = "/"
_scene = "Scene {}"

def mkdir(dir):
    os.mkdir(dir)

def move(src, dest):
    os.rename(src, dest)

def normalize(path):
    return os.path.normpath(path)

def formDir(arr):
    dir = ""
    for path in arr:
        dir += str(path) + _fslash
    return normalize(dir[:-1])
