# -*- coding: utf-8 -*-

"""
Is just main file of study2reads function
"""

# std import
import sys

# project import
from . import cli
from . import ena


def main(arg):
    """ Main function of study2reads function """
    ena.get.reads(**arg)

if __name__ == "__main__":

    main(cli.parser.read_arg(sys.argv[1:]))
