# -*- coding: utf-8 -*-

# std import
import sys

# project import
from . import cli
from . import ena

arg = cli.parser.read_arg(sys.argv[1:])

ena.get.reads(**arg)
