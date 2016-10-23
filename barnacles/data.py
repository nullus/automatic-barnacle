
import os
import sys

def get_files():
    return [
        i.decode(sys.getfilesystemencoding())
        for i in os.walk(os.getcwd()).next()[2]
        if i.lower().endswith('.mp4') or i.lower().endswith('.m4v')
    ]
