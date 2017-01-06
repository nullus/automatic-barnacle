#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test peformance of hashing algorithms
"""

import argparse
import functools
import hashlib
import multiprocessing
import os
import time

class Result(object):
    """
    Present results for testing
    """

    def __init__(self, algorithm, filesize, runtime, *args, **kwargs):
        super(Result, self).__init__(*args, **kwargs)
        self.algorithm = algorithm
        self.filesize = filesize
        self.runtime = runtime

    def __str__(self):
        return "{0}: {1} MiB/s".format(
            self.algorithm,
            (float(self.filesize) / 1048576.0) / self.runtime)

def hash_file(file, block_size, algorithm):
    """
    Hash file, yield result
    """

    def passfile(hash_update):    
        with open(file, "rb") as testdata:
            while True:
                block = testdata.read(block_size)
                if not block:
                    break
                hash_update(block)

    start = time.clock()
    size = os.stat(file).st_size
    # We don't intend to keep the result, so just pass an instance directly
    passfile(getattr(hashlib, algorithm)().update)
    end = time.clock()
    return Result(algorithm, size, end - start)

def run_test(file, block_size):
    """
    Test hashing performance of all available hash algorithms
    """

    # null pass for cache priming
    try:
        with open(file, "rb") as cache:
            while cache.read(block_size):
                pass
    except:
        pass

    pool = multiprocessing.Pool(processes=4)

    return pool.imap_unordered(functools.partial(hash_file, file, block_size), hashlib.algorithms)

    # for algorithm in hashlib.algorithms:
    #     yield hash_file(file, block_size, algorithm)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--block-size", "-b", default=4096, help="Read size")
    parser.add_argument("file", help="Test file")
    args = parser.parse_args()

    for result in run_test(args.file, args.block_size):
        print str(result)

if __name__ == "__main__":
    main()

