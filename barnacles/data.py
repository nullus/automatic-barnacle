# -*- coding: utf-8 -*-

import os
import sys

def get_files():
    return [
        "/".join(os.path.relpath(os.path.join(walk[0], i), os.getcwd()).split(os.sep)).decode(sys.getfilesystemencoding())
        for walk in os.walk(os.getcwd())
        for i in walk[2]
        if i.lower().endswith('.mp4') or i.lower().endswith('.m4v')
    ]

