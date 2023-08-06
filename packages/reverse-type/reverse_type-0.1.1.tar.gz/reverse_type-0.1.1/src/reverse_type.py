#!/bin/env python

from subprocess import run
import sys


def Main():
    """
    Main
    """
    if len(sys.argv) < 2:
        raise RuntimeError(f'Usage: {sys.argv[0]} TEXT ...')
    revtext = (chr(0x202E) + ' '.join(sys.argv[1:])[::-1] + chr(0x202C))
    status = run(
        ['xclip', '-in', '-target', 'UTF8_STRING', '-selection', 'clipboard'],
        input=revtext.encode(),
    )
    status.check_returncode()
    print(revtext)


if __name__ == '__main__':
    Main()
