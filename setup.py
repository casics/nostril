#!/usr/bin/env python3
# =============================================================================
# @file    setup.py
# @brief   Nostril setup file
# @author  Michael Hucka <mhucka@caltech.edu>
# @license Please see the file named LICENSE in the project directory
# @website https://github.com/casics/nostril
# =============================================================================

import os
from   os import path
from   setuptools import setup
import sys

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'requirements.txt')) as f:
    reqs = f.read().rstrip().splitlines()

with open("README.md") as f:
    readme_markdown = f.read()

# The following reads the variables without doing an "import nostril",
# because the latter will cause the python execution environment to fail if
# any dependencies are not already installed -- negating most of the reason
# we're using setup() in the first place.  This code avoids eval, for security.

version = {}
with open(path.join(here, 'nostril/__version__.py')) as f:
    text = f.read().rstrip().splitlines()
    vars = [line for line in text if line.startswith('__') and '=' in line]
    for v in vars:
        setting = v.split('=')
        version[setting[0].strip()] = setting[1].strip().replace("'", '')

# Finally, define our namesake.

setup(
    name             = version['__title__'].lower(),
    description      = version['__description__'],
    long_description = readme_markdown,
    long_description_content_type="text/markdown",
    version          = version['__version__'],
    url              = version['__url__'],
    author           = version['__author__'],
    author_email     = version['__email__'],
    license          = version['__license__'],
    keywords         = "program-analysis text-processing gibberish-detection identifiers",
    packages         = ['nostril'],
    scripts          = ['bin/nostril'],
    package_data     = {'nostril': ['ngram_data.pklz']},
    install_requires = reqs,
    platforms        = 'any',
    python_requires  = '>=3',
)
