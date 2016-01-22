# -*- coding: utf-8 -*-

# std import
import os
import argparse

def read_arg(args):
    """ Take a iterable and return a dict with valid argument """

    parser = _create_parser()

    arg = vars(parser.parse_args(args))

    return arg

def _create_parser():
    """ Create argparse argument parser """

    parser = argparse.ArgumentParser(prog="studies2read",
                                     formatter_class=argparse.
                                     ArgumentDefaultsHelpFormatter)

    parser.add_argument("-a", "--accession-number", type=__accession_number, 
                        help="accession number of studies you want dl reads")
    parser.add_argument("-o", "--output", type=__valid_prefix, 
                        help="prefix of reads file")
    parser.add_argument("-i", "--interactive", action='store_true',
                        help="ask for each read file if you want dl it")
    parser.add_argument("-v", "--verbose", action='store_true', 
                        help="studies2read, become more verbose")

    return parser

def __accession_number(number):
    """ Test if number is a valid accession number """

    number = str(number)

    if isinstance(number, str):
        raise argparse.ArgumentTypeError(number+" isn't a valid accession number")

def __valid_prefix(prefix):
    """Check if prefix is a valid path """
    prefix = str(prefix)
    total_path = ""
    for dir_name in os.path.splitext(os.path.dirname(prefix)):
        total_path = os.path.join(total_path, dir_name)
        if not os.path.isdir(total_path):
            raise argparse.ArgumentTypeError(total_path+"  is not a directory")

    return prefix
