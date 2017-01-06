#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test performance, and memory consumption of os.walk
"""

import argparse
import os
import sys
import time


#
# From http://stackoverflow.com/questions/14447333/approximately-how-much-memory-would-a-list-of-80000-items-consume-in-python
# Assume CC-BY-SA
#

totalSizeOf = lambda obj: sum(map(sys.getsizeof, explore(obj, set())))
def explore(obj, memo):
    loc = id(obj)
    if loc not in memo:
        memo.add(loc)
        yield obj
        # Handle instances with slots.
        try:
            slots = obj.__slots__
        except AttributeError:
            pass
        else:
            for name in slots:
                try:
                    attr = getattr(obj, name)
                except AttributeError:
                    pass
                else:
                    #yield from explore(attr, memo)
                    for bar in explore(attr, memo):
                        yield bar
        # Handle instances with dict.
        try:
            attrs = obj.__dict__
        except AttributeError:
            pass
        else:
            #yield from explore(attrs, memo)
            for bar in explore(attrs, memo):
                yield bar
        # Handle dicts or iterables.
        for name in 'keys', 'values', '__iter__':
            try:
                attr = getattr(obj, name)
            except AttributeError:
                pass
            else:
                for item in attr():
                    #yield from explore(item, memo)
                    for bar in explore(item, memo):
                        yield bar

class Result(object):
    """
    Result set for run_test
    """

    def __init__(self, entities, runtime, bytesused, *args, **kwargs):
        """Initialise with results"""
        super(Result, self).__init__(*args, **kwargs)
        self.entities = entities
        self.runtime = runtime
        self.bytesused = bytesused

    def __str__(self):
        """Return string representation"""
        return "Entities: {0}, CPU clock time (s): {1}, Memory usage (bytes): {2}".format(
            self.entities,
            self.runtime,
            self.bytesused
            )

def run_test(path, permute=lambda x: x, predicate=lambda x: True):
    """
    Run test, return results
    """

    start = time.clock()
    output = [permute(i) for i in os.walk(path) if predicate(i)]
    return Result(sum([len(i[2]) for i in output]), time.clock() - start, totalSizeOf(output))


def main():
    """
    Parse arguments, start test
    """

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', help="Starting path")
    args = parser.parse_args()

    print str(run_test(args.path))


if __name__ == "__main__":
    main()

