import os
import shutil

def copy_file(src, dest):
    shutil.copy(src, dest)

def move_file(src, dest):
    shutil.move(src, dest)

def delete_file(path):
    os.remove(path)