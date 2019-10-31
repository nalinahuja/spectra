import os

_fslash = "/"
_scene = "Scene {}"

def normalize(path):
    return os.path.normpath(path)

def move(src, dest):
    os.rename(src, dest)

def formDir(arr):
    dir = ""
    for path in arr:
        dir += str(path) + _fslash
    return normalize(dir[:-1])

def mkdir(dir):
    os.mkdir(dir)
