#!/usr/bin/env python
# -*- coding: utf-8 -*-

# setuptools import
from setuptools import setup, find_packages

# package information import
from study2reads import __version__, __name__

# find requirement import
from pip.req import parse_requirements

# find requirement
install_reqs = parse_requirements("requirements.txt")
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name = __name__,
    version = __version__,
    packages = find_packages(),

    author = "Pierre Marijon",
    author_mail = "pierre@marijon.fr",
    description = "Download all read realted to study in European Nucleotide \
    Archive database",
    long_description = "Please see README on https://github.com/natir/study2reads",
    keywords = "cli tools client",
    url = "https://github.com/natir/study2reads",

    install_requires = reqs,

    entry_points={
        'console_scripts': [
            'study2reads = study2reads.__main__'
        ]
    },

    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research"
    ]
)
